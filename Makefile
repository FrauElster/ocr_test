install:
	pip install --user -r

create:
	python3 -m ocr-test create --min 15 --max 25

eval:
	python3 -m ocr-test eval

del_pdf:
	python3 -m ocr-test delete --type pdf
