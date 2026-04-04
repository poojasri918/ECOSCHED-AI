# 🌱 EcoSched AI

## 🚀 One-line Pitch
EcoSched AI intelligently schedules workloads by deciding when to run, delay, or shift tasks to minimize carbon emissions in real time.

---

## 🧠 What Makes This Special

- Real-time carbon intensity simulation (UK API + dynamic environments)
- AI vs Baseline comparison (fair evaluation, not biased)
- Multi-factor optimization (carbon + cost + temperature)
- Interactive visualization dashboard
- Task difficulty modes (easy / medium / hard)

---

## 🚀 Problem

Modern data centers consume massive energy and contribute significantly to carbon emissions. Static scheduling fails to adapt to fluctuating carbon intensity, energy cost, and thermal conditions.This leads to inefficient energy usage and higher environmental impact.

---

## 💡 Solution

EcoSched AI uses a decision-based system to:

- Monitor carbon intensity, temperature, and cost
- Dynamically decide whether to:
  - Run workloads
  - Delay execution
  - Shift workloads to better conditions
  - Balance between perfomance,cost, and sustainability

---

## 📁 Project Structure

ecosched/ 

│── app.py              # Flask API + UI 

│── env.py              # Environment simulation 

│── inference.py        # AI decision logic 

│── evaluate.py         # AI vs baseline comparison 

│── grader.py           # Scoring system 

│── train_dqn.py        # RL training (if used)

│── openenv.yaml        # Environment spec 

│── requirements.txt    # Dependencies 

│── Dockerfile          # Container setup 

│── README.md

---


## 🧠 Key Features

- Real-time carbon-aware simulation
- Multi-objective optimization (carbon + cost + thermal)
- Job scheduling with deadlines
- AI vs Baseline comparison
- Explainable decision insights
- Real-time decision adaptation

---

## 📊 Evaluation

The system compares:

- AI-driven scheduling
- Baseline heuristic scheduling

Metrics:
- Average carbon usage
- Sustainability score

This system ensures fair comparison by introducing variability so that baseline can outperform AI in certain scenarios.

---

## 🔌 API Endpoints

-GET /data --> Run full simulations

-GET/reset --> Reset environment

-POST/step --> Take action (0,1,2)

-GET/state --> Get current state


## ⚙️ How to Run

```bash
pip install -r requirements.txt
python app.py

Open:
http://127.0.0.1:5000

---

🏆 Why It Matters

EcoSched AI demonstrates how intelligent scheduling can:

- Reduce emissions
- Improve efficiency
- Adapt to real-world variability

---

🎯 Design Philosophy

The system is intentionally designed so that AI does not always win, ensuring realistic evaluation under varying conditions.

---

📌 Tech Stack

- Python (Flask)
- JavaScript (Chart.js)
- Simulation-based AI logic

```

##🎮 Action Space

-0 --> Delay workload

-1 --> Run workload

-2 --> Shift workload

---


##🚀 Future Improvements

-Integrate reinforcement learning (DQN/PPO)

-Use real cloud workload datasets

-Multi-region optimization

-Deploy as scalable service

---

