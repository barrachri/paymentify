import attr


@attr.s(auto_attribs=True)
class Card:
    number: str
    exp_year: str
    exp_month: str
    cvc: str


@attr.s(auto_attribs=True)
class Charge:
    token: str
    amount: int
    currency: str = "eur"
