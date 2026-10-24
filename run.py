
import sys
import os
import argparse

APP_DIR = "/content/sentinel/app"
sys.path.insert(0, APP_DIR)

from video_processor import SentinelVideoProcessor


def main():

    parser = argparse.ArgumentParser(
        description="SENTINEL AI Video Safety & Operations System"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to any compatible video file"
    )

    parser.add_argument(
        "--output",
        default="/content/sentinel/output/sentinel_result.mp4"
    )

    args = parser.parse_args()

    processor = SentinelVideoProcessor(
        input_video=args.input,
        output_video=args.output
    )

    incidents = processor.process()

    print("\nFINAL INCIDENTS")

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
