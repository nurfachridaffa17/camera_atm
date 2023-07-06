# Use an official Python runtime as the base image
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /camera_1

RUN apt-get update && apt-get install libgl1-mesa-glx libglib2.0-0 -y

# Install any required dependencies
RUN pip install requests websocket-client asyncio opencv-python numpy websockets python-dotenv

COPY . .

COPY ./run.py .

# Set the command to run the script file
CMD ["python", "run.py"]