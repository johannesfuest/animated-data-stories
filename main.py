import pandas as pd
from reports.store_outlier import get_store_outlier_for_yesterday
from generate_video import generate_line_story

YESTERDAY = "2018-09-17"

def load_data():
    # Load from csv
    df_product_hierachy = pd.read_csv('dataset/product_hierarchy.csv', 
                                    delimiter= ',',
                                    dtype={'product_id':'category',
                                            'cluster_id':'category',
                                            'hierarchy1_id':'category',
                                            'hierarchy2_id':'category',
                                            'hierarchy3_id':'category',
                                            'hierarchy4_id':'category',
                                            'hierarchy5_id':'category'})
    df_sales = pd.read_csv('dataset/sales.csv',
                        delimiter=',', 
                        dtype={"product_id":"category", 
                                "store_id":"category",
                                "promo_type_1":"category",
                                "promo_bin_1":"category",
                                "promo_type_2":"category",
                                "promo_bin_2":"category",
                                "promo_discount_2":"category",
                                "promo_discount_type_2":"category"},
                        parse_dates=["date"])
    return df_sales.join(df_product_hierachy.set_index('product_id'), on='product_id')

def main():
    print("Load CSV Data")
    df_sales = load_data()
    print("CSV Data Loaded")
    # call different outlier scripts
    print("Check for Yesterdays Outliers")
    yesterday_outliers = get_store_outlier_for_yesterday(df_sales, YESTERDAY)
    print(f"Found {len(yesterday_outliers)} store outliers")
    # do priority
    

    # generate video
    print("Generating Videos...")
    i = 1
    for store, store_data in yesterday_outliers.items():
        chart_type, data, text1, text2 = store_data['chart_type'], store_data['data'], store_data['text1'], store_data['text2']
    
        x, y = data.T
        vid = generate_line_story('intro sentence', text1, text2, x, y)

        vid.write_videofile(f'videos/story{i}.mp4', fps=10)
        i += 1
    print("Videos generated.")

    # upload video
    print("Start Uploading Videos")
    print("Script Done")

if __name__ == "__main__":
    main()