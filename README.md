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

│── app.py                  # Flask API + UI +environment+evaluation logic

│── inference.py            # AI decision logic 

│── grader.py               # Scoring system 

│── train_dqn.py            # RL training (if used)

│── openenv.yaml            # Environment spec 

│── requirements.txt        # Dependencies 

│── Dockerfile              # Container setup 

│── README.md

---

## 🎥 Demo

Run the project locally and open:

http://127.0.0.1:5000

### Features shown in UI:
- AI vs Baseline comparison
- Carbon emission graph
- Temperature trends
- AI decision breakdown (Run / Delay / Shift)
- Sustainability score

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

## 📊 Results

- AI reduces carbon emissions in most scenarios by intelligently avoiding high-emission periods  
- Baseline can outperform AI under certain conditions (ensures fair and unbiased evaluation)  
- System dynamically adapts based on carbon, cost, and temperature  

### Example Output:
- AI Avg Carbon: 0.42  
- Baseline Avg Carbon: 0.51  
- Improvement: ~17%  

### Key Insight:
The model does not always win, demonstrating realistic and balanced decision-making rather than overfitting to a single strategy.

---

## 🏗️ System Architecture

- Backend: Flask API (simulation engine)
- AI Logic: Rule-based decision + adaptive behavior
- Frontend: HTML + Chart.js visualization
- Data Source: Real-time UK carbon intensity API + simulated regions

## 🔌 API Endpoints

### GET /data
Runs full simulation

Query params:
- task: easy | medium | hard
- region: uk | india | us | low | high

---

### GET /reset
Resets environment

---

### POST /step
Body:
{
  "action": 0 | 1 | 2
}

---

### GET /state
Returns current state


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

## 🎮 Action Space

- 0 → Delay workload (reduces cost impact)
- 1 → Run workload (immediate execution)
- 2 → Shift workload (optimize for low carbon periods)

---


## 🚀 Future Improvements

- Integrate real reinforcement learning (DQN / PPO)
- Use real cloud workload datasets
- Add multi-region scheduling optimization
- Deploy as SaaS dashboard

---

## ⚠️ Limitations

- Uses simplified simulation instead of real data center workload
- AI is rule-based (not fully trained RL model)
- Carbon data is partially simulated outside UK

## NOTE : Environment simulation and evaluation logic are integrated within app.py for simplicity and efficiency.

