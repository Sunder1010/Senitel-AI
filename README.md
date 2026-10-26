SENTINEL AI

AI Video Safety & Operations Monitoring Platform

SENTINEL is an AI-powered video safety and operations monitoring platform designed to transform continuous CCTV video into actionable, explainable incidents.

Instead of requiring security personnel to continuously watch CCTV footage, SENTINEL uses computer vision, object tracking, temporal analysis, and spatial rules to identify meaningful events and generate evidence for review.

From continuous video to actionable intelligence.

⸻

🚨 Why SENTINEL?

Traditional CCTV systems primarily provide video recording and live viewing.

The problem is that humans cannot continuously monitor every camera and every frame.

SENTINEL adds an intelligent monitoring layer:

CCTV / Video
     ↓
AI Detection
     ↓
Object Tracking
     ↓
Temporal & Spatial Analysis
     ↓
Incident Detection
     ↓
Evidence Generation
     ↓
Incident Database

This allows organizations to focus on events that require attention, rather than manually reviewing hours of footage.

⸻

🎯 Project Vision

SENTINEL is being developed as a scalable AI safety and operations platform that can work with existing CCTV infrastructure.

Potential environments include:

* 🎓 Educational campuses
* 🏢 Offices
* 🏭 Warehouses
* 🏬 Retail environments
* 🏘️ Residential communities
* 🚗 Parking facilities
* 🏗️ Industrial environments

The initial real-world pilot target is an authorized educational-campus CCTV environment.

⸻

🧠 Core Capabilities

Object Detection

Uses YOLO for real-time object detection.

Multi-Object Tracking

Uses ByteTrack to maintain object identities across video frames.

Crowd Detection

Detects when the number of people in a monitored scene crosses a configured threshold.

Loitering Detection

Tracks how long an individual remains within the monitored scene and generates an incident when the configured duration is exceeded.

Restricted-Area Intrusion

Allows a camera to have a configured restricted zone.

If a tracked person enters the zone, SENTINEL can generate a high-severity intrusion incident.

Evidence Generation

For detected incidents, SENTINEL automatically creates an evidence video clip containing footage around the incident timestamp.

Incident Database

Incidents are stored with information such as:

* Incident ID
* Event type
* Camera
* Timestamp
* Severity
* Person/track ID
* Status
* Evidence reference

⸻

🏗️ System Architecture

                    CCTV / Video Source
                            │
                 ┌──────────┴──────────┐
                 │                     │
              MP4 Video            RTSP CCTV
                 │                     │
                 └──────────┬──────────┘
                            ↓
                     OpenCV Reader
                            ↓
                      YOLO Detection
                            ↓
                     ByteTrack Tracking
                            ↓
                  Event Detection Engine
                            ↓
                       Incident
                            ↓
                ┌───────────┴───────────┐
                ↓                       ↓
          SQLite Database         Evidence Clip
                │
                ↓
          Future Web Application

⸻

🔬 Current Detection Pipeline

Video Frame
    ↓
YOLO
    ↓
Person Detection
    ↓
ByteTrack
    ↓
Track ID + Position
    ↓
Temporal / Spatial Rules
    ↓
Incident
    ↓
Severity Classification
    ↓
SQLite
    ↓
Evidence Generation

⸻

🛠️ Technology Stack

Technology	Purpose
Python	Core development
OpenCV	Video processing
Ultralytics YOLO	Object detection
ByteTrack	Multi-object tracking
SQLite	Incident persistence
FFmpeg	Evidence/video encoding
GitHub	Version control

⸻

📂 Project Structure

Senitel-AI/
│
├── app/
│   ├── database.py
│   ├── detector.py
│   ├── events.py
│   ├── tracker.py
│   └── video_processor.py
│
├── evidence.py
├── zones.py
├── run.py
├── requirements.txt
├── .gitignore
├── README.md
└── SENTINEL_GITHUB.zip

The project structure is being actively refined as the system moves from prototype development toward real-world deployment.

⸻

🎥 Supported Video Sources

SENTINEL is being designed to support:

* Recorded MP4 video
* Webcam input
* RTSP/IP camera streams

The current development and testing pipeline has been validated using recorded video.

The next major milestone is integration with an authorized college CCTV/RTSP stream.

⸻

📊 Incident Model

Each incident contains structured information:

Incident ID
     ↓
Event Type
     ↓
Camera
     ↓
Timestamp
     ↓
Severity
     ↓
Track ID
     ↓
Status
     ↓
Evidence

Example:

SNT-20261024-063842-0007
Event:       Loitering Detected
Camera:      Camera_01
Severity:    MEDIUM
Status:      OPEN
Timestamp:   18.57 seconds

⸻

🎥 Evidence Generation

SENTINEL does not only report that an event happened.

It can automatically generate a short evidence clip around the incident.

Example:

Incident detected
       ↓
Incident timestamp
       ↓
5 seconds before
       +
5 seconds after
       ↓
Evidence clip

This makes incidents easier to review and verify.

⸻

🔐 Privacy & Responsible AI

SENTINEL is designed around objective event detection rather than identity recognition.

The system does not require:

* Face recognition
* Identity profiling
* Facial identification
* “Suspicious person” classification based on appearance

The intended approach is to detect measurable events such as:

* Presence
* Movement
* Duration
* Crowd size
* Zone entry

Real-world deployments should only process CCTV streams with appropriate authorization and organizational approval.

⸻

🧪 Current Project Status

Phase 1 — AI Core

* [x]	YOLO detection
* [x]	ByteTrack tracking
* [x]	Crowd detection
* [x]	Loitering detection
* [x]	Restricted-zone detection
* [x]	Persistent zone configuration
* [x]	SQLite incident storage
* [x]	Evidence clip generation
* [x]	H.264 output generation
* [x]	End-to-end recorded-video testing

Phase 2 — Real-World Pilot

* [ ]	Authorized CCTV access
* [ ]	RTSP integration
* [ ]	Live camera testing
* [ ]	Camera configuration
* [ ]	Real-world event validation
* [ ]	Performance evaluation

Phase 3 — Application Platform

* [ ]	Backend API
* [ ]	Web dashboard
* [ ]	Camera management
* [ ]	Incident management
* [ ]	Alert system
* [ ]	User authentication
* [ ]	Multi-camera support
* [ ]	Reporting and analytics

⸻

🚀 Future Architecture

The long-term platform architecture is planned around:

                    CCTV Cameras
                         │
                         ↓
                   RTSP / Camera
                         │
                         ↓
                 SENTINEL AI Engine
                         │
              ┌──────────┼──────────┐
              ↓          ↓          ↓
           Detection   Events    Evidence
              │          │          │
              └──────────┼──────────┘
                         ↓
                    Backend API
                         ↓
                    PostgreSQL
                         ↓
                 SENTINEL Web App
                         ↓
              Security / Admin / Staff

Potential future technologies include:

* FastAPI
* React / Next.js
* PostgreSQL
* WebSocket-based live updates
* Email/SMS/notification integrations
* Multi-camera management
* Role-based access control
* Cloud or edge deployment

⸻

🏫 Initial Pilot

The first real-world deployment target is an authorized educational-campus CCTV environment.

The intended pilot workflow is:

College CCTV
     ↓
Authorized RTSP Stream
     ↓
SENTINEL AI Engine
     ↓
Real-Time Event Detection
     ↓
Incident Database
     ↓
Evidence
     ↓
Security / Operations Review

Only authorized camera streams should be connected to the system.

⸻

💻 Running SENTINEL

Install the required dependencies:

pip install -r requirements.txt

Run the video processor:

python run.py --input path/to/video.mp4

The system processes the video and generates:

* Processed video
* Detected incidents
* Incident records
* Evidence clips

⸻

📈 Project Direction

SENTINEL is being developed from a functional AI video-processing prototype toward a real-world safety and operations platform.

The focus is not simply detecting objects in video.

The goal is:

Detect → Understand → Record → Explain → Respond

⸻

👨‍💻 Developer

Sunder Vaidya

MCA — Artificial Intelligence & Machine Learning

Interests:

* Artificial Intelligence
* Machine Learning
* Computer Vision
* Data Science
* Intelligent Systems

⸻

📌 Project

SENTINEL AI — AI Video Safety & Operations Monitoring Platform

Status:

Prototype → Real-World Pilot

Built with Python, OpenCV, YOLO, ByteTrack, SQLite and FFmpeg.

⸻

⚠️ Disclaimer

SENTINEL is a developing prototype intended for authorized research, testing, and operational environments.

CCTV processing should only be performed with appropriate authorization, privacy controls, and organizational policies.
