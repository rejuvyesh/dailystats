all: push

csv:
	./arbtt-stats --categorizefile=./categorize.cfg --for-each=day --output-format=CSV > /tmp/cleanstats.csv
	./arbtt-stats --categorizefile=./minute-cat.cfg --for-each=minute --output-format=CSV > /tmp/minutestats.csv

json: csv
	mkdir -p /tmp/data
	python readdailystats.py /tmp/cleanstats.csv /tmp/minutestats.csv

git: json
	git checkout gh-pages
	/usr/bin/cp -r /tmp/data .
	/usr/bin/cp /tmp/loglist.json .
	git add .
	git commit -m "`date`: push logs"

push: git
	git push origin gh-pages
	git checkout master
