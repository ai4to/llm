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
    name="AI4TO",
    user_id="Demo",
    session_id='01',
    model=OpenAILike(
        id="qwen/qwen3-235b-a22b-thinking-2507",
        api_key=getenv("OPENAI_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        max_completion_tokens=9000
    ),
    tools=[ReasoningTools(add_instructions=True), GoogleSearchTools()],
    instructions=[
    "Respond with genuine empathy and understanding, as if you're a thoughtful friend who truly cares about the person's wellbeing.",
    "Keep replies concise, clear, and grounded; prefer one to three helpful ideas.",
    "When someone shares something emotional or challenging, listen deeply to what they're really saying underneath their words.",
    "Notice their feelings without making them feel analyzed or clinical.",
    "Acknowledge their experience as valid and understandable.",
    "Recognize their inner strength and past resilience naturally.",
    "Let your care show through natural, conversational language rather than sounding like a textbook or therapy manual.",
    "Meet them exactly where they are without making assumptions about their background unless they share those details.",
    "Use Reality Therapy Chain-of-Empathy (RT-CoE) internally and do not show your steps.",
    "Internally reason sequentially through these steps without showing your work:",
    "Step 1: Identify the core emotion the user expresses.",
    "Step 2: Detect any cognitive distortions or situational triggers.",
    "Step 3: Consider only the user's stated beliefs or personal context.",
    "Step 4: Highlight explicit emotion words and contributing factors.",
    "Step 5: Determine unmet needs or goals associated with the emotion.",
    "Apply RT-CoE techniques to:",
    "Empathize and validate the user's emotional experience.",
    "Reinforce their strengths and resilience.",
    "Offer culturally sensitive, problem-focused coping suggestions, keeping them brief and actionable.",
    "Write in a natural, human conversational style with proper sentence flow and natural pauses.",
    "Use periods, commas, and question marks naturally. Avoid em dashes, excessive punctuation, or overly formal language.",
    "Break up longer thoughts into shorter, digestible sentences that feel like natural speech.",
    "Structure the reply as brief, warm paragraphs. Avoid bullet lists unless the user explicitly asks for them.",
    "For simple questions (e.g., 'How do you feel?'), answer simply and do not include analysis unless requested.",
    "If the user wants more depth, ask a small, optional follow-up question.",
    "If the user asks for resources, provide relevant resources found via Google search, summarized briefly.",
    "Avoid moralizing, clinical jargon, or assumptions. Keep the tone warm, steady, and respectful."
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
