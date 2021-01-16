import datetime
from typing import List

import bs4
import pandas as pd
from simple_settings import settings

TENORS = [
    "BC_1MONTH",
    "BC_2MONTH",
    "BC_3MONTH",
    "BC_6MONTH",
    "BC_1YEAR",
    "BC_2YEAR",
    "BC_3YEAR",
    "BC_5YEAR",
    "BC_7YEAR",
    "BC_10YEAR",
    "BC_20YEAR",
    "BC_30YEAR",
]


def parse_xml_row(xml_tag: bs4.element.Tag) -> List:
    date = datetime.datetime.strptime(
        xml_tag.content.NEW_DATE.text[:10], "%Y-%m-%d"
    ).date()
    curve_data = [
        float(getattr(xml_tag.content, tenor).text)
        if getattr(xml_tag.content, tenor).text
        else float("nan")
        for tenor in TENORS
    ]
    return [date] + curve_data


def parse_xml_data() -> None:
    year = 2019
    with open(settings.RAW_CURVES_DATA_DIR / f"{year}.xml", "rt") as f:
        xml_data = f.read()

    soup = bs4.BeautifulSoup(xml_data, "xml")

    parsed_rows = [parse_xml_row(row) for row in soup.find_all("entry")]

    df = pd.DataFrame(
        columns=[
            "date",
            "1m",
            "2m",
            "3m",
            "6m",
            "1y",
            "2y",
            "3y",
            "5y",
            "7y",
            "10y",
            "20y",
            "30y",
        ],
        data=parsed_rows,
    )

    df.set_index("date", inplace=True)


if __name__ == "__main__":
    parse_xml_data()
