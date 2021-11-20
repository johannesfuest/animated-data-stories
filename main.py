import pandas as pd
from reports.store_outlier import get_store_outlier_for_yesterday
from generate_video import generate_line_story
from reports.growth_cities import get_growth_cities
import os

YESTERDAY1 = "2018-09-17"
YESTERDAY2 = '2019-02-28'


def load_data():
    # Load from csv
    df_product_hierachy = pd.read_csv('dataset/product_hierarchy.csv',
                                      delimiter=',',
                                      dtype={'product_id': 'category',
                                             'cluster_id': 'category',
                                             'hierarchy1_id': 'category',
                                             'hierarchy2_id': 'category',
                                             'hierarchy3_id': 'category',
                                             'hierarchy4_id': 'category',
                                             'hierarchy5_id': 'category'})
    df_stores = pd.read_csv('dataset/store_cities.csv',
                            delimiter=',',
                            dtype={'store_id': 'category',
                                   'storetype_id': 'category',
                                   'city_id': 'category'})
    df_sales = pd.read_csv('dataset/sales.csv',
                           delimiter=',',
                           dtype={"product_id": "category",
                                  "store_id": "category",
                                  "promo_type_1": "category",
                                  "promo_bin_1": "category",
                                  "promo_type_2": "category",
                                  "promo_bin_2": "category",
                                  "promo_discount_2": "category",
                                  "promo_discount_type_2": "category"},
                           parse_dates=["date"])
    df_sales = df_sales.join(df_stores.set_index('store_id'), on='store_id')
    return df_sales.join(df_product_hierachy.set_index('product_id'), on='product_id')


def main():

    print("Load CSV Data")
    df_sales = load_data()
    print("CSV Data Loaded")

    # call different outlier scripts
    print("Check for Yesterdays Outliers")
    yesterday_outliers = get_store_outlier_for_yesterday(df_sales, YESTERDAY1)
    growth_cities = get_growth_cities(df_sales, YESTERDAY2)
    print(f"Found {len(yesterday_outliers)} store outliers")
    print(f"Found {len(growth_cities)} growth cities")

    # do priority
    data_stores = {}
    data_stores.update(yesterday_outliers)
    data_stores.update(growth_cities)

    # generate video
    print("Generating Videos...")
    i = 1
    intro = 'Good morning Michael, here are your Daily Insights.'
    for item, item_data in data_stores.items():
        plot_type, data, text1, text2, _y_label = item_data['chart_type'], item_data['data'], item_data['text1'], item_data['text2'], item_data['y_label']

        x, y = data.T
        vid = generate_line_story(text1, text2, x, y, intro_text=intro, _y_label=_y_label, plot_type=plot_type)

        if not os.path.exists('videos'):
            os.makedirs('videos')
        vid.write_videofile(f'videos/story{i}.mp4', fps=10)
        i += 1
        intro = False
    print("Videos generated.")

    # upload video
    print("Start Uploading Videos")
    print("Script Done")


if __name__ == "__main__":
    main()
