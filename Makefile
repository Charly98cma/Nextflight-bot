init:
	pip3 install -r requirements.txt

.ONESHELL:
run:
	export NF_TOKEN=$(shell cat token.txt)
	python3 nextflight_bot/nextflight.py

dockerbuild:
	docker build --tag nextflight-bot .

dockerrun:
	docker run --detach --name nextflight-bot nextflight-bot:latest

.PHONY: init, run, dockerbuild, dockerrun
