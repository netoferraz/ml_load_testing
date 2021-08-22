from mimesis.schema import Field, Schema
import random

# arbiratry bounding box for NYC
# http://bboxfinder.com/#40.543026,-74.084930,40.949825,-73.561707
MAX_NYC_LATITUDE = 40.949825
MIN_NYC_LATITUDE = 40.543026
MAX_NYC_LONGITUDE = -73.561707
MIN_NYC_LONGITUDE = -74.084930
_ = Field("en")
description = lambda: {
    "id": _("uuid"),
    "pickup_datetime": _(
        "datetime.formatted_datetime", fmt="%Y-%m-%d %H:%M:%S", start=2015
    ),
    "pickup_longitude": _(
        "numbers.float_number", start=MIN_NYC_LONGITUDE, end=MAX_NYC_LONGITUDE
    ),
    "pickup_latitude": _(
        "numbers.float_number", start=MIN_NYC_LATITUDE, end=MAX_NYC_LATITUDE
    ),
    "dropoff_longitude": _(
        "numbers.float_number", start=MIN_NYC_LONGITUDE, end=MAX_NYC_LONGITUDE
    ),
    "dropoff_latitude": _(
        "numbers.float_number", start=MIN_NYC_LATITUDE, end=MAX_NYC_LATITUDE
    ),
    "passenger_count": _(
        "numbers.float_number", start=MIN_NYC_LATITUDE, end=MAX_NYC_LATITUDE
    ),
    "passenger_count": _("numbers.integer_number", start=1, end=4),
}
schema = Schema(schema=description)


def gen_payload() -> dict:
    while True:
        yield schema.create(iterations=1)[0]


def gen_invalid_payload() -> dict:
    while True:
        payload = schema.create(iterations=1)[0]
        fields = list(payload.keys())
        field = random.choice(fields)
        del payload[field]
        yield payload
