import os
import subprocess


class SentinelEvidence:
    def __init__(
        self,
        evidence_dir="evidence",
        before_seconds=5,
        after_seconds=5
    ):
        self.evidence_dir = evidence_dir
        self.before_seconds = before_seconds
        self.after_seconds = after_seconds

        os.makedirs(self.evidence_dir, exist_ok=True)

    def create_clip(self, video_path, incident):
        incident_id = incident["Incident_ID"]
        timestamp = float(incident["Timestamp_seconds"])

        start_time = max(0, timestamp - self.before_seconds)
        duration = self.before_seconds + self.after_seconds

        output_path = os.path.join(
            self.evidence_dir,
            f"{incident_id}.mp4"
        )

        command = [
            "ffmpeg",
            "-y",
            "-ss", str(start_time),
            "-i", video_path,
            "-t", str(duration),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            "-an",
            output_path
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print(f"Evidence creation failed: {incident_id}")
            print(result.stderr)
            return None

        print(f"Evidence created: {output_path}")
        return output_path

    def create_all(self, video_path, incidents):
        evidence_files = []

        for incident in incidents:
            path = self.create_clip(video_path, incident)

            if path:
                evidence_files.append({
                    "Incident_ID": incident["Incident_ID"],
                    "Evidence_Path": path
                })

        return evidence_files


if __name__ == "__main__":
    print("SentinelEvidence ready")
