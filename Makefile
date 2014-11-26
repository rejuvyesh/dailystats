all: push

csv:
	arbtt-stats --categorizefile=./categorize.cfg --for-each=day --output-format=CSV > /tmp/cleanstats.csv

json: csv
	mkdir -p /tmp/data
	python readdailystats.py /tmp/cleanstats.csv

git: json
	git checkout gh-pages
	/usr/bin/cp -r /tmp/data .
	/usr/bin/cp /tmp/loglist.json .
	git add .

push: git
	git commit -m "`date`: push logs"
	git push origin gh-pages
	git checkout master
