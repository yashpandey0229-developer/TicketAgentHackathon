import requests
import time

# --- CONFIGURATION ---
# Tumhara Hugging Face Space URL (Iske peeche .hf.space lagana mat bhulna)
API_URL = "https://yashpandey0229-ticketagentenv.hf.space"

def run_baseline_test():
    print("🚀 Starting Baseline Agent Test...")
    
    try:
        # 1. Reset Environment
        print("\n[Step 1]: Resetting Environment to get a ticket...")
        response = requests.post(f"{API_URL}/reset")
        if response.status_code == 200:
            obs = response.json()
            print(f"✅ Observation Received: ID={obs['id']}, Issue='{obs['issue']}'")
        else:
            print(f"❌ Reset Failed: {response.text}")
            return

        # 2. Agent Decision Logic
        # Hum simulate kar rahe hain ki Agent ne decide kiya priority High karne ka
        action = {
            "action_type": "set_priority",
            "content": "High"
        }
        print(f"\n[Step 2]: Agent is taking action -> Setting priority to {action['content']}...")
        time.sleep(1) # Realistic feel ke liye

        # 3. Step call karna
        response = requests.post(f"{API_URL}/step", json=action)
        if response.status_code == 200:
            result = response.json()
            reward = result['reward']
            print(f"✅ Step Success! Reward Score: {reward['score']}")
            print(f"💬 Judge's Comment: {reward['comment']}")
            print(f"🏁 Environment Done: {result['done']}")
        else:
            print(f"❌ Step Failed: {response.text}")

    except Exception as e:
        print(f"⚠️ Error connecting to API: {e}")

    print("\n--- Baseline Test Completed ---")

if __name__ == "__main__":
    run_baseline_test()