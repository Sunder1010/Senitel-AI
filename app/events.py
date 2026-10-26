%cd /content/sentinel

events_code = r'''
from datetime import datetime
import math


class SentinelEventEngine:

    def __init__(
        self,
        camera_name="Camera",
        crowd_threshold=8,
        loitering_time=10,
        loitering_radius=60,
        max_stationary_path=120,
        restricted_zone=None
    ):
        self.camera_name = camera_name

        self.crowd_threshold = crowd_threshold
        self.loitering_time = loitering_time
        self.loitering_radius = loitering_radius
        self.max_stationary_path = max_stationary_path
        self.restricted_zone = restricted_zone

        self.track_state = {}
        self.triggered = set()
        self.incidents = []

        # Crowd state
        self.crowd_active = False

    # ----------------------------------------------------------
    # Utility
    # ----------------------------------------------------------

    @staticmethod
    def distance(p1, p2):

        return math.sqrt(
            (p1[0] - p2[0]) ** 2 +
            (p1[1] - p2[1]) ** 2
        )

    # ----------------------------------------------------------
    # Incident creation
    # ----------------------------------------------------------

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
            "Timestamp_seconds": round(float(timestamp), 2),
            "Frame": int(frame),
            "Severity": severity,
            "Status": "OPEN"
        }

        self.incidents.append(item)

        return item

    # ----------------------------------------------------------
    # Main event processing
    # ----------------------------------------------------------

    def process(self, objects, frame_number, timestamp):

        people = [
            obj for obj in objects
            if obj.get("class_id") == 0
        ]

        # ======================================================
        # 1. CROWD DETECTION
        # ======================================================

        current_crowd = len(people) >= self.crowd_threshold

        # Trigger only when crowd condition STARTS
        if current_crowd and not self.crowd_active:

            self.incident(
                event="Crowd Detected",
                frame=frame_number,
                timestamp=timestamp,
                severity="MEDIUM"
            )

        # Update crowd state
        self.crowd_active = current_crowd

        # ======================================================
        # 2. PERSON TRACKING / LOITERING
        # ======================================================

        for obj in people:

            track_id = obj.get("track_id")
            center = obj.get("center")

            if track_id is None or center is None:
                continue

            # --------------------------------------------------
            # New track
            # --------------------------------------------------

            if track_id not in self.track_state:

                self.track_state[track_id] = {
                    "anchor": center,
                    "last_position": center,
                    "stationary_since": timestamp,
                    "path_length": 0.0,
                    "last_seen": timestamp
                }

            state = self.track_state[track_id]

            # --------------------------------------------------
            # Movement calculation
            # --------------------------------------------------

            step_distance = self.distance(
                center,
                state["last_position"]
            )

            displacement = self.distance(
                center,
                state["anchor"]
            )

            # Accumulate actual movement
            state["path_length"] += step_distance

            # --------------------------------------------------
            # LOITERING
            #
            # Person must:
            # 1. Stay near the same area
            # 2. Not travel too far
            # 3. Remain there for required duration
            # --------------------------------------------------

            still_in_area = (
                displacement <= self.loitering_radius
            )

            not_traveling = (
                state["path_length"] <= self.max_stationary_path
            )

            duration = (
                timestamp - state["stationary_since"]
            )

            if still_in_area and not_traveling:

                if duration >= self.loitering_time:

                    key = ("loiter", track_id)

                    if key not in self.triggered:

                        self.triggered.add(key)

                        self.incident(
                            event="Loitering Detected",
                            frame=frame_number,
                            timestamp=timestamp,
                            track_id=track_id,
                            severity="MEDIUM"
                        )

            else:

                # Person moved away.
                # Start a fresh stationary period.
                state["anchor"] = center
                state["stationary_since"] = timestamp
                state["path_length"] = 0.0

            state["last_position"] = center
            state["last_seen"] = timestamp

            # ==================================================
            # 3. RESTRICTED AREA INTRUSION
            # ==================================================

            if self.restricted_zone:

                x1, y1, x2, y2 = self.restricted_zone

                x, y = center

                inside_zone = (
                    x1 <= x <= x2
                    and
                    y1 <= y <= y2
                )

                if inside_zone:

                    key = ("intrusion", track_id)

                    if key not in self.triggered:

                        self.triggered.add(key)

                        self.incident(
                            event="Restricted Area Intrusion",
                            frame=frame_number,
                            timestamp=timestamp,
                            track_id=track_id,
                            severity="HIGH"
                        )

        # ------------------------------------------------------
        # Remove stale tracks
        # ------------------------------------------------------

        stale_ids = []

        for track_id, state in self.track_state.items():

            if timestamp - state["last_seen"] > 3:

                stale_ids.append(track_id)

        for track_id in stale_ids:

            self.track_state.pop(track_id, None)

        return self.incidents


if __name__ == "__main__":
    print("✅ SENTINEL Event Engine ready")
'''

with open("/content/sentinel/app/events.py", "w") as f:
    f.write(events_code)

print("✅ SENTINEL Event Engine updated")
print()
print("Crowd: one incident when a crowd begins.")
print("Loitering: requires low movement + same area + 10 seconds.")
print("Intrusion: one incident per tracked person entering the zone.")
