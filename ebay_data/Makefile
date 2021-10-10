database_name=auction.db

run: clean make_db

make_db: clean FORCE
	python parser.py items-*.json
	sqlite3 $(database_name) < create.sql
	sqlite3 $(database_name) < load.txt

clean: FORCE
ifneq ("$(wildcard $(database_name))","")
ifeq ($(OS),Windows_NT)
	del $(database_name)
else
	rm $(database_name)
endif
endif



FORCE:

