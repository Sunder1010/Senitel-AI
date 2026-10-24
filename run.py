
import argparse
import sys
from pathlib import Path


# Add the app directory to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parent
APP_DIR = PROJECT_ROOT / "app"

sys.path.insert(0, str(APP_DIR))

from video_processor import SentinelVideoProcessor


def main():

    parser = argparse.ArgumentParser(
        description="SENTINEL AI Video Safety & Operations Monitoring System"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to input video"
    )

    parser.add_argument(
        "--output",
        default="output/sentinel_result.mp4",
        help="Path for processed output video"
    )

    args = parser.parse_args()

    processor = SentinelVideoProcessor(
        input_video=args.input,
        output_video=args.output
    )

    incidents = processor.process()

    print("\n==============================")
    print("FINAL INCIDENTS")
    print("==============================")

    if not incidents:
        print("No incidents detected.")

    else:
        for incident in incidents:
            print(
                incident["Incident_ID"],
                "|",
                incident["Event"],
                "|",
                incident["Severity"]
            )


if __name__ == "__main__":
    main()
