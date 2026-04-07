import os
import json
import urllib.request
import urllib.error

# --- CONFIGURATION ---
API_BASE_URL = os.getenv("API_BASE_URL", "https://yashpandey0229-ticketagentenv.hf.space").rstrip('/')
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step, action, reward, done, error="null"):
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error}", flush=True)

def log_end(success, steps, rewards):
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}", flush=True)

def make_post_request(url, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), 
                                 headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def main():
    rewards = []
    steps_taken = 0
    success = False
    
    log_start(task="ticket-resolution", env="ticket_agent_v1", model=MODEL_NAME)

    try:
        # 1. Reset
        res_data = make_post_request(f"{API_BASE_URL}/reset", {})
        
        # 2. Step
        action_payload = {"action_type": "set_priority", "content": "High"}
        result = make_post_request(f"{API_BASE_URL}/step", action_payload)
        
        reward = float(result['reward']['score'])
        done = result['done']
        
        steps_taken = 1
        rewards.append(reward)
        log_step(step=1, action="set_priority:High", reward=reward, done=done)
        
        if reward > 0.0:
            success = True

    except Exception as e:
        # Error logging as per STDOUT format
        log_step(step=steps_taken+1, action="error", reward=0.0, done=True, error=str(e)[:50])
    finally:
        log_end(success=success, steps=steps_taken, rewards=rewards)

if __name__ == "__main__":
    main()