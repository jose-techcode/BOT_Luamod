# Use an official Python image

FROM python:3.12-slim

# Define the directory inside the container

WORKDIR /app

# Copy all files from your local folder to the container (. means "this folder")

COPY . /app

# Install the dependencies

RUN pip install --no-cache-dir -r requirements.txt

# Command to run the bot

CMD ["python", "bot.py"]
