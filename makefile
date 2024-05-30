run:
	cd app; python main.py

build:
	docker build -t my-python-app .

d-run:
	docker run -it --rm --name my-running-app my-python-app

test:
	cd app; python -m unittest discover -s tests

coverage:
	cd app; coverage run -m unittest discover -s tests

c-report:
	cd app; coverage report

c-html:
	cd app; coverage html

install:
	pip install -r requirements.txt 