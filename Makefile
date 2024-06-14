up:
	python ./src/data_processor/exchange_data.py 2024-05-29 && python ./src/data_processor/dim_parts_supplier.py 2024-05-29 && python ./src/data_processor/one_big_table.py 2024-05-29
