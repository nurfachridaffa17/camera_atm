from camera import main
import asyncio
import os
from camera import log as logging

log = logging.Logger()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8765))
    log.info("Starting the WebSocket server on port {}".format(port))
    asyncio.run(main.send_data())