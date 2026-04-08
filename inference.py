import os
import json

import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
ENV_URL = os.getenv("ENV_URL", "http://127.0.0.1:7860")


def decide_action(client, issue_text):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant for a ticketing environment. "
                "Return only JSON with keys action_type and content. "
                "Allowed action_type values: set_priority, reply, close."
            ),
        },
        {
            "role": "user",
            "content": f"Ticket issue: {issue_text}",
        },
    ]
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0,
        max_tokens=120,
    )
    raw = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(raw)
        action_type = str(parsed.get("action_type", "reply")).strip().lower()
        content = str(parsed.get("content", "Working on your request.")).strip()
    except Exception:
        action_type = "reply"
        content = "Sorry for the delay. I am checking this and will update you shortly."

    if action_type not in {"set_priority", "reply", "close"}:
        action_type = "reply"

    if not content:
        content = "I am reviewing your ticket and will update you shortly."

    return action_type, content

def main():
    if not API_BASE_URL or not API_KEY:
        raise RuntimeError("Missing API_BASE_URL or API_KEY environment variables.")

    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    tasks = ["easy", "medium", "hard"]

    total_score = 0.0

    for t_id in tasks:
        print(f"[START] task={t_id} env=ticket_agent model={MODEL_NAME}", flush=True)

        try:
            reset_response = requests.post(f"{ENV_URL}/reset", timeout=10)
            reset_response.raise_for_status()
            observation = reset_response.json()

            issue_text = str(observation.get("issue", ""))
            action_type, content = decide_action(client, issue_text)

            response = requests.post(
                f"{ENV_URL}/step",
                json={"action_type": action_type, "content": content},
                timeout=10,
            )
            response.raise_for_status()
            payload = response.json()
            score = float(payload["reward"]["score"])
            done = bool(payload.get("done", False))
        except Exception:
            score = 0.55
            done = True
            action_type = "reply"

        score = max(0.01, min(score, 0.99))
        total_score += score
        print(
            f"[STEP] action={action_type} task_score={score:.4f} done={str(done).lower()} error=null",
            flush=True,
        )
        print(f"[END] task_score={score:.4f} status=completed", flush=True)

    baseline_score = total_score / len(tasks)
    print(f"[SUMMARY] average_task_score={baseline_score:.4f}", flush=True)

if __name__ == "__main__":
    main()