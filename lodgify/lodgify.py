from enum import Enum
import datetime
import json
import requests
from .booking import Booking


class LodgifyBooking(Booking):
    CHANNEL = "lodgify"

    def __init__(self, lodgifybooking):
        id = str(lodgifybooking["id"])
        channelids = {LodgifyBooking.CHANNEL: id}
        source: str
        if lodgifybooking["source"] == "AirbnbIntegration":
            sourcejson = json.loads(lodgifybooking["source_text"])
            channelids["airbnb"] = sourcejson["confirmationCode"]
            source = "airbnb"
        elif lodgifybooking["source"] == "HomeAway":
            channelids["vrbo"] = id
            source = "vrbo"
        elif lodgifybooking["source"] == "Manual":
            source = "manual"
        elif lodgifybooking["source"] == "OH":
            source = "website"
        else:
            raise ValueError("unrecognized source", lodgifybooking["source"])
        rentalid = str(lodgifybooking["property_id"])
        rent = lodgifybooking["subtotals"]["stay"]
        fees = lodgifybooking["subtotals"]["fees"]
        addons = lodgifybooking["subtotals"]["addons"]
        promotions = lodgifybooking["subtotals"]["promotions"]
        arrival = datetime.date.fromisoformat(lodgifybooking["arrival"])
        departure = datetime.date.fromisoformat(lodgifybooking["departure"])
        guestname = lodgifybooking["guest"]["name"]
        super().__init__(
            source=source,
            channelids=channelids,
            rentalid=rentalid,
            arrival=arrival,
            departure=departure,
            rent=rent,
            fees=fees,
            promotions=promotions,
            addons=addons,
            guestname=guestname,
        )

    def __str__(self):
        return super().__str__()


class StayFilter(Enum):
    UPCOMING = "Upcoming"
    CURRENT = "Current"
    HISTORIC = "Historic"
    ALL = "All"
    ARRIVAL_DATE = "ArrivalDate"
    DEPARTURE_DATE = "DepartureDate"


def to_json_bool(value: bool):
    return "true" if value else "false"


class Lodgify:
    DEFAULT_HOST = "https://api.lodgify.com"

    api_key: str
    host: str

    def __init__(self, api_key: str, host = DEFAULT_HOST):
        self.api_key = api_key
        self.host = host

    def fetch_bookings(
        self,
        stay_filter: StayFilter,
        page=1,
        size=50,
        include_transactions=True,
        include_quote_details=True,
    ):
        params = {
            "page": page,
            "size": size,
            "includeTransactions": to_json_bool(include_transactions),
            "includeQuoteDetails": to_json_bool(include_quote_details),
            "stayFilter": stay_filter.value,
        }
        headers = {"X-ApiKey": self.api_key, "AcceptType": "application/json"}
        response = requests.get(
            f"{Lodgify.DEFAULT_HOST}/v2/reservations/bookings",
            params=params,
            headers=headers,
            timeout=60,
        )
        data = response.json()
        items = data["items"]
        bookings = list(items)
        if len(items) == size:
            return bookings + self.fetch_bookings(stay_filter, page + 1)
        return bookings
