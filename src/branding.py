"""Central branding configuration — edit this file to personalize the project."""

APP_TITLE = "AI Agent Studio"
APP_ICON = "✨"
APP_TAGLINE = (
    "Build, run, and chat with LangGraph agents — powered by FastAPI and Streamlit."
)

# Update these when your GitHub repo is ready.
GITHUB_OWNER = "YOUR_USERNAME"
GITHUB_REPO = "ai-agent-studio"
GITHUB_REPO_URL = f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}"
GITHUB_RAW_BASE = f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/blob/main"

AUTHOR_NAME = "Niloy Dey"
AUTHOR_LINK = ""  # e.g. "https://linkedin.com/in/your-profile"

PRIVACY_NOTICE = (
    "Conversations may be logged for quality improvement when tracing is enabled "
    "(LangSmith / Langfuse). Disable tracing in production if you do not need it."
)

# Per-agent welcome messages shown in the chat UI.
WELCOME_MESSAGES: dict[str, str] = {
    "chatbot": "Welcome to AI Agent Studio! I'm a general-purpose assistant — ask me anything.",
    "research-assistant": (
        "Welcome! I'm your research assistant with web search, weather, and calculator tools. "
        "What would you like to explore?"
    ),
    "rag-assistant": (
        "Welcome! I'm your document assistant. I answer questions from your indexed knowledge base. "
        "Ask me about policies, docs, or anything in the database."
    ),
    "command-agent": "Welcome! I'm a command-routing agent. Tell me what you'd like to accomplish.",
    "interrupt-agent": (
        "Welcome! I'm a human-in-the-loop demo agent. Share your birthday and I'll walk you "
        "through an interactive prediction."
    ),
    "github-mcp-agent": (
        "Welcome! I'm your GitHub assistant with MCP tools for repos, issues, and code search."
    ),
    "bg-task-agent": "Welcome! I run background tasks — ask me to kick off a long-running job.",
    "langgraph-supervisor-agent": "Welcome! I'm a multi-agent supervisor. Describe a complex task.",
    "langgraph-supervisor-hierarchy-agent": (
        "Welcome! I'm a hierarchical supervisor coordinating nested specialist agents."
    ),
    "knowledge-base-agent": (
        "Welcome! I'm a RAG agent backed by Amazon Bedrock Knowledge Base."
    ),
}

DEFAULT_WELCOME = "Welcome to AI Agent Studio! Pick an agent in the sidebar and start chatting."
