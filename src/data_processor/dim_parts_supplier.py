import duckdb
import argparse
from datetime import datetime

def extract_load(con):
    con.execute("INSTALL sqlite; LOAD sqlite;")

    # NOTE: this serves as both extract and load 
    con.execute("CALL sqlite_attach('./tpch.db')")

def transform(con, partition_key):
    # NOTE: Join tables and write to file system directly using DuckDB
    query = f"""
    COPY (
        SELECT 
            p.p_partkey AS partkey, 
            p.p_name AS part_name, 
            p.p_mfgr AS part_manufacturer, 
            p.p_brand AS part_brand, 
            p.p_type AS part_type, 
            p.p_size AS part_size, 
            s.s_name AS supplier_name, 
            p.p_container AS part_container, 
            p.p_retailprice AS part_retailprice, 
            ps.ps_availqty AS supplier_parts_availqty, 
            ps.ps_supplycost AS supplier_supplycost, 
            s.s_address AS supplier_address, 
            s.s_phone AS supplier_phone, 
            s.s_acctbal AS supplier_acctbal, 
            s.s_comment AS supplier_comment,
            n.n_name AS nation_name, 
            r.r_name AS region_name, 
        FROM partsupp ps
        JOIN part p ON ps.ps_partkey = p.p_partkey
        JOIN supplier s ON ps.ps_suppkey = s.s_suppkey
        JOIN nation n ON s.s_nationkey = n.n_nationkey
        JOIN region r ON n.n_regionkey = r.r_regionkey
    ) 
    TO './processed_data/dim_parts_supplier/{partition_key}.csv' (FORMAT csv, HEADER, DELIMITER ',')
    """
    # We can use duckdb's in built partition function as well

    # Execute the query
    con.execute(query)


def run_pipeline(partition_key):
    # create connection for ELT
    # Register SQLite tables in DuckDB
    con = duckdb.connect()
    extract_load(con)
    transform(con, partition_key)
    # Clean up
    con.close()

if __name__ == '__main__':
    # Argument parser for timestamp input
    parser = argparse.ArgumentParser(description="Create dim_parts_supplier table")
    parser.add_argument('timestamp', type=str, help='Timestamp for the folder name')
    args = parser.parse_args()
    folder_name = args.timestamp
    run_pipeline(folder_name)
