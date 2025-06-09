install:
	pip install -r requirements.txt

run:
	uvicorn app:app --reload

test:
	pytest
