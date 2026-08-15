"""Hotel and destination research tool backed by Tavily."""

import os
import re
from typing import List

from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

API_KEY = os.getenv("TAVILY_API_KEY")

client = (
    TavilyClient(api_key=API_KEY)
    if API_KEY
    else None
)


# Common destinations used in travel requests.
DESTINATIONS = [
    "paris",
    "tokyo",
    "osaka",
    "japan",
    "dubai",
    "singapore",
    "bali",
    "bangkok",
    "london",
    "new york",
    "los angeles",
    "san francisco",
    "rome",
    "barcelona",
    "amsterdam",
    "switzerland",
    "france",
]


def _extract_destination(query: str) -> str:
    """Extract the destination from a travel request."""

    query_lower = query.lower()

    # Prefer longer destination names first.
    for destination in sorted(
        DESTINATIONS,
        key=len,
        reverse=True,
    ):
        if re.search(
            rf"\b{re.escape(destination)}\b",
            query_lower,
        ):
            return destination

    return ""


def _clean_text(text: str, max_length: int = 500) -> str:
    """Clean and shorten Tavily result text."""

    if not text:
        return ""

    text = re.sub(r"\s+", " ", text).strip()

    if len(text) > max_length:
        text = (
            text[:max_length]
            .rsplit(" ", 1)[0]
            + "..."
        )

    return text


def _search(query: str, max_results: int = 5) -> List[dict]:
    """Execute a Tavily search safely."""

    if client is None:
        return []

    try:
        response = client.search(
            query=query,
            max_results=max_results,
            search_depth="advanced",
            include_answer=False,
        )

        return response.get("results", [])

    except Exception:
        return []


def tavily_search(query: str) -> str:
    """
    Research accommodation options for the requested destination.

    The function creates a hotel-focused Tavily query rather than
    performing a generic travel search.
    """

    if client is None:
        return (
            "Hotel research unavailable: "
            "set TAVILY_API_KEY in .env."
        )

    destination = _extract_destination(query)

    if not destination:

        return (
            "Hotel research could not determine the "
            "destination from the request.\n\n"
            f"User request: {query}"
        )

    # ---------------------------------------------------------
    # Hotel-focused search
    # ---------------------------------------------------------

    hotel_query = (
        f"best hotels in {destination} "
        f"for tourists accommodation "
        f"budget mid-range luxury "
        f"neighborhoods where to stay"
    )

    results = _search(
        hotel_query,
        max_results=8,
    )

    if not results:

        return (
            f"No hotel research results were returned "
            f"for {destination.title()}."
        )

    formatted_results = []

    for index, result in enumerate(
        results,
        start=1,
    ):

        title = result.get(
            "title",
            "Unknown",
        )

        url = result.get(
            "url",
            "",
        )

        content = _clean_text(
            result.get(
                "content",
                "",
            )
        )

        # -----------------------------------------------------
        # Ignore obviously irrelevant results.
        # -----------------------------------------------------

        combined_text = (
            f"{title} {content}"
        ).lower()

        irrelevant_terms = [
            "flight booking",
            "flight ticket",
            "airfare",
            "visa only",
        ]

        if any(
            term in combined_text
            for term in irrelevant_terms
        ):
            continue

        formatted_results.append(
            f"{index}. **{title}**\n"
            f"   Source: {url}\n"
            f"   {content}"
        )

    if not formatted_results:

        return (
            f"Tavily returned results for "
            f"{destination.title()}, but no useful "
            "hotel-focused results were found."
        )

    return (
        f"Hotel research for "
        f"**{destination.title()}**\n\n"
        + "\n\n".join(formatted_results[:5])
    )