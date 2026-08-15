"""Flight search tool backed by AviationStack."""

import os
import re

import requests
from dotenv import load_dotenv

try:
    import streamlit as st
except ImportError:
    st = None


load_dotenv()


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def get_api_key() -> str | None:
    """
    Load the AviationStack API key.

    Streamlit Cloud:
        Reads from st.secrets.

    Local development:
        Falls back to the .env / environment variable.
    """

    # Streamlit Cloud
    if st is not None:
        try:
            secrets = st.secrets

            if "AVIATIONSTACK_API_KEY" in secrets:
                value = secrets["AVIATIONSTACK_API_KEY"]

                if value:
                    return str(value)

        except Exception:
            # Local machine may not have Streamlit secrets configured.
            pass

    # Local .env / environment
    return os.getenv("AVIATIONSTACK_API_KEY")


API_KEY = get_api_key()

API_URL = "https://api.aviationstack.com/v1/flights"


# ---------------------------------------------------------------------------
# Origin cities / airports
# ---------------------------------------------------------------------------

ORIGIN_CODES = {
    "mumbai": ["BOM"],
    "bombay": ["BOM"],
    "delhi": ["DEL"],
    "new delhi": ["DEL"],
    "bangalore": ["BLR"],
    "bengaluru": ["BLR"],
    "hyderabad": ["HYD"],
    "chennai": ["MAA"],
    "kolkata": ["CCU"],
    "pune": ["PNQ"],
    "ahmedabad": ["AMD"],
    "goa": ["GOI"],
    "nagpur": ["NAG"],
}


# ---------------------------------------------------------------------------
# Destination cities / countries
# ---------------------------------------------------------------------------

DESTINATION_CODES = {
    "japan": ["NRT", "HND"],
    "tokyo": ["NRT", "HND"],
    "osaka": ["KIX"],
    "kyoto": ["KIX"],

    "france": ["CDG", "ORY"],
    "paris": ["CDG", "ORY"],

    "uae": ["DXB"],
    "dubai": ["DXB"],

    "singapore": ["SIN"],

    "thailand": ["BKK"],
    "bangkok": ["BKK"],

    "indonesia": ["DPS"],
    "bali": ["DPS"],
}


# ---------------------------------------------------------------------------
# Location helpers
# ---------------------------------------------------------------------------

def _find_location(text: str, locations: dict):
    """Find a location name mentioned in the user's query."""

    text = text.lower()

    for location in sorted(
        locations.keys(),
        key=len,
        reverse=True,
    ):
        if re.search(
            rf"\b{re.escape(location)}\b",
            text,
        ):
            return location, locations[location]

    return None, None


def _extract_route(query: str):
    """
    Extract origin and destination from natural-language travel requests.

    Examples:

        7-day Japan trip from Mumbai under ₹2L
        Mumbai to Tokyo trip
        5-day Paris trip from Delhi
        Dubai weekend trip from Mumbai
    """

    query_lower = query.lower()

    origin_name = None
    origin_codes = None

    destination_name = None
    destination_codes = None

    # ---------------------------------------------------------
    # 1. Look for "from Mumbai"
    # ---------------------------------------------------------

    from_match = re.search(
        r"\bfrom\s+([a-zA-Z][a-zA-Z\s]*?)(?=\s+(?:to|under|for|with|on|budget|trip|vacation)\b|$)",
        query_lower,
    )

    if from_match:
        origin_text = from_match.group(1).strip()

        for location in sorted(
            ORIGIN_CODES.keys(),
            key=len,
            reverse=True,
        ):
            if location in origin_text:
                origin_name = location
                origin_codes = ORIGIN_CODES[location]
                break

    # ---------------------------------------------------------
    # 2. Look for explicit "Mumbai to Tokyo"
    # ---------------------------------------------------------

    to_match = re.search(
        r"\bfrom\s+([a-zA-Z][a-zA-Z\s]*?)\s+to\s+([a-zA-Z][a-zA-Z\s]*?)(?=\s+(?:under|for|with|on|budget|trip|vacation)\b|$)",
        query_lower,
    )

    if to_match:

        origin_text = to_match.group(1).strip()
        destination_text = to_match.group(2).strip()

        for location in sorted(
            ORIGIN_CODES.keys(),
            key=len,
            reverse=True,
        ):
            if location in origin_text:
                origin_name = location
                origin_codes = ORIGIN_CODES[location]
                break

        for location in sorted(
            DESTINATION_CODES.keys(),
            key=len,
            reverse=True,
        ):
            if location in destination_text:
                destination_name = location
                destination_codes = DESTINATION_CODES[location]
                break

    # ---------------------------------------------------------
    # 3. Detect destination anywhere in the query.
    # ---------------------------------------------------------

    if not destination_codes:
        destination_name, destination_codes = _find_location(
            query_lower,
            DESTINATION_CODES,
        )

    # ---------------------------------------------------------
    # 4. Detect origin anywhere in the query.
    # ---------------------------------------------------------

    if not origin_codes:
        origin_name, origin_codes = _find_location(
            query_lower,
            ORIGIN_CODES,
        )

    return (
        origin_name,
        origin_codes,
        destination_name,
        destination_codes,
    )


# ---------------------------------------------------------------------------
# AviationStack API helper
# ---------------------------------------------------------------------------

def _search_api(params: dict):
    """Make an AviationStack request."""

    response = requests.get(
        API_URL,
        params=params,
        timeout=20,
    )

    response.raise_for_status()

    data = response.json()

    if data.get("error"):
        return []

    return data.get("data", [])


# ---------------------------------------------------------------------------
# Main Flight Search
# ---------------------------------------------------------------------------

def search_flights(query: str) -> str:
    """Search AviationStack using the route extracted from the request."""

    if not API_KEY:
        return (
            "Flight search unavailable: "
            "set AVIATIONSTACK_API_KEY in .env or Streamlit Secrets."
        )

    (
        origin_name,
        origin_codes,
        destination_name,
        destination_codes,
    ) = _extract_route(query)

    # ---------------------------------------------------------
    # We need at least a destination to perform a useful search.
    # ---------------------------------------------------------

    if not destination_codes:

        return (
            "Flight search could not determine the destination "
            "from the request.\n\n"
            f"User request: {query}\n\n"
            "Please specify a destination such as Japan, Tokyo, "
            "Paris, Dubai, or Singapore."
        )

    all_flights = []

    # ---------------------------------------------------------
    # Search each destination airport.
    # ---------------------------------------------------------

    for destination_code in destination_codes:

        params = {
            "access_key": API_KEY,
            "arr_iata": destination_code,
            "limit": 10,
        }

        if origin_codes:
            params["dep_iata"] = origin_codes[0]

        try:
            flights = _search_api(params)
            all_flights.extend(flights)

        except requests.HTTPError as exc:

            status = (
                exc.response.status_code
                if exc.response is not None
                else "unknown"
            )

            return (
                f"Flight search unavailable (HTTP {status}). "
                "Check AVIATIONSTACK_API_KEY."
            )

        except requests.RequestException as exc:

            return (
                "Flight search temporarily unavailable "
                "due to a network error.\n"
                f"Details: {exc}"
            )

    # ---------------------------------------------------------
    # Remove duplicate flights.
    # ---------------------------------------------------------

    unique_flights = []
    seen = set()

    for flight in all_flights:

        flight_id = (
            flight.get("flight", {}).get("iata")
            or flight.get("flight", {}).get("number")
            or str(flight)
        )

        if flight_id not in seen:
            seen.add(flight_id)
            unique_flights.append(flight)

    unique_flights = unique_flights[:10]

    # ---------------------------------------------------------
    # No results.
    # ---------------------------------------------------------

    if not unique_flights:

        route_text = ""

        if origin_name and destination_name:
            route_text = (
                f"{origin_name.title()} → "
                f"{destination_name.title()}"
            )

        elif destination_name:
            route_text = destination_name.title()

        return (
            f"No live flight records were returned for "
            f"{route_text}.\n\n"
            "This may happen because AviationStack's available "
            "live data does not contain the requested route."
        )

    # ---------------------------------------------------------
    # Format results.
    # ---------------------------------------------------------

    output = []

    if origin_name and destination_name:

        output.append(
            f"Route searched: "
            f"{origin_name.title()} → "
            f"{destination_name.title()}"
        )

    elif destination_name:

        output.append(
            f"Destination searched: "
            f"{destination_name.title()}"
        )

    output.append("")

    for flight in unique_flights:

        airline = (
            flight.get("airline", {}).get("name")
            or "Unknown airline"
        )

        departure = flight.get("departure", {}) or {}
        arrival = flight.get("arrival", {}) or {}
        flight_info = flight.get("flight", {}) or {}

        flight_number = (
            flight_info.get("iata")
            or flight_info.get("number")
            or "N/A"
        )

        departure_airport = (
            departure.get("airport")
            or "Unknown airport"
        )

        departure_iata = (
            departure.get("iata")
            or "N/A"
        )

        arrival_airport = (
            arrival.get("airport")
            or "Unknown airport"
        )

        arrival_iata = (
            arrival.get("iata")
            or "N/A"
        )

        departure_time = (
            departure.get("scheduled")
            or departure.get("estimated")
            or "N/A"
        )

        arrival_time = (
            arrival.get("scheduled")
            or arrival.get("estimated")
            or "N/A"
        )

        status = (
            flight.get("flight_status")
            or "Unknown"
        )

        output.append(
            f"Flight: {flight_number}\n"
            f"Airline: {airline}\n"
            f"Departure: {departure_airport} "
            f"({departure_iata})\n"
            f"Arrival: {arrival_airport} "
            f"({arrival_iata})\n"
            f"Departure time: {departure_time}\n"
            f"Arrival time: {arrival_time}\n"
            f"Status: {status}\n"
        )

    return "\n".join(output)