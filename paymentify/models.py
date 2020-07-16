import attr


@attr.s(auto_attribs=True)
class Card:
    number: str
    exp_year: str
    exp_month: str
    cvc: str


@attr.s(auto_attribs=True)
class Charge:
    amount: int
    token: str
