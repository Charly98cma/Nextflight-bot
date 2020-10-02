init:
	pip3 install -r requirements.txt

.ONESHELL:
run:
	export NF_TOKEN=$(shell cat token.txt)
	python3 nextflight_bot/nextflight.py

.PHONY: init, run
