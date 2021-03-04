FROM python:3.9-slim-buster

# Create directory for the bot
WORKDIR /nextflight_bot

# Copy and install dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the rest of the bot
COPY . .

# Run the bot
CMD ["python3", "nextflight_bot/nextflight.py"]
