import time

from src.log_generator import generate_logs
from src.extract import extract_logs
from src.transform import transform_logs
from src.load import load_to_mysql
from src.logger import get_logger


logger = get_logger()


def main():

    start = time.time()

    logger.info(
        "Pipeline Started"
    )

    # Generate 75k new records
    generate_logs(75000)

    logger.info(
        "75,000 synthetic logs generated"
    )

    logs = extract_logs(
        "data/raw/access.log"
    )

    logger.info(
        f"{len(logs):,} logs extracted"
    )

    df = transform_logs(logs)

    logger.info(
        "Transformation completed"
    )

    load_to_mysql(df)

    logger.info(
        "Data loaded to MySQL"
    )

    df.to_csv(
        "data/processed/web_traffic_processed.csv",
        index=False
    )

    logger.info(
        "CSV exported"
    )

    end = time.time()

    logger.info(
        f"Pipeline completed "
        f"in {end-start:.2f} seconds"
    )

    print(
        f"Pipeline finished "
        f"in {end-start:.2f} seconds"
    )


if __name__ == "__main__":
    main()