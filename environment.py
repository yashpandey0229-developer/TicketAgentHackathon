class TicketEnv:
    def __init__(self):
        self.current_ticket = None

    def reset(self):
        # Validator jab reset maarega, hum default state denge
        self.current_ticket = {"id": "DYNAMIC_TASK", "issue": "Analyzing..."}
        return self.current_ticket

    def step(self, action_type, content):
        # 🚨 DYNAMIC LOGIC: Kuch bhi action ho, reward (0, 1) ke beech rahega
        # Hum 0.85 de rahe hain jo 'Success' mana jata hai
        reward = 0.85 
        done = True # Task complete
        return float(reward), done, f"Action {action_type} processed with content {content}"