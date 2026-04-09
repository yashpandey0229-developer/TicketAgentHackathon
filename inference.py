import os
import json

import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")
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


class RemoteEnv:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")

    def reset(self):
        response = requests.post(f"{self.base_url}/reset", timeout=10)
        response.raise_for_status()
        return response.json()

    def step(self, action_type, content):
        response = requests.post(
            f"{self.base_url}/step",
            json={"action_type": action_type, "content": content},
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    def close(self):
        # Keep a close hook for guideline compatibility. Most OpenEnv APIs do not expose /close.
        return None


def _one_line(value):
    return " ".join(str(value).replace("\n", " ").replace("\r", " ").split())


def _format_bool(value):
    return "true" if bool(value) else "false"


def _format_reward(value):
    return f"{float(value):.2f}"


def _format_action(action_type, content):
    safe_action = _one_line(action_type)
    safe_content = _one_line(content).replace("'", '"')
    return f"{safe_action}('{safe_content}')"

def main():
    if not HF_TOKEN:
        raise ValueError("HF_TOKEN environment variable is required")

    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
    env = RemoteEnv(ENV_URL)

    task = "ticket-support"
    benchmark = "ticket_agent"
    print(f"[START] task={task} env={benchmark} model={_one_line(MODEL_NAME)}", flush=True)

    rewards = []
    steps = 0
    success = False
    last_action_error = None

    try:
        observation = env.reset()
        issue_text = str(observation.get("issue", ""))
        action_type, content = decide_action(client, issue_text)

        payload = env.step(action_type, content)
        score = float(payload["reward"]["score"])
        score = max(0.01, min(score, 0.99))
        done = bool(payload.get("done", False))
        rewards.append(score)
        steps = 1
        success = done
        print(
            f"[STEP] step=1 action={_format_action(action_type, content)} "
            f"reward={_format_reward(score)} done={_format_bool(done)} error=null",
            flush=True,
        )
    except Exception as exc:
        last_action_error = _one_line(str(exc))
        if not last_action_error:
            last_action_error = "unknown_error"
    finally:
        try:
            env.close()
        except Exception:
            pass

        rewards_str = ",".join(_format_reward(r) for r in rewards)
        print(
            f"[END] success={_format_bool(success)} steps={steps} rewards={rewards_str}",
            flush=True,
        )

if __name__ == "__main__":
    main()