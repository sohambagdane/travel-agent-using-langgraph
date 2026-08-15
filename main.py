"""AI Travel Planner - LangGraph multi-agent workflow."""

import operator
import os
from typing import Annotated, TypedDict

import psycopg
from dotenv import load_dotenv
from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, START, StateGraph
from psycopg.rows import dict_row

from tools.flight_tool import search_flights
from tools.tavily_tool import tavily_search


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ---------------------------------------------------------------------------
# LLM
# ---------------------------------------------------------------------------

llm = (
    ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        api_key=GROQ_API_KEY,
    )
    if GROQ_API_KEY
    else None
)


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int


# ---------------------------------------------------------------------------
# LLM Helper
# ---------------------------------------------------------------------------

def generate_plan(
    messages: list[AnyMessage],
    fallback_content: str,
) -> AIMessage:
    """Generate an LLM response with a transparent fallback."""

    if llm is None:
        return AIMessage(content=fallback_content)

    try:
        return llm.invoke(messages)

    except Exception as exc:
        print(f"LLM request failed: {exc}")
        return AIMessage(content=fallback_content)


# ---------------------------------------------------------------------------
# Fallback Itinerary
# ---------------------------------------------------------------------------

def starter_itinerary(query: str) -> str:
    """Provide a useful fallback itinerary when the LLM is unavailable."""

    return f"""## Starter Travel Itinerary

**Your request:** {query}

### Day 1 — Arrival and orientation

- Check in near the main sightseeing area.
- Take a relaxed neighborhood walk.
- Choose a local restaurant for dinner.

### Day 2 — Main attractions

- Visit the destination's top attraction early.
- Reserve the afternoon for a museum, cultural site, or guided activity.

### Day 3 — Flexible experiences

- Explore a market, nature activity, or food tour.
- Keep a buffer for transport, shopping, and unexpected discoveries.

### Before booking

- Compare flights and verify schedules.
- Check hotel location, cancellation policy, and recent reviews.
- Confirm visa, weather, and local transportation requirements.

> This is a fallback plan because the AI service was unavailable.
"""


# ---------------------------------------------------------------------------
# Flight Agent
# ---------------------------------------------------------------------------

def flight_agent(state: TravelState) -> dict:
    """Retrieve flight information for the travel request."""

    query = state["user_query"]
    flight_data = search_flights(query)

    return {
        "flight_results": flight_data,
        "messages": [
            AIMessage(content="Flight search completed.")
        ],
        "llm_calls": state.get("llm_calls", 0),
    }


# ---------------------------------------------------------------------------
# Hotel Agent
# ---------------------------------------------------------------------------

def hotel_agent(state: TravelState) -> dict:
    """Research hotel information using Tavily."""

    query = (
        f"Best hotels and accommodation options for "
        f"{state['user_query']}"
    )

    hotel_results = tavily_search(query)

    return {
        "hotel_results": hotel_results,
        "messages": [
            AIMessage(content="Hotel research completed.")
        ],
        "llm_calls": state.get("llm_calls", 0),
    }


# ---------------------------------------------------------------------------
# Itinerary Agent
# ---------------------------------------------------------------------------

def itinerary_agent(state: TravelState) -> dict:
    """Create an itinerary using collected travel information."""

    prompt = f"""
Create a practical travel itinerary based on the following information.

User request:
{state["user_query"]}

Flight information:
{state["flight_results"]}

Hotel information:
{state["hotel_results"]}

Include:

- Day-by-day activities
- Travel considerations
- Accommodation considerations
- Practical booking advice
- Important assumptions or limitations

Do not invent specific prices or availability when the supplied
data does not contain them.
"""

    response = generate_plan(
        [
            SystemMessage(
                content=(
                    "You are an expert travel planner. "
                    "Use the supplied research and clearly distinguish "
                    "known information from recommendations. "
                    "Never claim that live prices or availability are "
                    "guaranteed unless explicitly provided."
                )
            ),
            HumanMessage(content=prompt),
        ],
        starter_itinerary(state["user_query"]),
    )

    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": (
            state.get("llm_calls", 0)
            + (1 if llm else 0)
        ),
    }


# ---------------------------------------------------------------------------
# Final Agent
# ---------------------------------------------------------------------------

def final_agent(state: TravelState) -> dict:
    """Synthesize research and itinerary into the final response."""

    final_prompt = f"""
Create a concise and useful final travel plan.

User request:
{state["user_query"]}

Flight research:
{state["flight_results"]}

Hotel research:
{state["hotel_results"]}

Generated itinerary:
{state["itinerary"]}

Present the final answer clearly using headings and bullet points.

Include:
- Flight information
- Hotel/accommodation recommendations
- Day-by-day itinerary
- Practical travel advice
- Important limitations

Do not claim that live availability or prices are guaranteed.
Do not invent information that is not present in the supplied research.
"""

    response = generate_plan(
        [
            SystemMessage(
                content=(
                    "You are a professional travel assistant. "
                    "Create a clear, accurate and practical final "
                    "travel plan from the supplied information."
                )
            ),
            HumanMessage(content=final_prompt),
        ],
        state["itinerary"],
    )

    return {
        "messages": [response],
        "llm_calls": (
            state.get("llm_calls", 0)
            + (1 if llm else 0)
        ),
    }


# ---------------------------------------------------------------------------
# LangGraph Workflow
# ---------------------------------------------------------------------------

def build_graph() -> StateGraph:
    """Build the sequential multi-agent travel workflow."""

    workflow = StateGraph(TravelState)

    workflow.add_node("flight_agent", flight_agent)
    workflow.add_node("hotel_agent", hotel_agent)
    workflow.add_node("itinerary_agent", itinerary_agent)
    workflow.add_node("final_agent", final_agent)

    workflow.add_edge(START, "flight_agent")
    workflow.add_edge("flight_agent", "hotel_agent")
    workflow.add_edge("hotel_agent", "itinerary_agent")
    workflow.add_edge("itinerary_agent", "final_agent")
    workflow.add_edge("final_agent", END)

    return workflow


# ---------------------------------------------------------------------------
# PostgreSQL Checkpointer
# ---------------------------------------------------------------------------

def create_checkpointer():
    """
    Create a PostgreSQL-backed LangGraph checkpointer.

    PostgreSQL is used for persistent conversation history.
    If PostgreSQL is unavailable, the application falls back
    to in-memory storage so the UI can still start.
    """

    if not DATABASE_URL:
        print("DATABASE_URL not configured.")
        return (
            InMemorySaver(),
            "In-memory (set DATABASE_URL for persistence)",
        )

    try:
        connection = psycopg.connect(
            DATABASE_URL,
            autocommit=True,
            row_factory=dict_row,
        )

        checkpointer = PostgresSaver(connection)

        # Create LangGraph checkpoint tables if they do not exist.
        checkpointer.setup()

        print("PostgreSQL checkpointer connected successfully.")

        return (
            checkpointer,
            "PostgreSQL (persistent history enabled)",
        )

    except Exception as exc:
        print(
            "PostgreSQL checkpointer unavailable. "
            f"Falling back to memory.\nReason: {exc}"
        )

        return (
            InMemorySaver(),
            "In-memory (PostgreSQL connection unavailable)",
        )


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

graph = build_graph()

checkpointer, storage_mode = create_checkpointer()

app = graph.compile(
    checkpointer=checkpointer
)


# ---------------------------------------------------------------------------
# Local CLI Test
# ---------------------------------------------------------------------------

if __name__ == "__main__":

    user_input = input(
        "Enter travel request: "
    ).strip()

    if not user_input:
        raise SystemExit(
            "Please enter a travel request."
        )

    result = app.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "user_query": user_input,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0,
        },
        config={
            "configurable": {
                "thread_id": "soham_user"
            }
        },
    )

    print("\n" + "=" * 60)
    print("FINAL TRAVEL PLAN")
    print("=" * 60 + "\n")

    print(
        result["messages"][-1].content
    )