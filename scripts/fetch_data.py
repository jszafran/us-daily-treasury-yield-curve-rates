import requests
from simple_settings import settings

URL = (
    "http://data.treasury.gov/feed.svc/"
    "DailyTreasuryYieldCurveRateData?$filter=year(NEW_DATE)%20eq%20{year}"
)
REQUEST_TIMEOUT = 2


def main():
    # TODO: argparse arguments handling for settings years range
    years = range(2021, 2021)

    for year in years:
        url = URL.format(year=year)

        # TODO: add try except for catching unreliable network exceptions
        response = requests.get(url, timeout=REQUEST_TIMEOUT)

        with open(settings.RAW_CURVES_DATA_DIR / f"{year}.xml", "wt") as f:
            f.write(response.text)
            print(f"{year} fetched.")


if __name__ == "__main__":
    main()
