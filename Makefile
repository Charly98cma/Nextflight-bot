init:
	pip3 install -r requirements.txt
run:
	export NF_TOKEN=$(shell cat token.txt)
	python3 nextflight_bot/nextflight.py

.PHONY: token, init, run
