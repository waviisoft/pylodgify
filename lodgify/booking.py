from datetime import date


class Channel:
    name: str
    id: str

    def __init__(self, name: str, id: str):
        self.name = name
        self.id = id


class Booking:
    channelids: dict[str, str]
    source: str
    rentalid: str
    arrival: date
    departure: date
    rent: float
    fees: float
    promotions: float
    addons: float
    guestname: str
    nightsstayed: int
    gross: float

    def __init__(
        self,
        source: str,
        channelids: dict[str, str],
        rentalid: str,
        arrival: date,
        departure: date,
        rent: float,
        fees: float,
        promotions: float,
        addons: float,
        guestname: str,
    ):
        self.source = source
        self.channelids = channelids
        self.rentalid = rentalid
        self.arrival = arrival
        self.departure = departure
        self.rent = rent
        self.fees = fees
        self.promotions = promotions
        self.addons = addons
        self.guestname = guestname
        self.nightsstayed = (departure - arrival).days
        self._calcgross()

    def addpromotion(self, amount: float):
        self.promotions += amount
        self._calcgross()

    def _calcgross(self):
        self.gross = self.rent + self.fees + self.promotions + self.addons

    def __str__(self):
        return (
            f"Rental: {self.rentalid} - Source: {self.source}\n"
            f"Guest: {self.guestname}\n"
            f"IDs: {self.channelids}\n"
            f"{self.arrival} - {self.departure}\n"
            f"Rent: {self.rent}, Fees: {self.fees}, Promotions: {self.promotions}, addons: {self.addons}"
        )


class PeriodBooking:
    booking: Booking
    nightsstayed: int
    bookingendedinperiod: bool
    rent: float
    fees: float
    addons: float
    promotions: float
    gross: float

    def __init__(
        self,
        booking: Booking,
        nightsstayed: int,
        bookingendedinperiod: bool,
        rent: float,
        fees: float,
        addons: float,
        promotions: float,
    ):
        self.booking = booking
        self.nightsstayed = nightsstayed
        self.bookingendedinperiod = bookingendedinperiod
        self.rent = rent
        self.fees = fees
        self.addons = addons
        self.promotions = promotions
        self._calcgross()

    def _calcgross(self):
        self.gross = self.rent + self.fees + self.promotions + self.addons
