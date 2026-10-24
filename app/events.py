from datetime import datetime


class SentinelEventEngine:
    def __init__(
        self,
        camera_name="Camera",
        crowd_threshold=10,
        loitering_time=10,
        allowed_direction="right",
        min_movement=5,
        restricted_zone=None
    ):
        self.camera_name = camera_name
        self.crowd_threshold = crowd_threshold
        self.loitering_time = loitering_time
        self.allowed_direction = allowed_direction
        self.min_movement = min_movement
        self.restricted_zone = restricted_zone

        self.first_seen = {}
        self.previous_positions = {}
        self.triggered = set()
        self.incidents = []

    def incident(
        self,
        event,
        frame,
        timestamp,
        track_id=None,
        severity="MEDIUM"
    ):
        incident_id = (
            f"SNT-{datetime.now().strftime('%Y%m%d-%H%M%S')}-"
            f"{len(self.incidents) + 1:04d}"
        )

        item = {
            "Incident_ID": incident_id,
            "Event": event,
            "Camera": self.camera_name,
            "Person_ID": track_id,
            "Timestamp_seconds": round(timestamp, 2),
            "Frame": frame,
            "Severity": severity,
            "Status": "OPEN"
        }

        self.incidents.append(item)

        return item

    def process(self, objects, frame_number, timestamp):

        people = [
            obj for obj in objects
            if obj["class_id"] == 0
        ]

        # -----------------------------
        # CROWD DETECTION
        # -----------------------------
        if len(people) >= self.crowd_threshold:

            key = ("crowd", frame_number // 30)

            if key not in self.triggered:

                self.triggered.add(key)

                self.incident(
                    "Crowd Detected",
                    frame_number,
                    timestamp,
                    severity="MEDIUM"
                )

        # -----------------------------
        # PERSON-BASED EVENTS
        # -----------------------------
        for obj in people:

            track_id = obj["track_id"]
            center = obj["center"]

            if track_id is None:
                continue

            # First time seeing this person
            if track_id not in self.first_seen:
                self.first_seen[track_id] = timestamp

            duration = (
                timestamp -
                self.first_seen[track_id]
            )

            # -----------------------------
            # LOITERING
            # -----------------------------
            if duration >= self.loitering_time:

                key = ("loiter", track_id)

                if key not in self.triggered:

                    self.triggered.add(key)

                    self.incident(
                        "Loitering Detected",
                        frame_number,
                        timestamp,
                        track_id,
                        "MEDIUM"
                    )

            # -----------------------------
            # RESTRICTED AREA INTRUSION
            # -----------------------------
            if self.restricted_zone:

                x1, y1, x2, y2 = self.restricted_zone

                x, y = center

                inside_zone = (
                    x1 <= x <= x2 and
                    y1 <= y <= y2
                )

                if inside_zone:

                    key = ("intrusion", track_id)

                    if key not in self.triggered:

                        self.triggered.add(key)

                        self.incident(
                            "Restricted Area Intrusion",
                            frame_number,
                            timestamp,
                            track_id,
                            "HIGH"
                        )

            # Save previous position
            self.previous_positions[track_id] = center

        return self.incidents


if __name__ == "__main__":
    print("SENTINEL Event Engine ready")
