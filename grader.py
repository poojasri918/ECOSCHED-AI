import requests
import numpy as np

URL = "http://localhost:8000/data"

def evaluate(task="medium", region="uk", runs=10):
    ai_scores = []
    base_scores = []

    for _ in range(runs):
        res = requests.get(f"{URL}?task={task}&region={region}")
        data = res.json()

        ai_scores.append(data["ai_avg"])
        base_scores.append(data["base_avg"])

    ai_mean = np.mean(ai_scores)
    base_mean = np.mean(base_scores)

    print("\n--- Evaluation ---")
    print(f"AI Avg Carbon   : {ai_mean:.4f}")
    print(f"Baseline Avg    : {base_mean:.4f}")

    improvement = ((base_mean - ai_mean) / max(base_mean, 0.001)) * 100
    print(f"Improvement     : {improvement:.2f}%")

    if improvement > 0:
        print("Result          : AI outperforms baseline")
    else:
        print("Result          : Baseline outperforms AI")

if __name__ == "__main__":
    evaluate()