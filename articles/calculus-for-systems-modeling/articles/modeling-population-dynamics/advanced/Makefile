.PHONY: smoke report clean
smoke: report
report:
	python3 python/generate_advanced_report.py
clean:
	rm -f outputs/reports/*.md outputs/json/*.json outputs/tables/*.csv
