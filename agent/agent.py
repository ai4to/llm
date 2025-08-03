from openai import OpenAI
from dotenv import load_dotenv
import os
from os import getenv

from agno.agent import Agent
from agno.models.openai.like import OpenAILike
from agno.memory.v2.memory import Memory
from agno.storage.sqlite import SqliteStorage
from agno.tools.reasoning import ReasoningTools
from agno.playground import Playground
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.tools.googlesearch import GoogleSearchTools

load_dotenv()
memory = Memory(
    model=OpenAILike(
        id="qwen/qwen3-235b-a22b-thinking-2507",
        api_key=getenv("OPENAI_API_KEY"),
        base_url="https://openrouter.ai/api/v1"),
    # Store memories in a SQLite database
    db=SqliteMemoryDb(table_name="user_memories", db_file="tmp/agent.db"),
)
agent_storage = "tmp/agents.db"

counselor_agent = Agent(
    name="Counselor Agent",
    model=OpenAILike(
        id="qwen/qwen3-235b-a22b-thinking-2507",
        api_key=getenv("OPENAI_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    ),
    tools=[ReasoningTools(add_instructions=True), GoogleSearchTools()],
    instructions=[
        "Use Reality Therapy Chain‑of‑Empathy (RT‑CoE) to interpret the user's emotional and situational context.",
        "Reason sequentially:",
        "Step 1: Identify the core emotion the user expresses.",
        "Step 2: Detect any cognitive distortions or situational triggers.",
        "Step 3: Uncover the user's underlying beliefs or personal context.",
        "Step 4: Highlight explicit emotion words and contributing factors.",
        "Step 5: Determine unmet needs or goals associated with the emotion.",
        "Aapply RT‑CoE techniques to:",
        "Empathize and validate the user's emotional experience.",
        "Reinforce their strengths and resilience.",
        "Offer culturally sensitive, problem‑focused coping suggestions.",
        "Structure the reply as brief, warm paragraphs with no bullet lists. Don't be verbose, don't assume anything about the user's culture unless the user explicity tells you about their culture.",
        "If the users asks for resources, provide them with relevant resources from google search."
    ],
    storage=SqliteStorage(table_name="counselor_agent", db_file=agent_storage),
    memory = memory,
    enable_agentic_memory=True,
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

playground_app = Playground(agents=[counselor_agent])
app = playground_app.get_app()

if __name__ == "__main__":
    playground_app.serve("playground:app", reload=True)
