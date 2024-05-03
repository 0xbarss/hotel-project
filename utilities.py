import re
import pandas as pd

HEADERS =  {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}
URL = "https://www.booking.com/searchresults.html?ss={}&ssne={}&ssne_untouched={}&efdco=1&label=gen173nr-1FCAEoggI46AdIM1gEaOQBiAEBmAExuAEHyAEP2AEB6AEBAECiAIBqAIDuAKo8sKxBsACAdICJGZlZWVmNGJjLWI2OGEtNGM0OS05ODk0LTM2ZGQ4YzkxYzY0MNgCBeACAQ&aid=304142&lang=en-us&sb=1&src_elem=sb&src=index&dest_id={}&dest_type=city&checkin={}&checkout={}&group_adults=2&no_rooms=1&group_children=0"

HOTEL_SCRAPING_COUNT = 10
HOTEL_VIEW_COUNT = 5

FILE = "hotelList.csv"
TITLE = "Hotel Title"
ADDRESS = "Hotel Address"
DISTANCE = "Distance to City Center/Downtown"
RATING = "Hotel Rating"
PRICE = "Price"
NOTGIVEN = "NOT GIVEN"

TL = "TL"
EU = "Euro"

WARNING_MESSAGE = "Please enter dates in 'YYYY-MM-DD' format!!"

CITIES = {"London": "-2601889", "Paris": "-1456928", "Berlin": "-1746443", "Valencia": "-406131", "Sevilla": "-402849", "Edinburgh": "-2595386", "Manchester": "-2602512", "Munich": "-1829149", "Cologne": "-1810561", "Hamburg": "-1785434", "Nice": "-1454990", "Lyon": "-1448468"}

def isDate(date: str):
    pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    return True if re.match(pattern, date) else False

def sortHotelData(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values(by=[PRICE])

def createCSVFile(df: pd.DataFrame):
    df.to_csv(FILE, header=True, index=False)