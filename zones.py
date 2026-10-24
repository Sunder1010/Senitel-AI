import json
import os


class SentinelZoneManager:
    def __init__(self, path="data/zones.json"):
        self.path = path

        os.makedirs(
            os.path.dirname(self.path),
            exist_ok=True
        )

    def save_zone(self, camera_name, zone):
        data = {}

        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}

        data[camera_name] = {
            "restricted_zone": list(zone)
        }

        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)

        print(
            f"Zone saved for {camera_name}: {zone}"
        )

    def get_zone(self, camera_name):
        if not os.path.exists(self.path):
            return None

        with open(self.path, "r") as f:
            data = json.load(f)

        camera = data.get(camera_name)

        if not camera:
            return None

        zone = camera.get("restricted_zone")

        if zone:
            return tuple(zone)

        return None

    def get_all_zones(self):
        if not os.path.exists(self.path):
            return {}

        with open(self.path, "r") as f:
            return json.load(f)
