import argparse
from typing import Tuple

import duckdb


def extract_transform_load(con: duckdb.DuckDBPyConnection, partition_key: str) -> None:
    """
    Extracts exchange data from a CoinCap API, transforms it, and loads it into a CSV file.

    Args:
        con: A DuckDB connection object.
        partition_key: A string used to name the output CSV file (e.g., a timestamp).
    """
    con.execute("INSTALL httpfs;")
    con.execute("LOAD httpfs;")
    # Read data from the API and flatten it using DuckDB
    # URL to fetch the data
    url = "https://api.coincap.io/v2/exchanges"
    con.execute(
        f"""
        COPY (
        WITH exchange_data as (
        SELECT UNNEST(data) as data
        FROM read_json('{url}')
        )
        SELECT 
        regexp_replace(json_extract(data, '$.exchangeId')::VARCHAR, '"', '', 'g') AS id,
        regexp_replace(json_extract(data, '$.name')::VARCHAR, '"', '', 'g') AS name,
        json_extract(data, '$.rank')::INTEGER AS rank,
        json_extract(data, '$.percentTotalVolume')::DOUBLE AS percentTotalVolume,
        json_extract(data, '$.volumeUsd')::DOUBLE AS volumeUsd,
        json_extract(data, '$.tradingPairs')::INTEGER AS tradingPairs,
        json_extract(data, '$.socket')::BOOLEAN AS socket,
        regexp_replace(json_extract(data, '$.exchangeUrl')::VARCHAR, '"', '', 'g') AS nexchangeUrl,
        json_extract(data, '$.updated')::BIGINT AS updated
        FROM exchange_data) TO './processed_data/exchange_data/{partition_key}.csv' (FORMAT csv, HEADER, DELIMITER ',')

        """
    ).fetchall()


def run_pipeline(partition_key: str) -> None:
    """
    Runs the entire ETL pipeline for exchange data.

    Args:
        partition_key: A string used to partition the output data (e.g., a timestamp).
    """
    # create connection for ELT
    # Register SQLite tables in DuckDB
    con = duckdb.connect()
    extract_transform_load(con, partition_key)
    # Clean up
    con.close()


if __name__ == "__main__":
    # Argument parser for timestamp input
    parser = argparse.ArgumentParser(description="Create dim_parts_supplier table")
    parser.add_argument("timestamp", type=str, help="Timestamp for the folder name")
    args = parser.parse_args()
    folder_name = args.timestamp
    run_pipeline(folder_name)
