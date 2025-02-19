import os
from fastapi import FastAPI, Query
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Mock flight response data
MOCK_FLIGHT_RESPONSE = {
    "flights": [
        {
            "flightNumber": "ET608",
            "airline": "Ethiopian Airlines",
            "departure": "NBO",
            "arrival": "KUL",
            "departureTime": "2025-02-15T16:00:00",
            "arrivalTime": "2025-02-15T23:45:00",
            "price": 690.00,
            "currency": "USD",
            "duration": "11h 45m",
            "stops": 1
        },
        {
            "flightNumber": "KQ101",
            "airline": "Kenya Airways",
            "departure": "NBO",
            "arrival": "KUL",
            "departureTime": "2025-02-15T10:00:00",
            "arrivalTime": "2025-02-15T22:00:00",
            "price": 750.00,
            "currency": "USD",
            "duration": "12h 00m",
            "stops": 0
        },
        {
            "flightNumber": "MH701",
            "airline": "Malaysia Airlines",
            "departure": "NBO",
            "arrival": "KUL",
            "departureTime": "2025-02-15T18:00:00",
            "arrivalTime": "2025-02-16T06:00:00",
            "price": 770.00,
            "currency": "USD",
            "duration": "12h 00m",
            "stops": 0
        },
        {
            "flightNumber": "ET609",
            "airline": "Ethiopian Airlines",
            "departure": "KUL",
            "arrival": "NBO",
            "departureTime": "2025-02-20T23:45:00",
            "arrivalTime": "2025-02-21T06:30:00",
            "price": 700.00,
            "currency": "USD",
            "duration": "11h 45m",
            "stops": 1
        },
        {
            "flightNumber": "KQ102",
            "airline": "Kenya Airways",
            "departure": "KUL",
            "arrival": "NBO",
            "departureTime": "2025-02-20T22:00:00",
            "arrivalTime": "2025-02-21T10:00:00",
            "price": 760.00,
            "currency": "USD",
            "duration": "12h 00m",
            "stops": 0
        },
        {
            "flightNumber": "MH702",
            "airline": "Malaysia Airlines",
            "departure": "KUL",
            "arrival": "NBO",
            "departureTime": "2025-02-20T20:00:00",
            "arrivalTime": "2025-02-21T08:00:00",
            "price": 780.00,
            "currency": "USD",
            "duration": "12h 00m",
            "stops": 0
        },
           {   
            "flightNumber": "AI504",
            "airline": "Air India",
            "departure": "DXB",
            "arrival": "BOM",
            "departureTime": "2025-03-15T10:00:00",
            "arrivalTime": "2025-03-15T14:30:00",
            "price": 430.00,
            "currency": "USD",
            "duration": "4h 30m",
            "stops": 0
        },
        {
            "flightNumber": "QR302",
            "airline": "Qatar Airways",
            "departure": "DXB",
            "arrival": "BOM",
            "departureTime": "2025-03-15T16:00:00",
            "arrivalTime": "2025-03-15T20:30:00",
            "price": 460.00,
            "currency": "USD",
            "duration": "4h 30m",
            "stops": 0
        },
        {
           "flightNumber": "6E112",
           "airline": "IndiGo",
           "departure": "DXB",
           "arrival": "BOM",
           "departureTime": "2025-03-15T18:00:00",
           "arrivalTime": "2025-03-15T22:30:00",
           "price": 410.00,
           "currency": "USD",
           "duration": "4h 30m",
           "stops": 0
        },
        {
           "flightNumber": "AI505",
           "airline": "Air India",
           "departure": "BOM",
           "arrival": "DXB",
           "departureTime": "2025-03-20T10:00:00",
           "arrivalTime": "2025-03-20T14:30:00",
           "price": 430.00,
           "currency": "USD",
           "duration": "4h 30m",
           "stops": 0
        },
        {
           "flightNumber": "QR303",
           "airline": "Qatar Airways",
           "departure": "BOM",
           "arrival": "DXB",
           "departureTime": "2025-03-20T16:00:00",
           "arrivalTime": "2025-03-20T20:30:00",
           "price": 460.00,
           "currency": "USD",
           "duration": "4h 30m",
           "stops": 0
       },
       {
           "flightNumber": "6E113",
           "airline": "IndiGo",
           "departure": "BOM",
           "arrival": "DXB",
           "departureTime": "2025-03-20T18:00:00",
           "arrivalTime": "2025-03-20T22:30:00",
           "price": 410.00,
           "currency": "USD",
           "duration": "4h 30m",
           "stops": 0
      }

    ],
    "source": "Mock API"
}

@app.get("/search-flights")
async def search_flights(
    origin: str = Query(..., description="Origin airport code"),
    destination: str = Query(..., description="Destination airport code"),
    departure_date: str = Query(..., description="Departure date (YYYY-MM-DD)"),
    return_date: str = Query(None, description="Return date (YYYY-MM-DD), optional")
):
    """
    Handles flight search requests and filters results based on user input.
    Supports both one-way and round-trip flight searches.
    """
    try:
        print(f"🔹 Searching flights from {origin} to {destination} on {departure_date}")
        if return_date:
            print(f"🔹 Searching return flights from {destination} to {origin} on {return_date}")

        # Filter outbound flights (origin -> destination)
        outbound_flights = [
            flight for flight in MOCK_FLIGHT_RESPONSE["flights"]
            if flight["departure"] == origin and flight["arrival"] == destination
        ]

        # Filter return flights (destination -> origin) if return_date is provided
        return_flights = []
        if return_date:
            return_flights = [
                flight for flight in MOCK_FLIGHT_RESPONSE["flights"]
                if flight["departure"] == destination and flight["arrival"] == origin
            ]

        # If no outbound flights found
        if not outbound_flights:
            return {"message": f"No outbound flights found from {origin} to {destination} on {departure_date}."}

        # If return date is provided but no return flights found
        if return_date and not return_flights:
            return {"message": f"No return flights found from {destination} to {origin} on {return_date}."}

        # Sort outbound and return flights by price (cheapest first)
        outbound_flights.sort(key=lambda x: x["price"])
        return_flights.sort(key=lambda x: x["price"])

        # Build response
        response = {
            "outbound_flights": outbound_flights,
            "source": "Mock API"
        }
        if return_flights:
            response["return_flights"] = return_flights

        return response

    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": "Internal server error", "details": str(e)}
