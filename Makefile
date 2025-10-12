.PHONY: sample

sample:
	python main.py "+" 4

clearPDF:
	rm -rf *.pdf

test:
	pytest -v .