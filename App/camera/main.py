import json
from . import stream_websocket
from .log import Logger
import requests
from dotenv import load_dotenv
from . import stream_camera
import os
import datetime
import base64
import cv2
import time

load_dotenv()

CAMERA_URL = os.getenv("CAMERA_URL")
WEBSOCKET_URI = os.getenv("WEBSOCKET_URI")
API_URL = os.getenv("API_URL")
LOG_MAIN = os.getenv("LOG_MAIN")
PATH_FILE = os.getenv("PATH_FILE")

now = datetime.datetime.now()
log = Logger(log_level=LOG_MAIN)
path_file = PATH_FILE
quality = 25

def take_snapshot(rtsp_url, folder_path, image_name, quality=25):
    # Create a VideoCapture object and open the RTSP stream
    cap = cv2.VideoCapture(rtsp_url)

    # Read a frame from the video stream
    ret, frame = cap.read()

    # Check if a frame was captured successfully
    if ret:
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
            except any as e :
                log.error('No create folder {}'.format(e))

        # Save the frame as an image file in the specified folder
        try:
            cv2.imwrite(os.path.join(folder_path, image_name), frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
            log.info('Success write file')
        except any as e :
            log.error('Gagal bikin file {}'.format(e))

    # Release the VideoCapture object
    cap.release()


def start_camera(image_name):
    screecshooter = stream_camera.CameraScreenshotter(camera_url=CAMERA_URL)
    output_path = '{}/{}'.format(path_file,image_name)
    screecshooter.open_stream()
    screecshooter.capture_screenshot(output_path=output_path)
    screecshooter.close_stream()

    
def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string.decode("utf-8")

async def send_data():
    while True:
        ws =stream_websocket.WebSocketStreamer(uri=WEBSOCKET_URI)
        people_kit = await ws.get_people_kit()
        if people_kit["people"] != False and people_kit["helmet"] != False and people_kit["crowbar"] != False and people_kit["bowed_position"] != False:
            image_name = "capture_ATM_001_{}_4.jpg".format(now.strftime("%Y-%m-%d_%H-%M-%S"))
            output_path = '{}/{}'.format(path_file,image_name)
            # take_snapshot(rtsp_url=CAMERA_URL, folder_path=path_file, image_name=image_name, quality=quality)
            start_camera(image_name=image_name)
            base_64_image = convert_image_to_base64(image_path=output_path)
            payload = {
                "atm_name": "ATM_001",
                "customer_name": "Aetherica",
                "device_name": "Edge_AI_1",
                "objects_count" : 4,
                "detected_objects": [
                        {
                            "label": people_kit["people"]["label"],
                            "confidence": people_kit["people"]["confidence"]
                        },
                        {
                            "label": people_kit["helmet"]["label"],
                            "confidence": people_kit["helmet"]["confidence"]
                        },
                        {
                            "label": people_kit["crowbar"]["label"],
                            "confidence": people_kit["crowbar"]["confidence"]
                        },
                        {
                            "label": people_kit["bowed_position"]["label"],
                            "confidence": people_kit["bowed_position"]["confidence"]
                        }
                    ],
                "image" : base_64_image,
            }
            headers = {
                "Content-Type": "application/json"
            }
            try:
                response = requests.post(API_URL, json=payload, headers=headers)
                if response.status_code == 204:
                    log.info("Success send data to API : {}".format(response.status_code))
                else:
                    log.error("Failed send data to API : {}".format(response.status_code))
            except requests.exceptions.ConnectionError:
                log.error("Connection refused to API Server : {}".format(API_URL))
            time.sleep(5)

        elif people_kit["people"] != False and people_kit["helmet"] == False and people_kit["crowbar"] == False and people_kit["bowed_position"] == False:
            image_name = "capture_ATM_001_{}_1_people.jpg".format(now.strftime("%Y-%m-%d_%H-%M-%S"))
            # take_snapshot(rtsp_url=CAMERA_URL, folder_path=path_file, image_name=image_name, quality=quality)
            output_path = '{}/{}'.format(path_file,image_name)
            start_camera(image_name=image_name)
            base_64_image = convert_image_to_base64(image_path=output_path)
            payload = {
                "atm_name": "ATM_001",
                "customer_name": "Aetherica",
                "device_name": "Edge_AI_1",
                "objects_count" : 1,
                "detected_objects": [
                        {
                            "label": people_kit["people"]["label"],
                            "confidence": people_kit["people"]["confidence"]
                        }
                    ],
                "image" : base_64_image,
            }
            headers = {
                "Content-Type": "application/json"
            }
            try:
                response = requests.post(API_URL, json=payload, headers=headers)
                if response.status_code == 204:
                    log.info("Success send data to API : {}".format(response.status_code))
                else:
                    log.error("Failed send data to API : {}".format(response.status_code))
            except requests.exceptions.ConnectionError:
                log.error("Connection refused to API Server : {}".format(API_URL))
            time.sleep(5)
        
        elif people_kit["people"] != False and people_kit["helmet"] != False and people_kit["crowbar"] == False and people_kit["bowed_position"] == False:
            image_name = "capture_ATM_001_{}_2_people_helmet.jpg".format(now.strftime("%Y-%m-%d_%H-%M-%S"))
            # take_snapshot(rtsp_url=CAMERA_URL, folder_path=path_file, image_name=image_name, quality=quality)
            output_path = '{}/{}'.format(path_file,image_name)
            start_camera(image_name=image_name)
            base_64_image = convert_image_to_base64(image_path=output_path)
            payload = {
                "atm_name": "ATM_001",
                "customer_name": "Aetherica",
                "device_name": "Edge_AI_1",
                "objects_count" : 2,
                "detected_objects": [
                        {
                            "label": people_kit["people"]["label"],
                            "confidence": people_kit["people"]["confidence"]
                        },
                        {
                            "label": people_kit["helmet"]["label"],
                            "confidence": people_kit["helmet"]["confidence"]
                        }
                    ],
                "image" : base_64_image,
            }
            headers = {
                "Content-Type": "application/json"
            }
            try:
                response = requests.post(API_URL, json=payload, headers=headers)
                if response.status_code == 204:
                    log.info("Success send data to API : {}".format(response.status_code))
                else:
                    log.error("Failed send data to API : {}".format(response.status_code))
            except requests.exceptions.ConnectionError:
                log.error("Connection refused to API Server : {}".format(API_URL))
            time.sleep(5)
        
        elif people_kit["people"] != False and people_kit["helmet"] != False and people_kit["crowbar"] != False and people_kit["bowed_position"] == False:
            image_name = "capture_ATM_001_{}_3_people_helmet_crowbar.jpg".format(now.strftime("%Y-%m-%d_%H-%M-%S"))
            # take_snapshot(rtsp_url=CAMERA_URL, folder_path=path_file, image_name=image_name, quality=quality)
            output_path = '{}/{}'.format(path_file,image_name)
            start_camera(image_name=image_name)
            base_64_image = convert_image_to_base64(image_path=output_path)
            payload = {
                "atm_name": "ATM_001",
                "customer_name": "Aetherica",
                "device_name": "Edge_AI_1",
                "objects_count" : 3,
                "detected_objects": [
                        {
                            "label": people_kit["people"]["label"],
                            "confidence": people_kit["people"]["confidence"]
                        },
                        {
                            "label": people_kit["helmet"]["label"],
                            "confidence": people_kit["helmet"]["confidence"]
                        },
                        {
                            "label": people_kit["crowbar"]["label"],
                            "confidence": people_kit["crowbar"]["confidence"]
                        }
                    ],
                "image" : base_64_image,
            }
            headers = {
                "Content-Type": "application/json"
            }
            try:
                response = requests.post(API_URL, json=payload, headers=headers)
                if response.status_code == 204:
                    log.info("Success send data to API : {}".format(response.status_code))
                else:
                    log.error("Failed send data to API : {}".format(response.status_code))
            except requests.exceptions.ConnectionError:
                log.error("Connection refused to API Server : {}".format(API_URL))
            time.sleep(5)

        elif people_kit["people"] != False and people_kit["helmet"] == False and people_kit["crowbar"] != False and people_kit["bowed_position"] != False:
            image_name = "capture_ATM_001_{}_3_people_crowbar_bowed.jpg".format(now.strftime("%Y-%m-%d_%H-%M-%S"))
            # take_snapshot(rtsp_url=CAMERA_URL, folder_path=path_file, image_name=image_name, quality=quality)
            output_path = '{}/{}'.format(path_file,image_name)
            start_camera(image_name=image_name)
            base_64_image = convert_image_to_base64(image_path=output_path)
            payload = {
                "atm_name": "ATM_001",
                "customer_name": "Aetherica",
                "device_name": "Edge_AI_1",
                "objects_count" : 3,
                "detected_objects": [
                        {
                            "label": people_kit["people"]["label"],
                            "confidence": people_kit["people"]["confidence"]
                        },
                        {
                            "label": people_kit["crowbar"]["label"],
                            "confidence": people_kit["crowbar"]["confidence"]
                        },
                        {
                            "label": people_kit["bowed_position"]["label"],
                            "confidence": people_kit["bowed_position"]["confidence"]
                        }
                    ],
                "image" : base_64_image,
            }
            headers = {
                "Content-Type": "application/json"
            }
            try:
                response = requests.post(API_URL, json=payload, headers=headers)
                if response.status_code == 204:
                    log.info("Success send data to API : {}".format(response.status_code))
                else:
                    log.error("Failed send data to API : {}".format(response.status_code))
            except requests.exceptions.ConnectionError:
                log.error("Connection refused to API Server : {}".format(API_URL))
            time.sleep(5)
        
        elif people_kit["people"] != False and people_kit["helmet"] != False and people_kit["crowbar"] == False and people_kit["bowed_position"] != False:
            image_name = "capture_ATM_001_{}_3_people_helmet_bowed.jpg".format(now.strftime("%Y-%m-%d_%H-%M-%S"))
            # take_snapshot(rtsp_url=CAMERA_URL, folder_path=path_file, image_name=image_name, quality=quality)
            output_path = '{}/{}'.format(path_file,image_name)
            start_camera(image_name=image_name)
            base_64_image = convert_image_to_base64(image_path=output_path)
            payload = {
                "atm_name": "ATM_001",
                "customer_name": "Aetherica",
                "device_name": "Edge_AI_1",
                "objects_count" : 3,
                "detected_objects": [
                        {
                            "label": people_kit["people"]["label"],
                            "confidence": people_kit["people"]["confidence"]
                        },
                        {
                            "label": people_kit["helmet"]["label"],
                            "confidence": people_kit["helmet"]["confidence"]
                        },
                        {
                            "label": people_kit["bowed_position"]["label"],
                            "confidence": people_kit["bowed_position"]["confidence"]
                        }
                    ],
                "image" : base_64_image,
            }
            headers = {
                "Content-Type": "application/json"
            }
            try:
                response = requests.post(API_URL, json=payload, headers=headers)
                if response.status_code == 204:
                    log.info("Success send data to API : {}".format(response.status_code))
                else:
                    log.error("Failed send data to API : {}".format(response.status_code))
            except requests.exceptions.ConnectionError:
                log.error("Connection refused to API Server : {}".format(API_URL))
            time.sleep(5)
        
        elif people_kit["people"] != False and people_kit["helmet"] == False and people_kit["crowbar"] == False and people_kit["bowed_position"] != False:
            image_name = "capture_ATM_001_{}_2_people_bowed.jpg".format(now.strftime("%Y-%m-%d_%H-%M-%S"))
            # take_snapshot(rtsp_url=CAMERA_URL, folder_path=path_file, image_name=image_name, quality=quality)
            output_path = '{}/{}'.format(path_file,image_name)
            start_camera(image_name=image_name)
            base_64_image = convert_image_to_base64(image_path=output_path)
            payload = {
                "atm_name": "ATM_001",
                "customer_name": "Aetherica",
                "device_name": "Edge_AI_1",
                "objects_count" : 2,
                "detected_objects": [
                        {
                            "label": people_kit["people"]["label"],
                            "confidence": people_kit["people"]["confidence"]
                        },
                        {
                            "label": people_kit["bowed_position"]["label"],
                            "confidence": people_kit["bowed_position"]["confidence"]
                        }
                    ],
                "image" : base_64_image,
            }
            headers = {
                "Content-Type": "application/json"
            }
            try:
                response = requests.post(API_URL, json=payload, headers=headers)
                if response.status_code == 204:
                    log.info("Success send data to API : {}".format(response.status_code))
                else:
                    log.error("Failed send data to API : {}".format(response.status_code))
            except requests.exceptions.ConnectionError:
                log.error("Connection refused to API Server : {}".format(API_URL))
            time.sleep(5)
        else:
            log.info("No suspicious activity detected")

    