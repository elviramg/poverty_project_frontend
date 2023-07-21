import pandas as pd

def get_csv():
    labor_pov = pd.read_csv("data/Labor_Poverty.csv", index_col=0, parse_dates=True)
    labor_pov = labor_pov.replace({"ND": None})
    labor_pov = labor_pov.astype(float)

    # Dictionary to map Spanish month abbreviations to English abbreviations
    spanish_to_english_months = {
        "ene": "01",
        "feb": "02",
        "mar": "03",
        "abr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "ago": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dic": "12",
    }

    # Convert month abbreviations to the desired format "Jan-05", "Feb-05", etc.
    new_index = [spanish_to_english_months[month[:3]] + "-" + month[-2:] for month in labor_pov.index]
    labor_pov.index = pd.to_datetime(new_index, format="%m-%y")

    return labor_pov
