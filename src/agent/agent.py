import os

from deepagents import create_deep_agent
from deepagents.backends import FilesystemBackend
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()


def _project_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


mcp_tools = []

llm = ChatOpenAI(
    model="anthropic/claude-haiku-4.5",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    extra_body={
        "cache_control": {"type": "ephemeral"},
        "provider": {
            "require_parameters": True,
            "data_collection": "deny",
        },
    },
)

root = _project_root()
workspace_dir = os.path.join(root, "workspace")
backend = FilesystemBackend(root_dir=workspace_dir, virtual_mode=True)
skills_dir = os.path.join(workspace_dir, "skills")
memory_path = os.path.join(workspace_dir, "memories", "AGENTS.md")

graph = create_deep_agent(
    backend=backend,
    model=llm,
    tools=mcp_tools,
    checkpointer=InMemorySaver(),
    skills=[skills_dir] if os.path.isdir(skills_dir) else [],
    memory=[memory_path] if os.path.isfile(memory_path) else [],
    system_prompt="You are a helpful research assistant.",
)