# vars.py is a file for storing global variables, lists, and dictionaries

API_KEY = '48a3fb6b1cd34f7b859d0e0d220c15d1'

MBTA_BASE_URL = "https://api-v3.mbta.com/"

SERVER_IP = "0.0.0.0"

ROUTE = "Green-E"
# curl -X GET "https://api-v3.mbta.com/routes/Green-E" -H "accept: application/vnd.api+json"

# API_FILTER = "filter%5Broute%5D=Green-C&filter%5Bdirection_id%5D=1"
API_FILTER = "filter%5Broute%5D=Green-C"

TOTAL_NUM_PIXELS = 35

STOP_LIST = [
    "place-hsmnl",
    "place-bckhl",
    "place-rvrwy",
    "place-mispk",
    "place-fenwd",
    "place-brmnl",
    "place-lngmd",
    "place-mfa",
    "place-nuniv",
    "place-symcl",
    "place-prmnl",
    "place-coecl",
    "place-armnl",
    "place-boyls",
    "place-pktrm",
    "place-gover",
    "place-haecl",
    "place-north",
    "place-spmnl",
    "place-lech",
    "place-esomr",
    "place-gilmn",
    "place-mgngl",
    "place-balsq",
    "place-mdftf"
]

ABBR_STOP_LIST = [
    "place-north",
    "place-spmnl",
    "place-lech",
    "place-esomr",
    "place-gilmn",
    "place-mgngl",
    "place-balsq",
    "place-mdftf"
]