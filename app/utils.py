import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from datetime import datetime

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

def get_model_csv():
    model_pred = pd.read_csv("output/model_prediction.csv", index_col=0).transpose()
    new_index = list(model_pred.index)
    model_pred.index = pd.to_datetime(new_index, format="%m-%Y")
    return model_pred

def yearly_rankings(data, start_year=2005, end_year=2023):
    """"THIS FUNCTION RETURNS A DATAFRAME WITH THE YEARLY RANKINGS OF POVERTY BY STATE (% OF PEOPLE IN LABOR POVERTY)
    OVER A SELECTED RANGE OF YEARS (FIRST PLACE HAS HIGHEST RATE, LAST PLACE HAS LOWEST.)"""
    rank_df = None
    years = [i for i in range(start_year, end_year + 1)]
    df_start = (start_year - 2005) * 4
    df_end = (end_year - 2005) * 4
    if 2023 in years:
        df_end = 72
    start = df_start
    for i in range((df_end - df_start) // 4 + 1):
        end = start + 4
        batch = data.iloc[start:end,:].mean().sort_values()
        rank_series = pd.Series([i + 1 for i in range(len(batch))], index=batch.index).sort_index()
        if rank_df is None:
            rank_df = pd.DataFrame(rank_series).T
        else:
            rank_df.loc[i] = rank_series.to_dict().values()
        start += 4
        if end >= 72:
            break
    if 2023 in years:
        batch_2023 = data.iloc[df_end,:].sort_values(ascending=False)
        rank_2023 = pd.Series([i + 1 for i in range(len(batch_2023))], index=batch_2023.index).sort_index()
        rank_df.loc[len(rank_df)] = rank_2023.to_dict().values()
    rank_df.index = years
    return rank_df

def get_recovery_graph(recovered_df):
    state_recovery_data = recovered_df.sort_values('Months since 2020-04-01')

    # Crear lista de colores basada en los valores del DataFrame
    colors = []
    max_value = state_recovery_data['Months since 2020-04-01'].max()
    for value in state_recovery_data['Months since 2020-04-01']:
        if value == -1:
            colors.append('red')
        else:
            # Genera un valor de color basado en el valor actual
            color_intensity = 1 - np.clip(value / max_value, 0, 1)  # Esto asegura que el verde no sea demasiado oscuro
            colors.append(mcolors.to_rgba((1 - color_intensity, 1, 0)))  # Establece un color en formato RGB

    fig, ax = plt.subplots(figsize=(12, 10))
    state_recovery_data['Months since 2020-04-01'].plot(kind='barh', ax=ax, color=colors, edgecolor='black', legend=False)
    ax.set_title('States recovery time from April 2020', fontsize=16)
    ax.set_xlabel('Months since Abril 2020', fontsize=14)
    ax.set_ylabel('Months from April 2020', fontsize=14)
    ax.text(0.5, 0.09, 'A shorter green bar indicates faster return to pre-COVID poverty levels.', transform=ax.transAxes, fontsize=15, va='top')
    ax.axvline(0, color='red', linestyle='--')

    return fig
