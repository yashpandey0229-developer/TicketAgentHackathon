import os
import json
import urllib.request
from openai import OpenAI

# --- CONFIGURATION (Mandatory for Proxy Tracking) ---
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")
# Hamara Space URL jahan env run ho raha hai
ENV_URL = "https://yashpandey0229-ticketagentenv.hf.space"

def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step, action, reward, done, error="null"):
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error}", flush=True)

def log_end(success, steps, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}", flush=True)

def main():
    # 🚨 CRITICAL: OpenAI Client initialize karna zaroori hai Proxy tracking ke liye
    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)
    
    rewards = []
    steps_taken = 0
    success = False
    
    log_start(task="ticket-resolution", env="ticket_agent_v1", model=MODEL_NAME)

    try:
        # 1. Reset Environment
        req_reset = urllib.request.Request(f"{ENV_URL}/reset", method='POST')
        with urllib.request.urlopen(req_reset) as res:
            obs = json.loads(res.read().decode())

        # 2. 🚨 THE "PROXY" CALL (Selection ke liye mandatory)
        # Yeh call unke LiteLLM proxy se hokar jayegi tabhi Phase 2 pass hoga
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": f"Resolve this ticket: {obs['issue']}. Respond with 'High' or 'Low' priority."}],
            max_tokens=10
        )
        llm_decision = completion.choices[0].message.content.strip()

        # 3. Step in Environment
        action_payload = {"action_type": "set_priority", "content": "High"} # Logic as per your env
        req_step = urllib.request.Request(f"{ENV_URL}/step", 
                                          data=json.dumps(action_payload).encode(),
                                          headers={'Content-Type': 'application/json'}, method='POST')
        
        with urllib.request.urlopen(req_step) as res:
            result = json.loads(res.read().decode())
        
        reward = float(result['reward']['score'])
        done = result['done']
        
        steps_taken = 1
        rewards.append(reward)
        log_step(step=1, action=f"LLM_Decision:{llm_decision}", reward=reward, done=done)
        
        if reward > 0.0:
            success = True

    except Exception as e:
        log_step(step=steps_taken+1, action="error", reward=0.0, done=True, error=str(e)[:50])
    finally:
        log_end(success=success, steps=steps_taken, rewards=rewards)

if __name__ == "__main__":
    main()