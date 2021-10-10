database_name=auction.db
python=python
sqlite=sqlite3

run: clean make_db run_queries

make_db: clean FORCE
	$(python) parser.py items-*.json
	$(sqlite) $(database_name) < create.sql
	$(sqlite) $(database_name) < load.txt

run_queries: make_db
	$(sqlite) $(database_name) < query1.sql
	$(sqlite) $(database_name) < query2.sql
	$(sqlite) $(database_name) < query3.sql
	$(sqlite) $(database_name) < query4.sql
	$(sqlite) $(database_name) < query5.sql
	$(sqlite) $(database_name) < query6.sql
	$(sqlite) $(database_name) < query7.sql


clean: FORCE
ifneq ("$(wildcard $(database_name))","")
ifeq ($(OS),Windows_NT)
	del $(database_name)
else
	rm $(database_name)
endif
endif



FORCE:

