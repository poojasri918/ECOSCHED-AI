import os
import json
import time
import random

# ---------------- ENV VARIABLES ----------------
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN", "dummy")

# ---------------- HELPERS ----------------
def reset_env():
    return{
        "carbon":0.4,
        "price":0.6,
        "temp":0.5
    }

def step_env(action, state):
    carbon = state.get("carbon", 0.5)
    price = state.get("price", 0.5)
    temp = state.get("temp", 0.5)

    # simulate realistic fluctuations
    import random
    carbon += random.uniform(-0.05, 0.05)
    price += random.uniform(-0.05, 0.05)
    temp += random.uniform(-0.03, 0.03)

    # apply action effects
    if action == 0:  # delay
        reward = -0.3
        carbon += 0.05

    elif action == 1:  # run
        reward = 1.0 - (carbon + price)  # penalize high cost/emission
        carbon -= 0.08

    elif action == 2:  # shift
        reward = 0.6 - abs(temp - 0.5)  # better if temp stable
        price -= 0.07

    # clamp values
    carbon = max(0, min(1, carbon))
    price = max(0, min(1, price))
    temp = max(0, min(1, temp))

    new_state = {
        "carbon": carbon,
        "price": price,
        "temp": temp
    }

    # dynamic termination
    done = (carbon < 0.2 and price < 0.3) or (carbon > 0.9)

    return {
        "state": new_state,
        "reward": reward,
        "done": done
    }
# ---------------- POLICY (SMART BUT FAIR) ----------------
def policy(state):
<<<<<<< HEAD
    carbon = state.get["carbon",0.5]
    temp = state.get["temp",0.5]
    price = state.get["price",0.5]
=======
    carbon = state.get("carbon", 0)
    price = state.get("price", 0)
    temp = state.get("temp", 0)
>>>>>>> 08d9150 (Final submission - EcoSched AI Dashboard)

    # normalize importance (weights)
    w_carbon = 0.5
    w_price = 0.3
    w_temp = 0.2

    # compute pressure score
    pressure = (w_carbon * carbon) + (w_price * price) + (w_temp * temp)

    # decision logic
    if pressure > 0.7:
        return 2  # shift (optimize load)
    elif price > 0.75:
        return 0  # delay (too expensive)
    elif carbon < 0.3 and price < 0.5:
        return 1  # run (ideal condition)
    else:
        return 1  # safe default

# ---------------- RUN ----------------
def run_episode():
    state = reset_env()

    total_reward = 0
    steps = 50

    print("[START]")

    for i in range(steps):
        action = policy(state)

        result = step_env(action,state)

        state = result["state"]
        reward = result["reward"]
        done = result["done"]

        total_reward += reward

        print(f"[STEP {i}] Action={action},Reward={round(reward,3)}")

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
