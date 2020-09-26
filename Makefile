init:
	pip3 install -r requirements.txt
token:
	export NF_TOKEN=$(cat token.txt)
run:
	python3 nextflight_bot/nextflight.py

.PHONY: token, init, run
