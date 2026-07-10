install:
	pip install -r requirements.txt

test:
	pytest

validate:
	python lambda/validation/handler.py
