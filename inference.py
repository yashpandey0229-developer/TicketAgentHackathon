import os
import time
from openai import OpenAI

# --- CONFIGURATION (As per Hackathon Requirements) ---
# Ye variables automated grader provide karega, humein sirf inhe read karna hai
API_BASE_URL = os.getenv("API_BASE_URL", "https://yashpandey0229-ticketagentenv.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo") # Ya jo bhi model grader use kare
HF_TOKEN = os.getenv("HF_TOKEN", "your_token_here")

# OpenAI Client setup (Pointed to your OpenEnv API)
client = OpenAI(
    base_url=f"{API_BASE_URL}", 
    api_key=HF_TOKEN # Hackathon rules ke mutabiq token hi key hai
)

def run_inference():
    print("🚀 Starting Official Inference Test...")
    
    try:
        # 1. Reset Environment (Using standard POST request)
        # Note: OpenEnv standard mein reset hamesha initial observation deta hai
        import requests
        print("\n[Step 1]: Resetting Environment...")
        res = requests.post(f"{API_BASE_URL}/reset")
        if res.status_code == 200:
            obs = res.json()
            print(f"✅ Ticket Received: ID={obs['id']}, Issue='{obs['issue']}'")
        else:
            print(f"❌ Reset Failed: {res.text}")
            return

        # 2. Agent Logic (Using OpenAI Client for actions)
        # Grader expect karta hai ki agent API ke through 'step' call kare
        print(f"\n[Step 2]: Agent is taking action...")
        
        # Example action payload
        action = {
            "action_type": "set_priority",
            "content": "High"
        }

        # 3. Call Step Endpoint
        response = requests.post(f"{API_BASE_URL}/step", json=action)
        
        if response.status_code == 200:
            result = response.json()
            reward = result['reward']
            print(f"✅ Step Success! Reward: {reward['score']}")
            print(f"💬 Grader Feedback: {reward['comment']}")
            print(f"🏁 Episode Done: {result['done']}")
        else:
            print(f"❌ Step Failed: {response.text}")

    except Exception as e:
        print(f"⚠️ Connection Error: {e}")

    print("\n--- Inference Completed ---")

if __name__ == "__main__":
    run_inference()