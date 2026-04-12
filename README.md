🌱 EcoSched AI

AI-powered environment for carbon-aware workload scheduling in data centers.
This project simulates real-world scheduling decisions to minimize carbon emissions, cost, and thermal load.

---

🚀 Features

- Real-time carbon-aware scheduling simulation
- Supports 3 difficulty levels: Easy → Medium → Hard
- AI vs Baseline comparison
- Dynamic reward function with penalties & incentives
- Job scheduling with deadlines (real-world scenario)
- Interactive UI with graphs and insights
- REST API for environment interaction

---

🧠 Problem Statement

Data centers consume massive energy and contribute to carbon emissions.
This system simulates how AI can intelligently schedule workloads based on:

- Carbon intensity
- Electricity price
- Thermal constraints
- Job deadlines

---

🏗️ Project Structure

ecosched/
│
├── server/
│   ├── app.py              # FastAPI backend + UI
│
├── inference.py            # AI decision logic
├── grader.py               # Evaluation system
├── openenv.yaml           # Environment specification
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container setup
├── README.md               # Documentation
│
└── ecosched-dashboard/     # (Optional React frontend - not required)

---

⚙️ How to Run Locally

🔹 Backend (Main Application)

pip install -r requirements.txt
python server/app.py

👉 Runs on:

http://127.0.0.1:8000

👉 Open this URL in your browser to access the UI.

---

📡 API Endpoints

GET "/data"

Runs full simulation

Query params:

- "task" → easy | medium | hard
- "region" → uk | india | us | low | high

---

POST "/step"

Executes one step

Body:

{ "action": 0 | 1 | 2 }

---

GET "/reset"

Resets environment

GET "/state"

Returns current state

GET "/evaluate"

Returns AI vs baseline performance

GET "/health"

Health check

---

🎯 Tasks & Difficulty Levels

Level| Description
Easy| Basic carbon + cost optimization
Medium| Adds cost variability
Hard| Adds thermal constraints + job scheduling

---

🏆 Reward Function

Reward balances:

- Low carbon emission
- Low temperature
- Low cost

Includes:

- Penalties for bad decisions
- Bonuses for smart shifting
- Deadline penalties for missed jobs

---

📊 Evaluation

- AI vs baseline comparison
- Average carbon reduction
- Score between 0.0 → 1.0
- Improvement metric

---

🧪 Example Output

- AI Avg Carbon: 0.42
- Baseline Avg: 0.55
- Improvement: +23%

---

🐳 Docker Setup

docker build -t ecosched-ai .
docker run -p 8000:8000 ecosched-ai

Runs on:

http://localhost:8000

---

☁️ Deployment

- GitHub: https://github.com/poojasri918/ECOSCHED-AI
- Hugging Face Space: (if deployed)

---

✅ OpenEnv Compliance

This project implements:

- step(action) → observation, reward, done
- reset() → initial state
- state() → current state
- openenv.yaml specification

---

📌 Notes

- Frontend React app is optional and not required for running the system
- Backend includes full UI and API
- Designed for evaluation and benchmarking AI agents

---

👨‍💻 Author

EcoSched AI — Hackathon Submission 🚀