import argparse

import duckdb


def extract_transform_load(
    con: duckdb.DuckDBPyConnection, partition_key: str, api_token: str
) -> None:
    """
    Extracts exchange data from a CoinCap API, transforms it, and loads it into a CSV file.

    Args:
        con: A DuckDB connection object.
        partition_key: A string used to name the output CSV file (e.g., a timestamp).
        api_token: The CoinCap API token, as string.
    """
    con.execute("INSTALL httpfs;")
    con.execute("LOAD httpfs;")

    # Disable ETag checks to avoid errors caused by live API responses changing
    # between DuckDB's internal multi-pass HTTP reads of the same endpoint.
    con.execute("SET unsafe_disable_etag_checks = true;")

    # Read data from the API and flatten it using DuckDB
    # URL to fetch the data
    url = "https://rest.coincap.io/v3/exchanges"

    con.execute(f"CREATE SECRET http_auth (TYPE http, BEARER_TOKEN '{api_token}');")
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
                regexp_replace(json_extract(data, '$.exchangeUrl')::VARCHAR, '"', '', 'g') AS exchangeUrl,
                json_extract(data, '$.updated')::BIGINT AS updated
            FROM exchange_data
        ) TO './processed_data/exchange_data/{partition_key}.csv' (FORMAT csv, HEADER, DELIMITER ',')
        """
    ).fetchall()


def run_pipeline(partition_key: str, api_token: str) -> None:
    """
    Runs the entire ETL pipeline for exchange data.

    Args:
        partition_key: A string used to partition the output data (e.g., a timestamp).
        api_token: The CoinCap API token, as string.
    """
    # create connection for ELT
    # Register SQLite tables in DuckDB
    con = duckdb.connect()
    extract_transform_load(con, partition_key, api_token)
    # Clean up
    con.close()


if __name__ == "__main__":
    # Argument parser for timestamp input
    parser = argparse.ArgumentParser(description="Create dim_parts_supplier table")
    parser.add_argument("timestamp", type=str, help="Timestamp for the folder name")
    parser.add_argument("api_token", type=str, help="CoinCap API token")
    args = parser.parse_args()

    run_pipeline(args.timestamp, args.api_token)
