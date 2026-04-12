🌱 EcoSched AI

Intelligent Carbon-Aware Workload Scheduler

---

🚀 One-line Pitch

EcoSched AI intelligently schedules workloads by deciding when to run, delay, or shift tasks to minimize carbon emissions in real time.

---

🌟 What Makes This Special

- ⚡ Real-time carbon intensity simulation (multi-region support)
- 🤖 AI vs Baseline comparison (fair, unbiased evaluation)
- 📊 Multi-factor optimization (carbon + cost + temperature)
- 📈 Interactive dashboard with live graphs
- 🎯 Action-based decision system (Run / Delay / Shift)
- 🔄 Real-time adaptive system (dynamic updates)

---

❗ Problem

Modern data centers consume massive energy and contribute significantly to carbon emissions.

Static scheduling fails to adapt to:

- Changing carbon intensity
- Fluctuating electricity prices
- Thermal conditions

➡️ Result: inefficient energy usage and higher environmental impact.

---

💡 Solution

EcoSched AI uses a decision-based system to:

- Monitor:
  
  - Carbon intensity
  - Temperature
  - Energy cost

- Dynamically decide whether to:
  
  - ▶️ Run workloads
  - ⏸ Delay execution
  - 🔁 Shift workloads to better conditions

- Balance:
  
  - Performance
  - Cost
  - Sustainability

---

🧠 System Architecture

- Backend: Flask API (simulation engine)
- AI Logic: Rule-based + adaptive decision system
- Frontend: React + Vite + Chart.js
- Visualization: Real-time graphs
- Containerization: Docker
- Deployment: Hugging Face Spaces

---

📡 API Endpoints

"GET /data"

Runs full simulation

Query Params:

- "task": easy | medium | hard
- "region": uk | india | us | low | high

---

"POST /step"

Executes one step

Body:

{
  "action": 0 | 1 | 2
}

---

"GET /state"

Returns current system state

---

"GET /reset"

Resets environment

---

📊 Features in UI

- AI vs Baseline comparison
- Carbon emission graph
- Price trend graph
- Temperature trend graph
- Decision logs
- Sustainability score
- Live system metrics

---

📁 Project Structure

ecosched/
│
├── server/
│   └── app.py              # Flask backend
│
├── ecosched-dashboard/
│   ├── src/                # React frontend
│   └── package.json
│
├── inference.py            # AI decision logic
├── grader.py               # Evaluation system
├── openenv.yaml            # Environment config
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container setup
├── pyproject.toml
└── README.md

---

⚙️ How to Run Locally

🔹 Backend (Flask)

pip install -r requirements.txt
python server/app.py

Runs on:
👉 http://127.0.0.1:5000

---

🔹 Frontend (React + Vite)

cd ecosched-dashboard
npm install
npm run dev

Runs on:
👉 http://localhost:5173

---

🐳 Docker Setup

docker build -t ecosched-ai .
docker run -p 8000:8000 ecosched-ai

Runs on:
👉 http://localhost:8000

---

🌐 Deployment

- GitHub: https://github.com/poojasri918/ECOSCHED-AI
- Hugging Face Space: https://huggingface.co/spaces/pooja-918/ecosched-ai

---

📈 Example Output

- AI Avg Carbon: 0.42
- Baseline Avg Carbon: 0.51
- Improvement: ~17%

---

🔍 Key Insight

The model does not always win — ensuring realistic, unbiased evaluation rather than overfitting to a single strategy.

---

🎯 Why It Matters

EcoSched AI demonstrates how intelligent scheduling can:

- 🌍 Reduce carbon emissions
- ⚡ Improve efficiency
- 🔁 Adapt to real-world variability

---

🧩 Tech Stack

- Python (Flask)
- React (Vite)
- Chart.js
- Docker
- NumPy

---

🏁 Final Note

This project focuses on real-world decision intelligence, not just optimization — balancing sustainability, cost, and performance dynamically.

---