import os
import time
import uuid
from datetime import datetime, timezone

file_path = "/usr/src/app/files/log.txt"

os.makedirs(os.path.dirname(file_path), exist_ok=True)

random_string = str(uuid.uuid4())

while True:
    timestamp = datetime.now(timezone.utc).isoformat()
    with open(file_path, "w") as f:
        f.write(f"{timestamp}: {random_string}\n")
    time.sleep(5)
