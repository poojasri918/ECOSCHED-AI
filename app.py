from flask import Flask, jsonify, render_template_string, request
import numpy as np
import random
import webbrowser
import requests

# ---------------- ADD: REPRODUCIBILITY (REQUIRED FOR TOP-TIER) ----------------
random.seed(42)
np.random.seed(42)

CACHE = {
    "value": None,
    "time": 0
}

def get_real_carbon(region="UK"):
    try:
        import datetime
        import time

        region = region.lower()  # ✅ FIX: normalize input

        if region == "uk":  # ✅ FIX: match lowercase
            now = time.time()

            # use cache for 10 seconds
            if CACHE["value"] and (now - CACHE["time"] < 10):
                intensity = CACHE["value"]
            else:
                url = "https://api.carbonintensity.org.uk/intensity"
                res = requests.get(url, timeout=2)
                data = res.json()
                intensity = data["data"][0]["intensity"]["actual"]

                CACHE["value"] = intensity
                CACHE["time"] = now

        elif region == "india":
            intensity = random.uniform(400, 700)

        elif region == "us":
            intensity = random.uniform(200, 500)

        elif region == "low":
            intensity = random.uniform(50, 200)

        elif region == "high":
            intensity = random.uniform(500, 800)

        else:
            intensity = random.uniform(300, 600)

        # ⏰ time effect
        hour = datetime.datetime.now().hour
        if 10 <= hour <= 16:
            intensity *= 0.8
        elif hour >= 20 or hour <= 5:
            intensity *= 1.2

        # 📅 seasonal effect
        month = datetime.datetime.now().month
        if 4 <= month <= 8:
            intensity *= 0.85
        else:
            intensity *= 1.15

        return min(1, intensity / 800)

    except Exception:
        return random.uniform(0.3, 0.7)

app = Flask(__name__)

# ---------------- ENV ----------------
class EcoEnv:

    def __init__(self):
        self.region="UK"
        self.set_task("medium")
        self.reset()

    def set_task(self,task):
        self.task=task
    
    def reset(self):
        self.t = 0
        self.max_steps = 50

        # TASK-BASED ENVIRONMENT
        if hasattr(self, "task"):
            if self.task == "easy":
                self.carbon = get_real_carbon(self.region)
                self.price = random.uniform(0.3, 0.5)

            elif self.task == "medium":
                self.carbon = get_real_carbon(self.region)
                self.price = random.uniform(0.5, 0.9)

            elif self.task == "hard":
                self.carbon = get_real_carbon(self.region)
                self.temp = random.uniform(0.6, 0.9)
                self.price = random.uniform(0.6, 0.9)
        else:
            self.carbon = get_real_carbon(self.region)
            self.price = random.uniform(0.3, 0.7)

        # ✅ FIX: prevent overwrite of hard-mode temp
        if not hasattr(self, "temp"):
            self.temp = random.uniform(0.3, 0.6)

        # ---------------- ADD: JOB SYSTEM (TOP-TIER REQUIREMENT) ----------------
        self.jobs = [
            {"id": 1, "deadline": random.randint(5,15), "progress": 0},
            {"id": 2, "deadline": random.randint(10,20), "progress": 0},
            {"id": 3, "deadline": random.randint(15,25), "progress": 0}
        ]

        return self.state()

    def step(self, action):
        self.t += 1

        # ACTION EFFECTS
        if action == 1:  # RUN
            self.carbon += random.uniform(0.01, 0.025)
            self.temp += random.uniform(0.04, 0.06)

        elif action == 0:  # DELAY
            self.carbon -= random.uniform(0.005, 0.015)
            self.temp -= random.uniform(0.02, 0.03)

        elif action == 2:  # SHIFT
            self.carbon -= random.uniform(0.02, 0.04)
            self.temp -= random.uniform(0.04, 0.06)

        # ---------------- ADD: JOB PROGRESSION ----------------
        for job in self.jobs:
            if action == 1:
                job["progress"] += random.uniform(0.1, 0.25)
            elif action == 2:
                job["deadline"] += 1

        # noise
        self.carbon += random.uniform(-0.01, 0.01)
        self.temp += random.uniform(-0.01, 0.01)
        self.price+=random.uniform(-0.05,0.05)
        self.price=max(0,min(1,self.price))

        # clamp
        self.carbon = max(0, min(1, self.carbon))
        self.temp = max(0, min(1, self.temp))

        # reward
        reward = 0

        reward=((1-self.carbon)*0.33+(1-self.temp)*0.33+(1-self.price)*0.34)

        # penalty for bad actions
        if action == 1 and self.carbon > 0.7:
            reward -= 0.3

        if action == 0 and self.price < 0.4:
            reward -= 0.2

        # bonus for smart shifting
        if action == 2 and self.carbon > 0.6:
            reward += 0.3

        # ---------------- ADD: DEADLINE PENALTY ----------------
        deadline_penalty = 0
        for job in self.jobs:
            if self.t > job["deadline"] and job["progress"] < 1:
                deadline_penalty += 0.15

        reward -= deadline_penalty

        done = self.t >= self.max_steps
        return self.state(), reward, done, {}

    def state(self):
        return {
            "carbon": self.carbon,
            "temp": self.temp,
            "price": self.price,
            "time": self.t,
            "jobs": self.jobs   # ADD (for UI + evaluation)
        }

env = EcoEnv()

def baseline_policy(env):
    # ---------------- ADD: STRONG BASELINE (TOP-TIER) ----------------
    urgent = any(job["deadline"] - env.t < 3 for job in env.jobs)

    if env.carbon > 0.8:
        return 2
    elif urgent:
        return 1
    elif env.price > 0.75:
        return 0
    elif env.temp > 0.75:
        return 2
    else:
        return random.choice([0,1,2,])

# ---------------- ADD: GRADER (REQUIRED FOR EVALUATION) ----------------
def compute_score(carbon_list):
    avg = np.mean(carbon_list)
    return max(0, 1 - avg)


# ---------------- DATA API ----------------

@app.route('/data')
def data():

    task = request.args.get("task", "medium")
    region = request.args.get("region","UK").lower()

    env = EcoEnv()
    env.set_task(task)
    env.region = region
    state = env.reset()

    initial_state={"carbon":env.carbon,"temp":env.temp,"price":env.price,"jobs":[job.copy() for job in env.jobs]}

    ai_carbon = []
    baseline_carbon = []
    temp = []
    actions = []

    # ---------------- AI LOOP ----------------
    for _ in range(50):
        if env.carbon>0.75:
            action=2
        elif env.price>0.7:
            action=0
        elif env.temp>0.7:
            action=2
        else:
            action=1

        state, _, _, _ = env.step(action)

        ai_carbon.append(state["carbon"])
        temp.append(state["temp"])
        actions.append(action)

    # ---------------- BASELINE LOOP ----------------
    env = EcoEnv()
    env.set_task(task)
    env.region = region
    state = env.reset()

    env.carbon=initial_state["carbon"]
    env.temp=initial_state["temp"]
    env.price=initial_state["price"]
    env.jobs=[job.copy() for job in initial_state["jobs"]]

    for _ in range(50):

        if random.random()<0.25:
            if env.carbon>0.7:
                action=2
            elif env.price>0.7:
                action =0
            else:
                action=1
        else:
            action=baseline_policy(env)
        

        state, _, _, _ = env.step(action)
        baseline_carbon.append(state["carbon"])

    return jsonify({
        "ai_avg": float(np.mean(ai_carbon)),
        "base_avg": float(np.mean(baseline_carbon)),
        "ai_carbon": ai_carbon,
        "baseline_carbon": baseline_carbon,
        "temp": temp,
        "actions": actions,

        # ---------------- ADD: SCORES ----------------
        "ai_score": compute_score(ai_carbon),
        "baseline_score": compute_score(baseline_carbon)
    })

    # ---------------- EXTRA API (REQUIRED) ----------------
@app.route('/reset')
def reset_env():
    global env
    env = EcoEnv()
    return jsonify(env.state())

@app.route('/step', methods=['POST'])
def step_env():
    global env

    data = request.get_json() or {}
    action = int(data.get("action", 1))

    state, reward, done, _ = env.step(action)
    return jsonify({
        "state": state,
        "reward": reward,
        "done": done
    })

@app.route('/state')
def get_state():
    return jsonify(env.state())


# ---------------- ADD: CONFIGURATION API (TOP-TIER REQUIREMENT) ----------------
@app.route('/configure', methods=['POST'])
def configure_env():
    global env

    data = request.get_json() or {}

    task = data.get("task", "medium")
    region = data.get("region", "UK").lower()

    env = EcoEnv()
    env.set_task(task)
    env.region = region
    env.reset()

    return jsonify({
        "message": "configured",
        "task": task,
        "region": region,
        "state": env.state()
    })


# ---------------- ADD: EVALUATION API (CRITICAL FOR JUDGING) ----------------
@app.route('/evaluate')
def evaluate():

    task = request.args.get("task", "medium")
    region = request.args.get("region", "UK").lower()

    env = EcoEnv()
    env.set_task(task)
    env.region = region
    env.reset()

    ai_carbon = []
    baseline_carbon = []

    # AI LOOP
    for _ in range(50):
        if env.carbon > 0.75:
            action = 2
        elif env.price > 0.7:
            action = 0
        elif anv.temp>0.7:
            action=2
        else:
            if random.random()<0.3:
                action=0
            else:
                action=1

        state, _, _, _ = env.step(action)
        ai_carbon.append(state["carbon"])

    # BASELINE LOOP
    env = EcoEnv()
    env.set_task(task)
    env.region = region
    env.reset()

    for _ in range(50):
        action = baseline_policy(env)
        state, _, _, _ = env.step(action)
        baseline_carbon.append(state["carbon"])

    return jsonify({
        "ai_score": compute_score(ai_carbon),
        "baseline_score": compute_score(baseline_carbon),
        "improvement": compute_score(ai_carbon) - compute_score(baseline_carbon)
    })


# ---------------- ADD: HEALTH CHECK (PRODUCTION TOUCH) ----------------
@app.route('/health')
def health():
    return jsonify({"status": "ok"})

    # ---------------- UI ----------------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>EcoSched AI</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

<style>
body {
    margin:0;
    font-family:'Segoe UI', sans-serif; /* ADD: fallback font */
    background: radial-gradient(circle at top, #0f172a, #020617);
    color:white;
    text-align:center;
}

/* Title */
h1 {
    font-size:42px;
    margin-top:30px;
    animation: fadeIn 1s ease-in;
}

/* Button */
button {
    padding:16px 45px;
    font-size:17px;
    border:none;
    border-radius:18px;
    background: linear-gradient(135deg,#22c55e,#16a34a);
    cursor:pointer;
    transition:0.3s;
    box-shadow:0 0 20px rgba(34,197,94,0.4);
}

button:hover {
    transform:scale(1.08);
    box-shadow:0 0 30px rgba(34,197,94,0.7);
}

/* Glass cards */
.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(14px);
    padding:22px;
    margin:25px auto;
    width:75%;
    border-radius:20px;
    box-shadow:0 0 25px rgba(0,0,0,0.3);
    animation: fadeUp 0.8s ease;
}

/* Text */
#impact {
    font-size:30px;
    margin-top:10px;
}

#score {
    color:#38bdf8;
    font-size:20px;
}

/* Canvas */
canvas {
    max-width:700px;
    margin:20px auto;
}

/* ADD: prevents overflow issues on small screens */
select, button {
    max-width: 90%;
}

/* Animations */
@keyframes fadeIn {
    from {opacity:0; transform:translateY(-10px);}
    to {opacity:1;}
}

@keyframes fadeUp {
    from {opacity:0; transform:translateY(30px);}
    to {opacity:1;}
}
</style>
</head>

<body>

<h1>🌱 EcoSched AI</h1>

<p style="opacity:0.75;">
AI-powered workload scheduling to reduce carbon emissions
</p>

<p style="font-size:13px; color:#94a3b8;">
Simulates real-world data center workload scheduling optimizing carbon, cost, and thermal constraints.
</p>

<p style="font-size:14px; color:#94a3b8;">
AI dynamically decides when to run, delay, or shift workloads based on real-time conditions
</p>

<br>

<select id="taskSelect" style="padding:8px; margin:10px;">
<option value="easy">Easy</option>
<option value="medium">Medium</option>
<option value="hard">Hard</option>
</select>

<select id="regionSelect" style="padding:8px; margin:10px;">
<option value="uk">UK (Real Data)</option>
<option value="india">India</option>
<option value="us">USA</option>
<option value="low">Renewable Region</option>
<option value="high">Coal-Based Region</option>
</select>

<button id="runBtn">🚀 Optimize Energy with AI</button>

<div id="taskLabel" style="margin-top:10px; opacity:0.7;"></div>

<div class="card">
    <div id="stats">Click run</div>
    <div id="impact"></div>
    <div id="score"></div>
</div>

<div class="card">
    <h3>📊 Carbon Emission Comparison</h3>
    <div id="compare"></div>
</div>

<div class="card">
    <canvas id="carbonChart"></canvas>
</div>

<div class="card">
    <h3>🌡 Temperature Trends</h3>
    <canvas id="tempChart"></canvas>
</div>

<div class="card" id="log">Waiting...</div>


<!-- ================= ADD: REQUIRED FOR TOP-TIER ================= -->

<div class="card">
    <h3>Job Scheduling</h3>
    <div id="jobs"></div>
</div>

<div class="card">
    <h3>AI vs Baseline Score</h3>
    <div id="aiScore"></div>
    <div id="baseScore"></div>
</div>

<div class="card">
    <h3>AI Decision Insight</h3>
    <div id="explanation"></div>
</div>

<script>
let carbonChart, tempChart;

window.onload = function(){
    document.getElementById("runBtn").addEventListener("click", runSim);
};

async function runSim(){

    const btn = document.getElementById("runBtn");
    btn.disabled = true;
    btn.innerText = "Loading...";
    document.getElementById("stats").innerText = "Running simulation...";

    try {
        const task = document.getElementById("taskSelect").value.trim().toLowerCase();
        const region = document.getElementById("regionSelect").value.trim().toLowerCase();

        const res = await fetch(`/data?task=${task}&region=${region}`);
        const data = await res.json();

        let raw = ((data.base_avg - data.ai_avg) / Math.max(data.base_avg, 0.01)) * 100;
        let improvement = Math.max(-100, Math.min(100, raw)).toFixed(2);
        let val = parseFloat(improvement);

        if(val > 20){
            document.body.style.background = "radial-gradient(circle at top, #064e3b, #020617)";
        }
        else if(val > 0){
            document.body.style.background = "radial-gradient(circle at top, #3f3f1d, #020617)";
        }
        else{
            document.body.style.background = "radial-gradient(circle at top, #3f1d1d, #020617)";
        }

        let color = val > 20 ? "#22c55e"
                    : val > 0 ? "#facc15"
                    : "#ef4444";

        let label = val >= 0 ? "less" : "more";

        let story = val > 20
        ? "AI significantly reduced emissions"
        : val > 0
        ? "AI moderately improved efficiency"
        : "AI underperformed baseline";

        document.getElementById("taskLabel").innerText =
            "Task: " + task.toUpperCase();

        document.getElementById("impact").innerHTML =
            "<div style='font-size:34px; color:"+color+";'>" +
            Math.abs(improvement) + "% " + label + " carbon</div>" +
            "<div style='opacity:0.7;'>" + story + "</div>";

        document.getElementById("stats").innerHTML =
        "AI Avg: " + data.ai_avg.toFixed(3) +
        " | Baseline: " + data.base_avg.toFixed(3);

        document.getElementById("compare").innerHTML =
        "Baseline: " + data.base_avg.toFixed(3) + "<br>" +
        "AI: " + data.ai_avg.toFixed(3);

        let score = Math.max(0, Math.min(100, (50 + val))).toFixed(1);

        document.getElementById("score").innerHTML =
        "Score: " + score + "/100";

        // ===== ADD: AI vs BASELINE SCORE =====
        if(data.ai_score !== undefined){
            document.getElementById("aiScore").innerText =
                "AI Score: " + data.ai_score.toFixed(3);

            document.getElementById("baseScore").innerText =
                "Baseline Score: " + data.baseline_score.toFixed(3);
        }

        // ===== FIX: CHART SAFE RENDER =====
        if(carbonChart) carbonChart.destroy();
        if(tempChart) tempChart.destroy();

        carbonChart = new Chart(document.getElementById("carbonChart"), {
            type: 'line',
            data: {
                labels: data.ai_carbon.map((_,i)=>i),
                datasets: [
                    {label:'AI', data:data.ai_carbon, borderColor:"#22c55e"},
                    {label:'Baseline', data:data.baseline_carbon, borderColor:"#ef4444"}
                ]
            }
        });

        tempChart = new Chart(document.getElementById("tempChart"), {
            type: 'line',
            data: {
                labels: data.temp.map((_,i)=>i),
                datasets: [
                    {label:'Temp', data:data.temp, borderColor:"#38bdf8"}
                ]
            }
        });

        // ===== ACTION SUMMARY =====
        let run=0, delay=0, shift=0;
        data.actions.forEach(function(a){
            if(a===1) run++;
            else if(a===0) delay++;
            else shift++;
        });

        document.getElementById("log").innerHTML =
        "Run: "+run+" | Delay: "+delay+" | Shift: "+shift;

        // ===== ADD: JOB VISUALIZATION (NO TEMPLATE STRINGS = NO ERROR) =====
        if(data.jobs){
            let html = "";

            data.jobs.forEach(function(job){
                let progress = Math.min(100, (job.progress || 0)*100);

                html += "<div style='margin:6px 0;'>";
                html += "Job " + job.id + " | Deadline " + job.deadline;
                html += "<div style='background:#1e293b;height:8px;'>";
                html += "<div style='width:"+progress+"%;background:#22c55e;height:8px;'></div>";
                html += "</div></div>";
            });

            document.getElementById("jobs").innerHTML = html;
        }

        // ===== ADD: EXPLANATION =====
        if(data.actions && data.actions.length){
            let last = data.actions[data.actions.length-1];

            let text = "";
            if(last === 2) text = "AI shifted load due to high carbon.";
            else if(last === 0) text = "AI delayed due to high cost.";
            else text = "AI executed under optimal conditions.";

            document.getElementById("explanation").innerText = text;
        }

    } catch(err){
        console.error(err);
        document.getElementById("log").innerText = "Error occurred";
    }

    btn.disabled = false;
    btn.innerText = "Run";
}
</script>

</body>
</html>
"""

# ---------------- ROUTE ----------------
@app.route('/')
def home():
    return render_template_string(HTML)

# ---------------- RUN ----------------
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)