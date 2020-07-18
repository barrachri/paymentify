CardResourceRequest = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://example.com/product.schema.json",
    "title": "Card",
    "description": "Tokenise endpoint schema",
    "type": "object",
    "properties": {
        "number": {
            "description": "The card number you want to tokenisem with no hyphens",  # noqa: E501
            "type": "string",
            # digits 2 or 4 chars long
            "pattern": "^[\\d]{12,19}$",
        },
        "exp_month": {
            "description": "Month expiry of the card, either single or double digit",  # noqa: E501
            "type": "string",
            # digits 2 or 4 chars long
            "pattern": "^[\\d]{1,2}$",
            "minLength": 1,
            "maxLength": 2,
        },
        "exp_year": {
            "description": "Year expiry of the card, either double or 4 digit",
            "type": "string",
            # digits 2 or 4 chars long
            "pattern": "^[\\d]{2,4}$",
        },
        "cvc": {
            "description": "The cvc of the card",
            "type": "string",
            # digits 3 or 4 chars long
            "pattern": "^[\\d]{3,4}$",
        },
    },
    "additionalProperties": False,
    "required": ["number", "exp_month", "exp_year", "cvc"],
}


SaleResourceSchema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://example.com/product.schema.json",
    "title": "Sale",
    "description": "Sale endpoint schema",
    "type": "object",
    "properties": {
        "token": {
            "description": "The token (credit card) you want to charge",
            "type": "string",
            "minLength": 1,
        },
        "amount": {
            "description": "The amount you want to charge, expressed as zero-decimal currency ($1.00 is equal to 100)",  # noqa: E501
            "type": "integer",
        },
    },
    "additionalProperties": False,
    "required": ["token", "amount"],
}