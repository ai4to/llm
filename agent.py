
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
from os import getenv
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.tools.reasoning import ReasoningTools
from agno.agent import Agent, RunResponse
from agno.models.openai.like import OpenAILike


memory = Memory(
    model=OpenAILike(
        id="qwen/qwen3-235b-a22b-thinking-2507",
        api_key=getenv("OPENAI_API_KEY"),
        base_url="https://openrouter.ai/api/v1"),
    # Store memories in a SQLite database
    db=SqliteMemoryDb(table_name="user_memories", db_file="tmp/agent.db"),
)

agent = Agent(
    model=OpenAILike(
        id="qwen/qwen3-235b-a22b-thinking-2507",
        api_key=getenv("OPENAI_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        max_tokens=5000,
    ), 
    tools=[
        ReasoningTools(add_instructions=True)],
    user_id="ava",
    instructions = [
    "Use Reality Therapy Chain‑of‑Empathy (RT‑CoE) to interpret the user's emotional and situational context.",
    "Within <analysis>, sequentially perform:",
        "Step 1: Identify the core emotion the user expresses.",
        "Step 2: Detect any cognitive distortions or situational triggers.",
        "Step 3: Uncover the user's underlying beliefs or personal context.",
        "Step 4: Highlight explicit emotion words and contributing factors.",
        "Step 5: Determine unmet needs or goals associated with the emotion.",
    "Within <reply>, apply RT‑CoE techniques to:",
        "Empathize and validate the user's emotional experience.",
        "Reinforce their strengths and resilience.",
        "Offer culturally sensitive, problem‑focused coping suggestions.",
    "Structure the reply as brief, warm paragraphs with no bullet lists.",
    "Wrap the full output in <answer> and </answer> tags.",
    "Return only the <reply> portion to the user; keep the <analysis> internal."
],
    memory=memory,
    # Let the Agent manage its memories
    enable_agentic_memory=True,
    markdown=True,
)


# Print the response in the terminal
if __name__ == "__main__":
    # This will create a memory that ava struggles with depression
    agent.print_response(
        "I was recently diagnosed with breast cancer, and I feel so lost. I’m exhausted from treatment and I feel like I’ve let my family down. I don’t speak English well, so I’m worried I can’t advocate for my needs, and I feel isolated because I don’t have family nearby. How can I cope with these feelings and stay strong for my children?",
        stream=True,
        show_full_reasoning=True,
        stream_intermediate_steps=True,
    )
    # This will use the memory to answer the question
    agent.print_response(
        "Can you help me?",
        stream=True,
        show_full_reasoning=True,
        stream_intermediate_steps=True,
    )