import pandas as pd
import numpy as np


def get_growth_cities(df_sales, yesterday):
    df_sales_clean = df_sales[['date', 'revenue', 'city_id']]
    df_sales_clean['revenue'] = df_sales_clean['revenue'].fillna(0)

    # We then group the data by city id and date, giving us daily revenue by city
    daily_revenue_by_city = df_sales_clean.groupby(['city_id', 'date'])[
        'revenue'].agg('sum')
    daily_revenue_by_city = daily_revenue_by_city.dropna()

    # We further aggregate the data to get monthly revenue data per city
    monthly_rev_by_city = daily_revenue_by_city.groupby([pd.Grouper(level='city_id'),
                                                         pd.Grouper(freq='1M', level='date')]).sum()
    monthly_rev_by_city = monthly_rev_by_city.reset_index()
    monthly_rev_by_city = monthly_rev_by_city.dropna()

    # We can now compare the revenue of the last month with the month half a year ago
    get_growth = monthly_rev_by_city
    get_growth['revenue_past_halb_year'] = get_growth['revenue'].shift(6)
    get_growth['half_year_increase'] = (
        (get_growth['revenue'] / get_growth['revenue_past_halb_year']) - 1) * 100
    get_growth = get_growth.loc[get_growth.date ==
                                pd.to_datetime(yesterday, format='%Y-%m-%d')]
    get_growth = get_growth.loc[get_growth.half_year_increase > 100]
    growth_cities = get_growth['city_id'].tolist()
    growth_values = get_growth['half_year_increase'].tolist()

    # The identified groth cities are now stored with the respectiv graph data and texts
    res = {}
    for i in range(len(growth_cities)):
        res[growth_cities[i]] = {}
        temp = monthly_rev_by_city
        temp = temp.loc[temp.city_id == growth_cities[i]]
        temp['date'] = pd.to_datetime(temp['date'], format='%Y-%m-%d')
        temp = temp[['date', 'revenue']]
        temp = temp.loc[temp.date <= pd.to_datetime(
            yesterday, format='%Y-%m-%d')]
        temp = temp.loc[temp.date >= (pd.to_datetime(
            yesterday, format='%Y-%m-%d') - pd.DateOffset(years=1))]
        temp['date'] = temp['date'].dt.strftime('%Y-%m')
        res[growth_cities[i]]["data"] = temp.to_numpy()
        res[growth_cities[i]
            ]["text1"] = f"City {growth_cities[i]} increased its monthly revenue by {int(growth_values[i])} percent over the past six months"
        res[growth_cities[i]
            ]["text2"] = "We should consider expanding our presense in the city"
        res[growth_cities[i]]["y_label"] = "Monthly Revenue"
        res[growth_cities[i]]["chart_type"] = 1
    return res
