run:
	cd app; python main.py

build:
	docker build -t my-python-app .

d-run:
	docker run -it --rm --name my-running-app my-python-app