setup:
	python3 -m venv ~/.MovieSchedulerApp

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	hadolint Dockerfile
	pylint --disable=R,C,W1203 main.py
	
all:
	install lint