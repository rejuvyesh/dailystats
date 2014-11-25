all: csv json

csv:
	arbtt-stats --categorizefile=./categorize.cfg --for-each=day --output-format=CSV > /tmp/cleanstats.csv

json: csv
	mkdir -p data
	python readdailystats.py /tmp/cleanstats.csv
