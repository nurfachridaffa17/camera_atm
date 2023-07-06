import asyncio
import websockets
import json
from .log import Logger

log = Logger()

class WebSocketStreamer:
    def __init__(self, uri):
        self.uri = uri
        self.websocket = None
        self.is_streaming = False

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.uri)
            self.is_streaming = True
            log.info("Connected to the WebSocket server.")
        except websockets.exceptions.ConnectionError:
            log.error("Failed to connect to the WebSocket server.")

    async def disconnect(self):
        await self.websocket.close()
        self.is_streaming = False

    async def stream_data(self):
        await self.connect()
        command_id = 1
        people_kit = {
            "people": False,
            "helmet": False,
            "crowbar": False,
            "bowed_position": False
        }
        while self.is_streaming:
            try:
                if self.websocket:
                    await self.websocket.send(json.dumps({"type": "get_entities", "command_id": command_id}))
                else:
                    log.error("WebSocket connection is not established.")
                    break

                response = await self.websocket.recv()
                parsed_response = json.loads(response)
                result = parsed_response.get("result")
                if result:
                    for value, entity_data in result.items():
                        if "binary_sensor.viseron_camera_object_detected_orang" in value:
                            if entity_data['state'] == "on":
                                people_kit["people"] = True
                                if people_kit["people"]:
                                    people_kit["people"] = {
                                        "label": entity_data["attributes"]["objects"][0]["label"],
                                        "confidence": entity_data["attributes"]["objects"][0]["confidence"],
                                    }
                            else:
                                people_kit["people"] = False

                        if "binary_sensor.viseron_camera_object_detected_helm" in value:
                            if entity_data['state'] == "on":
                                people_kit["helmet"] = True
                                if people_kit["helmet"]:
                                    people_kit["helmet"] = {
                                        "label": entity_data["attributes"]["objects"][0]["label"],
                                        "confidence": entity_data["attributes"]["objects"][0]["confidence"],
                                    }
                            else:
                                people_kit["helmet"] = False

                        if "binary_sensor.viseron_camera_object_detected_linggis" in value:
                            if entity_data['state'] == "on":
                                people_kit["crowbar"] = True
                                if people_kit["crowbar"]:
                                    people_kit["crowbar"] = {
                                        "label": entity_data["attributes"]["objects"][0]["label"],
                                        "confidence": entity_data["attributes"]["objects"][0]["confidence"],
                                    }
                            else:
                                people_kit["crowbar"] = False

                        if "binary_sensor.viseron_camera_object_detected_posisi_nunduk" in value:
                            if entity_data['state'] == "on":
                                people_kit["bowed_position"] = True
                                if people_kit["bowed_position"]:
                                    people_kit["bowed_position"] = {
                                        "label": entity_data["attributes"]["objects"][0]["label"],
                                        "confidence": entity_data["attributes"]["objects"][0]["confidence"],
                                    }
                            else:
                                people_kit["bowed_position"] = False

                    if any(people_kit.values()):
                        log.info("One or more values are True. Disconnecting from WebSocket.")
                        await self.disconnect()
                        # asyncio.sleep(5)

            except websockets.exceptions.ConnectionClosed:
                log.warning("Connection closed by the server")
                await self.disconnect()

            command_id += 1

        return people_kit

    async def get_people_kit(self):
        return await self.stream_data()

    def start_streaming(self):
        self.is_streaming = True
        asyncio.get_event_loop().run_until_complete(self.stream_data())

    def stop_streaming(self):
        self.is_streaming = False