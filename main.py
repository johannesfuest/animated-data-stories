from reports.store_outlier import get_store_outlier_for_yesterday
from generate_video import generate_video

YESTERDAY = "2018-09-17"

def main():
    # load data
    print("Load Date")

    print("Data Loaded")

    # call different outlier scripts
    print("Check for Yesterdays Outliers")
    yesterday_outliers = get_store_outlier_for_yesterday(YESTERDAY)
    print(f"Found {len(yesterday_outliers)} store outliers")
    # do priority

    # generate video
    print("Start generation Videos")
    generate_video(yesterday_outliers)
    # upload video
    print("Start Uploading Videos")
    print("Script Done")

if __name__ == "__main__":
    main()