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

## 🚀 Environment Overview
This Space provides a containerized API for AI agents to interact with a ticketing system. It is designed to test an agent's ability to prioritize, reply, and resolve issues autonomously.

### 🧠 Observation Space
The environment returns a JSON object:
- `id`: Unique Ticket ID (e.g., `T1`).
- `issue`: The customer's query text.
- `status`: Current state (`Open`, `Pending`, `Closed`).

### 🛠️ Action Space
Agents can perform:
1. **`set_priority`**: Assigns `Low`, `Medium`, or `High`.
2. **`reply`**: Sends a text response.
3. **`close`**: Marks the ticket as resolved.

---

## 🏗️ Technical Specs
- **Engine:** FastAPI / Python 3.10+
- **Standard:** OpenEnv Compliant (`/reset`, `/step`, `/state`)
- **Package:** Standardized via `pyproject.toml` for multi-mode deployment.

---