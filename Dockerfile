FROM python:3.7

RUN mkdir /nextflight_bot
WORKDIR /nextflight_bot
COPY . .

RUN make init

CMD make run
