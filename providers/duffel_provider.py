import os
import requests
from dotenv import load_dotenv


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

DUFFEL_API_KEY = os.getenv("DUFFEL_API_KEY")

BASE_URL = "https://api.duffel.com"


# ============================================================
# DUFFEL PROVIDER
# ============================================================

class DuffelProvider:

    def __init__(self):

        if not DUFFEL_API_KEY:
            raise RuntimeError(
                "DUFFEL_API_KEY is missing. "
                "Check your .env file."
            )

        self.headers = {
            "Authorization": f"Bearer {DUFFEL_API_KEY}",
            "Duffel-Version": "v2",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }


    # ========================================================
    # TEST CONNECTION
    # ========================================================

    def test_connection(self):

        url = f"{BASE_URL}/air/offer_requests"

        params = {
            "limit": 1
        }

        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            timeout=30
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"Duffel API error "
                f"{response.status_code}: "
                f"{response.text}"
            )

        return response.json()


    # ========================================================
    # SEARCH FLIGHTS
    # ========================================================

    def search_flights(
        self,
        origin,
        destination,
        departure_date,
        passengers=1,
        cabin_class="economy",
    ):

        url = f"{BASE_URL}/air/offer_requests"

        passenger_list = [
            {
                "type": "adult"
            }
            for _ in range(passengers)
        ]

        payload = {
            "data": {
                "slices": [
                    {
                        "origin": origin.upper(),
                        "destination": destination.upper(),
                        "departure_date": departure_date,
                    }
                ],
                "passengers": passenger_list,
                "cabin_class": cabin_class,
            }
        }

        response = requests.post(
            url,
            headers=self.headers,
            json=payload,
            timeout=60
        )

        if response.status_code not in (200, 201):

            raise RuntimeError(
                f"Duffel flight search failed "
                f"{response.status_code}: "
                f"{response.text}"
            )

        return response.json()


# ============================================================
# FIRST AEROFIND FLIGHT SEARCH
# ============================================================

if __name__ == "__main__":

    print()
    print("✈️ AeroFind — First Flight Search")
    print("=" * 60)

    try:

        provider = DuffelProvider()

        print()
        print("Searching:")
        print("From:        HYD")
        print("To:          DXB")
        print("Date:        17 November 2026")
        print("Passengers:  1 Adult")
        print("Cabin:       Economy")
        print()

        result = provider.search_flights(
            origin="HYD",
            destination="DXB",
            departure_date="2026-11-17",
            passengers=1,
            cabin_class="economy",
        )

        data = result.get("data", {})

        print("✅ Flight search request successful!")
        print()

        print(f"Offer Request ID: {data.get('id')}")
        print(f"Live Mode:        {data.get('live_mode')}")

        offers = data.get("offers", [])

        print(f"Offers Returned:  {len(offers)}")
        print()

        if offers:

            print("🎉 AeroFind received flight offers!")
            print()

            for index, offer in enumerate(offers[:5], start=1):

                print(f"--- Offer {index} ---")

                print(
                    "Offer ID:",
                    offer.get("id")
                )

                print(
                    "Total:",
                    offer.get("total_amount"),
                    offer.get("total_currency")
                )

                print()

        else:

            print(
                "⚠️ No offers were returned."
            )

            print(
                "This can happen in Duffel test mode."
            )

        print()
        print("=" * 60)
        print("🎉 AeroFind ↔ Duffel search test completed.")

    except Exception as error:

        print()
        print("❌ Flight search failed.")
        print()
        print(f"Error: {error}")                          