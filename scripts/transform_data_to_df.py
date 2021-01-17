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

DF_COLUMNS = [
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
]


def parse_xml_row(xml_tag: bs4.element.Tag) -> List:
    """
    :param xml_tag: Tag representing a single entry in XML file.
    Contains curve data for one specific day.
    :return: List containing parsed data and curve data values.
    """
    date = datetime.datetime.strptime(
        xml_tag.content.NEW_DATE.text[:10], "%Y-%m-%d"
    ).date()
    # TODO: check if there's better way to access tag attribute with variable
    curve_data = [
        float(getattr(xml_tag.content, tenor).text)
        if getattr(xml_tag.content, tenor).text
        else float("nan")
        for tenor in TENORS
    ]
    return [date] + curve_data


def parse_xml_data() -> None:
    year_from = 1990
    year_until = 2020
    dfs = []

    for year in range(year_from, year_until + 1):
        with open(settings.RAW_CURVES_DATA_DIR / f"{year}.xml", "rt") as f:
            xml_data = f.read()

        soup = bs4.BeautifulSoup(xml_data, "xml")

        parsed_rows = [parse_xml_row(row) for row in soup.find_all("entry")]

        df = pd.DataFrame(
            columns=DF_COLUMNS,
            data=parsed_rows,
        )

        dfs.append(df)
        print(f"Year {year} done.")

    # post-merge processing
    all_years_df = pd.concat(dfs, axis=0)
    all_years_df.set_index("date", inplace=True)
    all_years_df.sort_index(inplace=True)

    years_range_str = f"{year_from}-{year_until}"
    print(f"Year(s) {years_range_str} parsed successfully.")

    all_years_df.to_csv(
        settings.PARSED_DATA_DIR / f"{years_range_str}.csv",
        index=True,
    )


if __name__ == "__main__":
    parse_xml_data()
