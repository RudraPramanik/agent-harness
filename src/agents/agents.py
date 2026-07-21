import os
from dataclasses import dataclass, field

from langgraph.graph.state import CompiledStateGraph
from langgraph.pregel import Pregel

from agents.bg_task_agent.bg_task_agent import bg_task_agent
from agents.chatbot import chatbot
from agents.command_agent import command_agent
from agents.github_mcp_agent.github_mcp_agent import github_mcp_agent
from agents.interrupt_agent import interrupt_agent
from agents.knowledge_base_agent import kb_agent
from agents.langgraph_supervisor_agent import langgraph_supervisor_agent
from agents.langgraph_supervisor_hierarchy_agent import langgraph_supervisor_hierarchy_agent
from agents.lazy_agent import LazyLoadingAgent
from agents.rag_assistant import rag_assistant
from agents.research_assistant import research_assistant
from schema import AgentInfo

DEFAULT_AGENT = "research-assistant"

# Type alias to handle LangGraph's different agent patterns
# - @entrypoint functions return Pregel
# - StateGraph().compile() returns CompiledStateGraph
AgentGraph = CompiledStateGraph | Pregel  # What get_agent() returns (always loaded)
AgentGraphLike = CompiledStateGraph | Pregel | LazyLoadingAgent  # What can be stored in registry


class AgentPausedError(LookupError):
    """Raised when an agent exists in the registry but is paused (enabled=False)."""

    def __init__(self, agent_id: str) -> None:
        self.agent_id = agent_id
        super().__init__(f"Agent '{agent_id}' is paused")


@dataclass
class Agent:
    description: str
    graph_like: AgentGraphLike
    enabled: bool = True
    required_env: frozenset[str] = field(default_factory=frozenset)


agents: dict[str, Agent] = {
    "chatbot": Agent(description="General-purpose conversational agent.", graph_like=chatbot),
    "research-assistant": Agent(
        description="Web search, weather, and calculator for open-ended research.",
        graph_like=research_assistant,
    ),
    "rag-assistant": Agent(
        description="Document Q&A over your ChromaDB knowledge base.",
        graph_like=rag_assistant,
        enabled=False,
        required_env=frozenset({"OPENAI_API_KEY"}),
    ),
    "command-agent": Agent(
        description="Command routing and flow control demo.",
        graph_like=command_agent,
        enabled=False,
    ),
    "bg-task-agent": Agent(
        description="Background task execution demo.",
        graph_like=bg_task_agent,
        enabled=False,
    ),
    "langgraph-supervisor-agent": Agent(
        description="Multi-agent supervisor pattern.",
        graph_like=langgraph_supervisor_agent,
        enabled=False,
    ),
    "langgraph-supervisor-hierarchy-agent": Agent(
        description="Nested hierarchy of supervised agents.",
        graph_like=langgraph_supervisor_hierarchy_agent,
        enabled=False,
    ),
    "interrupt-agent": Agent(
        description="Human-in-the-loop with LangGraph interrupts.",
        graph_like=interrupt_agent,
        enabled=False,
    ),
    "knowledge-base-agent": Agent(
        description="RAG via Amazon Bedrock knowledge base.",
        graph_like=kb_agent,
        enabled=False,
        required_env=frozenset({"AWS_KB_ID"}),
    ),
    "github-mcp-agent": Agent(
        description="GitHub MCP tools for repos and development workflows.",
        graph_like=github_mcp_agent,
        enabled=False,
        required_env=frozenset({"GITHUB_PAT"}),
    ),
}


def resolve_agent_enablement() -> None:
    """Opt-in: auto-enable paused agents when all required_env keys are set.

    Call only when AUTO_ENABLE_AGENTS is true. Does not disable agents that are
    already enabled.
    """
    for agent in agents.values():
        if agent.enabled or not agent.required_env:
            continue
        if all(os.environ.get(key) for key in agent.required_env):
            agent.enabled = True


async def load_agent(agent_id: str) -> None:
    """Load lazy agents if needed."""
    graph_like = agents[agent_id].graph_like
    if isinstance(graph_like, LazyLoadingAgent):
        await graph_like.load()


def get_agent(agent_id: str) -> AgentGraph:
    """Get an agent graph, loading lazy agents if needed.

    Raises:
        KeyError: If agent_id is not in the registry.
        AgentPausedError: If the agent exists but is paused (enabled=False).
    """
    agent = agents[agent_id]
    if not agent.enabled:
        raise AgentPausedError(agent_id)

    agent_graph = agent.graph_like

    # If it's a lazy loading agent, ensure it's loaded and return its graph
    if isinstance(agent_graph, LazyLoadingAgent):
        if not agent_graph._loaded:
            raise RuntimeError(f"Agent {agent_id} not loaded. Call load() first.")
        return agent_graph.get_graph()

    # Otherwise return the graph directly
    return agent_graph


def get_all_agent_info() -> list[AgentInfo]:
    """Return metadata for enabled agents only."""
    return [
        AgentInfo(key=agent_id, description=agent.description)
        for agent_id, agent in agents.items()
        if agent.enabled
    ]
