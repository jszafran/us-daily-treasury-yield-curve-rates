import sys
from typing import Optional

import requests
from simple_settings import settings

URL = (
    "http://data.treasury.gov/feed.svc/"
    "DailyTreasuryYieldCurveRateData?$filter=year(NEW_DATE)%20eq%20{year}"
)
REQUEST_TIMEOUT = 2


def main(year_start_: int, year_end_: Optional[int] = None):
    if not year_end_:
        year_end_ = year_start_ + 1

    years = range(year_start_, year_end_)

    for year in years:
        url = URL.format(year=year)

        # TODO: add try except for catching unreliable network exceptions
        response = requests.get(url, timeout=REQUEST_TIMEOUT)

        with open(settings.RAW_CURVES_DATA_DIR / f"{year}.xml", "wt") as f:
            f.write(response.text)
            print(f"{year} fetched.")


if __name__ == "__main__":
    # TODO: Think about switching to argparse?
    try:
        year_start = int(sys.argv[1])
    except IndexError:
        print("Please provide year to be fetched. Quitting script.")
        sys.exit(1)
    except ValueError:
        print(f"Parsing {sys.argv[1]} val to int failed. Quitting script.")
        sys.exit(1)

    try:
        year_end = int(sys.argv[2])
    except IndexError:
        year_end = None
    except ValueError:
        print(f"Parsing {sys.argv[2]} val to int failed. Quitting script.")
        sys.exit(1)

    main(year_start, year_end)
