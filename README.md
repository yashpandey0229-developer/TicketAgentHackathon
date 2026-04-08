---
title: TicketAgentEnv
emoji: 👁️
colorFrom: red
colorTo: purple
sdk: docker
pinned: false
tags:
- openenv
---

# 🎟️ TicketAgentEnv: Customer Support AI Simulation

A real-world environment for AI agents to handle customer support tickets following the **OpenEnv v0.1.0** specification.

---

## What This Environment Does
This project simulates three customer-support tasks with deterministic grading. Each task produces a reward strictly between 0 and 1, and the baseline runner reports a reproducible average score across all three tasks.

---

## 🚀 Environment Overview
This Space provides a containerized API for AI agents to interact with a ticketing system. It is designed to test an agent's ability to prioritize, reply, and resolve issues autonomously.

### 🧠 Observation Space
The environment returns a JSON object:
- `id`: Unique Ticket ID (e.g., `T1`).
- `issue`: The customer's query text.
- `priority`: Current priority (`Low`, `Medium`, `High`).
- `status`: Current state (`Open`, `Pending`, `Closed`).

### 🛠️ Action Space
Agents can perform:
1. **`set_priority`**: Assigns `Low`, `Medium`, or `High`.
2. **`reply`**: Sends a text response.
3. **`close`**: Marks the ticket as resolved.

### 🎯 Tasks
The environment rotates through three deterministic tasks:
1. Raise a refund ticket priority to `High`.
2. Reply to a customer with a concise status update.
3. Close a ticket after resolution is confirmed.

### 📈 Scoring
Rewards are shaped from partial progress signals and always stay within the open interval $(0,1)$.

---

## Baseline Runner
`inference.py` runs a reproducible baseline against the local API. It submits one action per task, records the returned reward, and prints an average score summary.

---

## 🏗️ Technical Specs
- **Engine:** FastAPI / Python 3.10+
- **Standard:** OpenEnv Compliant (`/reset`, `/step`, `/state`)
- **Package:** Standardized via `pyproject.toml` for multi-mode deployment.

## Local Run
1. Install dependencies from `requirements.txt`.
2. Start the API with `python server/app.py`.
3. Run `python inference.py` to reproduce the baseline scores.

---