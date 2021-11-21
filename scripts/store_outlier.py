import pandas as pd


def get_store_outlier_for_yesterday(df_sales, yesterday):

    # We first build a tool for anomaly detection on daily store performance measured against the 14-day running average:
    daily_revenue_by_store = df_sales.groupby(['store_id', 'date'])[
        'revenue'].agg('sum').reset_index()

    # Only take into account revenue per store over the last 14 days
    daily_revenue_by_store_last_two_weeks = daily_revenue_by_store[daily_revenue_by_store.date.isin(pd.date_range(
        pd.Timedelta(-13, unit='d')+pd.to_datetime(yesterday, format='%Y-%m-%d', errors='ignore').date(), periods=14))]

    # We filter out stores that are not regularaly reporting numbers:
    daily_revenue_by_store_last_two_weeks['revenue'] = daily_revenue_by_store_last_two_weeks['revenue'].fillna(
        0)
    filter_good_stores = daily_revenue_by_store_last_two_weeks.groupby(
        ['store_id']).agg(['max', 'min']).reset_index()
    filter_good_stores.columns = list(
        map(''.join, filter_good_stores.columns.values))
    filter_good_stores = filter_good_stores.loc[filter_good_stores.revenuemax !=
                                                filter_good_stores.revenuemin]
    good_stores = filter_good_stores['store_id'].tolist()
    daily_revenue_by_store_last_two_weeks = daily_revenue_by_store_last_two_weeks[
        daily_revenue_by_store_last_two_weeks.store_id.isin(good_stores)]

    # We now create a dataframe that shows average sales over the past two weeks per store and yesterday's revenue per store.
    two_week_store_mean = daily_revenue_by_store_last_two_weeks.groupby(
        ['store_id']).agg('mean').reset_index()
    two_week_store_mean = two_week_store_mean.dropna()
    two_week_store_mean = two_week_store_mean.rename(
        columns={"revenue": "mean_revenue"})

    yesterday_store_revenue = daily_revenue_by_store_last_two_weeks.loc[
        daily_revenue_by_store_last_two_weeks.date == yesterday]
    yesterday_store_revenue = yesterday_store_revenue.drop(columns=['date'])
    yesterday_store_revenue = yesterday_store_revenue.rename(
        columns={"revenue": "yesterday_revenue"})

    store_mean_yesterday = two_week_store_mean.set_index(
        'store_id').join(yesterday_store_revenue.set_index('store_id'))

    # We now isolate stores whose revenue yesterday was less than 5% of the moving 14-day average:
    underperforming_stores_df = store_mean_yesterday.loc[store_mean_yesterday.yesterday_revenue <
                                                         0.05 * store_mean_yesterday.mean_revenue].reset_index()
    underperforming_stores = underperforming_stores_df['store_id'].tolist()

    result = {}
    for store in underperforming_stores:
        temp = daily_revenue_by_store_last_two_weeks[daily_revenue_by_store_last_two_weeks.store_id.isin([
                                                                                                         store])]
        result[store] = {}
        result[store]["chart_type"] = 0
        result[store]["data"] = temp[['date', 'revenue']].to_numpy()
        result[store]["text1"] = f"Yesterday's daily revenue for store {store} fell below 5% of its 14 day average."
        result[store]["text2"] = "I suggest you check in with the responsible store manager for an explanation."
        result[store]["y_label"] = "Revenue"
    return result
