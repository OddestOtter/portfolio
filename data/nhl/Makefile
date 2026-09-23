SEASONS ?= 20242025
land:
	python src/ingest.py $(SEASONS)

silver:
	cd dbt_project && dbt build

pipeline: land silver

rebuild:
	rm -f data/warehouse/nhl.duckdb
	$(MAKE) silver