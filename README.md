# Engine Camera ATM

# Introduction

This is a simple engine camera for CCTV in ATM. This engine is usefull for monitoring activity in ATM. This engine is build in docker and using python programming language. For stream the camera is using websocket in viseron.

# Installation docker
- For installation docker you can follow this link https://docs.docker.com/engine/install/ubuntu/
- For installation docker-compose you can follow this link https://docs.docker.com/compose/install/

# Requirements
- Viseron

# Installation
- First you have to create image folder inside the App Folder
- Then you have to create .env file inside the App Folder
- After that running this command in your terminal
``` docker-compose up -d --build ```
- Open your browser and type localhost:9443 to see the container is already running or not

# Environment Variable

- CAMERA_URL=Your camera url
- WEBSOCKET_URI=Your websocket uri
- API_URL=Your api url
- PATH_FILE=/App/image

