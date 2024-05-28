.silent on
-- Create tables
CREATE TABLE nation (
    n_nationkey INTEGER PRIMARY KEY,
    n_name TEXT,
    n_regionkey INTEGER,
    n_comment TEXT
);

CREATE TABLE region (
    r_regionkey INTEGER PRIMARY KEY,
    r_name TEXT,
    r_comment TEXT
);

CREATE TABLE part (
    p_partkey INTEGER PRIMARY KEY,
    p_name TEXT,
    p_mfgr TEXT,
    p_brand TEXT,
    p_type TEXT,
    p_size INTEGER,
    p_container TEXT,
    p_retailprice REAL,
    p_comment TEXT
);

CREATE TABLE supplier (
    s_suppkey INTEGER PRIMARY KEY,
    s_name TEXT,
    s_address TEXT,
    s_nationkey INTEGER,
    s_phone TEXT,
    s_acctbal REAL,
    s_comment TEXT
);

CREATE TABLE partsupp (
    ps_partkey INTEGER,
    ps_suppkey INTEGER,
    ps_availqty INTEGER,
    ps_supplycost REAL,
    ps_comment TEXT,
    PRIMARY KEY (ps_partkey, ps_suppkey)
);

CREATE TABLE customer (
    c_custkey INTEGER PRIMARY KEY,
    c_name TEXT,
    c_address TEXT,
    c_nationkey INTEGER,
    c_phone TEXT,
    c_acctbal REAL,
    c_mktsegment TEXT,
    c_comment TEXT
);

CREATE TABLE orders (
    o_orderkey INTEGER PRIMARY KEY,
    o_custkey INTEGER,
    o_orderstatus TEXT,
    o_totalprice REAL,
    o_orderdate TEXT,
    o_orderpriority TEXT,
    o_clerk TEXT,
    o_shippriority INTEGER,
    o_comment TEXT
);

CREATE TABLE lineitem (
    l_orderkey INTEGER,
    l_partkey INTEGER,
    l_suppkey INTEGER,
    l_linenumber INTEGER,
    l_quantity REAL,
    l_extendedprice REAL,
    l_discount REAL,
    l_tax REAL,
    l_returnflag TEXT,
    l_linestatus TEXT,
    l_shipdate TEXT,
    l_commitdate TEXT,
    l_receiptdate TEXT,
    l_shipinstruct TEXT,
    l_shipmode TEXT,
    l_comment TEXT,
    PRIMARY KEY (l_orderkey, l_linenumber)
);

-- Import data
.mode csv
.separator |
.import ./tpch-dbgen/nation.tbl nation
.import ./tpch-dbgen/region.tbl region
.import ./tpch-dbgen/part.tbl part
.import ./tpch-dbgen/supplier.tbl supplier
.import ./tpch-dbgen/partsupp.tbl partsupp
.import ./tpch-dbgen/customer.tbl customer
.import ./tpch-dbgen/orders.tbl orders
.import ./tpch-dbgen/lineitem.tbl lineitem

