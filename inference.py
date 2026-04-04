import os
import requests
import json
import time

# ---------------- ENV VARIABLES ----------------
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN", "dummy")

# ---------------- HELPERS ----------------
def reset_env():
    res = requests.get(f"{API_BASE_URL}/reset")
    return res.json()

def step_env(action):
    res = requests.post(f"{API_BASE_URL}/step", json={"action": action})
    return res.json()

# ---------------- POLICY (SMART BUT FAIR) ----------------
def policy(state):
    carbon = state["carbon"]
    temp = state["temp"]
    price = state["price"]

    # balanced decision (not biased)
    if carbon > 0.7 and price > 0.6:
        return 2  # shift
    elif price > 0.75:
        return 0  # delay
    elif temp > 0.75:
        return 2  # shift
    elif carbon < 0.3 and price < 0.5:
        return 1  # run
    else:
        return 1  # default run

# ---------------- RUN ----------------
def run_episode():
    state = reset_env()

    total_reward = 0
    steps = 50

    print("[START]")

    for i in range(steps):
        action = policy(state)

        result = step_env(action)

        state = result["state"]
        reward = result["reward"]
        done = result["done"]

        total_reward += reward

        print(f"[STEP] {json.dumps({'step': i, 'action': action, 'reward': reward})}")

        if done:
            break

    avg_reward = total_reward / steps

    # normalize to 0–1
    score = max(0.0, min(1.0, (avg_reward + 1) / 2))

    print("[END]")
    print(json.dumps({
        "score": score
    }))

# ---------------- MAIN ----------------
if __name__ == "__main__":
    run_episode()