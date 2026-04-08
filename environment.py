TASKS = [
    {
        "id": "T1",
        "issue": "Customer says the refund is late and wants the ticket priority raised.",
        "priority": "Low",
        "status": "Open",
        "expected_action": "set_priority",
        "target_priority": "High",
    },
    {
        "id": "T2",
        "issue": "Customer is waiting for a status update and expects a concise reply.",
        "priority": "Medium",
        "status": "Open",
        "expected_action": "reply",
        "target_priority": "Medium",
    },
    {
        "id": "T3",
        "issue": "Customer confirms the issue is resolved and asks to close the ticket.",
        "priority": "High",
        "status": "Pending",
        "expected_action": "close",
        "target_priority": "High",
    },
]


class TicketEnv:
    def __init__(self):
        self.task_index = -1
        self.current_task = None
        self.current_ticket = None

    def _load_task(self, task_index):
        self.current_task = TASKS[task_index % len(TASKS)]
        self.current_ticket = {
            "id": self.current_task["id"],
            "issue": self.current_task["issue"],
            "priority": self.current_task["priority"],
            "status": self.current_task["status"],
        }

    def reset(self):
        self.task_index += 1
        self._load_task(self.task_index)
        return self.get_state()

    def get_state(self):
        if self.current_ticket is None:
            self.reset()
        return dict(self.current_ticket)

    def _score_action(self, action_type, content):
        action_type = (action_type or "").strip().lower()
        content = (content or "").strip().lower()
        expected_action = self.current_task["expected_action"]
        target_priority = self.current_task["target_priority"].lower()

        score = 0.12
        if action_type == expected_action:
            score += 0.5
        else:
            score += 0.15

        if action_type == "set_priority":
            if content in {"low", "medium", "high"}:
                score += 0.2
            if content == target_priority:
                score += 0.1
        elif action_type == "reply":
            if any(keyword in content for keyword in ["sorry", "update", "assist", "thanks", "apolog"]):
                score += 0.2
            if len(content) >= 25:
                score += 0.08
        elif action_type == "close":
            if any(keyword in content for keyword in ["resolved", "closed", "done", "confirmed"]):
                score += 0.2

        return max(0.05, min(score, 0.95))

    def step(self, action_type, content):
        if self.current_task is None:
            self.reset()

        reward = self._score_action(action_type, content)
        expected_action = self.current_task["expected_action"]
        done = True

        if action_type == expected_action:
            comment = f"Task {self.current_task['id']} handled with the expected action."
        else:
            comment = f"Task {self.current_task['id']} completed with a partial-match action."

        self.current_ticket["status"] = "Closed" if action_type == "close" else "Pending"

        info = {
            "task_id": self.current_task["id"],
            "expected_action": expected_action,
            "received_action": (action_type or "").strip().lower(),
        }
        return float(reward), done, comment, info