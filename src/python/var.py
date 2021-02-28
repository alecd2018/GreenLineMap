# vars.py is a file for storing global variables, lists, and dictionaries

API_KEY = '48a3fb6b1cd34f7b859d0e0d220c15d1'

MBTA_BASE_URL = "https://api-v3.mbta.com/"

SERVER_IP = "localhost"
PORT=8080

LINE_LIST = [
    "Red",
    "Mattapan",
    "Blue",
    "Orange",
    "Green-B",
    "Green-C",
    "Green-D",
    "Green-E"
]

TOTAL_NUM_PIXELS = 120

GREEN_C_STOP_LIST = [
    'place-clmnl',
    'place-engav',
    'place-denrd',
    'place-tapst',
    'place-bcnwa',
    'place-fbkst',
    'place-bndhl',
    'place-sumav',
    'place-cool',
    'place-stpul',
    'place-kntst',
    'place-hwsst',
    'place-smary',
    'place-kencl',
    'place-hymnl',
    'place-coecl',
    'place-armnl',
    'place-boyls',
    'place-pktrm',
    'place-gover',
    'place-haecl',
    'place-north'
]

ABBR_STOP_LIST = GREEN_C_STOP_LIST
LED_ROUTE = "Green-C"