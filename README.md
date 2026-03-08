# NegotiAI — Autonomous Multi-Agent Negotiation System

NegotiAI is an interactive AI-driven negotiation simulator where autonomous Buyer and Seller agents negotiate deals using strategy, utility optimization, and market signals.

The system visualizes negotiation dynamics in a “War Room” dashboard that shows how autonomous agents converge toward a Pareto-optimal agreement.

This project demonstrates concepts from agentic AI systems, game theory, and automated negotiation.

---

# Features

### Multi-Agent System

The platform simulates multiple autonomous agents.

Buyer Agent
Goal: minimize the final price.
Uses strategies such as concession curves, aggressive bargaining, and deadline pressure.

Seller Agent
Goal: maximize profit above cost.
Uses strategies such as anchoring, counter-offers, dynamic discounting, and scarcity pressure.

Strategy Engine
Responsible for decision logic including:

* Utility optimization
* Nash bargaining solution
* Pareto optimal deal calculation
* Bayesian belief updates

Market Intelligence Agent
Simulates external market signals including:

* competitor pricing
* demand levels
* inventory conditions
* urgency factors

---

# Negotiation Model

The agents negotiate across multiple rounds.

Each round follows this process:

1. Buyer proposes an offer
2. Seller generates a counter-offer
3. Agents update beliefs about opponent constraints
4. Strategy engine evaluates utilities
5. Convergence is checked

When both offers converge within a threshold, the system calculates a final deal using a Pareto-optimal midpoint based on the Nash bargaining solution.

---

# Dashboard Capabilities

The NegotiAI War Room interface provides several visualization panels.

Live Negotiation Analytics

* Offer progression graph
* Utility comparison chart
* Gap analysis between buyer and seller offers

Market Intelligence Panel

Displays simulated signals such as:

* competitor pricing
* demand level
* inventory signal
* urgency factor

Agent Reasoning

Each negotiation round displays the reasoning steps of both agents.

Example reasoning:

Buyer Agent

* competitor price lower than seller ask
* demand signal indicates leverage
* adjusting offer upward slowly

Seller Agent

* buyer budget estimated from offers
* inventory scarcity detected
* holding high anchor price

Final Deal Summary

Displays:

* final negotiated price
* savings relative to original ask
* number of negotiation rounds
* buyer utility
* seller profit

---

# Agent Strategies

Buyer Strategies

* Concession
* Aggressive Bargaining
* Deadline Pressure
* Anchoring Low

Seller Strategies

* Anchoring High
* Counter Offer
* Dynamic Discount
* Scarcity Pressure

Different combinations of strategies produce different negotiation behaviors.

---

# System Architecture

```
Frontend (Streamlit Dashboard)
        │
Negotiation Controller
        │
Negotiation Environment
        │
 ├ Buyer Agent
 ├ Seller Agent
 ├ Strategy Engine
 └ Market Intelligence Agent
```

Core components implemented in the code:

```
BuyerAgent
SellerAgent
StrategyEngine
MarketAgent
NegotiationEnvironment
```

---

# Technology Stack

Python

Streamlit — interactive dashboard

Plotly — visualization and charts

Pandas — data processing

Game-theoretic optimization models

---

# Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/autonomous-negotiation-agent.git
cd autonomous-negotiation-agent
```

Install dependencies:

```bash
pip install streamlit pandas plotly
```

Or install using a requirements file:

```bash
pip install -r requirements.txt
```

---

# Running the Application

Start the application using:

```bash
streamlit run negotiation_agent.py
```

The application will open in your browser at:

```
http://localhost:8501
```

---

# How to Use

1. Choose a negotiation scenario
2. Select buyer strategy
3. Select seller strategy
4. Adjust urgency level
5. Set the maximum negotiation rounds
6. Launch the negotiation

The system will simulate the negotiation process and display the full analysis in the dashboard.

---

# Project Structure

```
autonomous-negotiation-agent
│
├ negotiation_agent.py
├ requirements.txt
└ README.md
```

---

# Example Scenarios

The system includes several predefined negotiation environments.

E-commerce bulk orders
SaaS subscription negotiations
Supply chain contracts
Freelance development contracts

Each scenario defines parameters such as budget, target price, seller floor price, and production cost.

---

# Example Negotiation Outcome

```
Original Ask: $10,000
Final Deal:   $7,200
Savings:      $2,800
Rounds:       6
Buyer Utility: $800
Seller Profit: $1,700
```

---

# Possible Future Improvements

Reinforcement learning negotiation strategies

LLM-based reasoning agents

Negotiation memory across sessions

Multi-party negotiation environments

Integration with real market data APIs

Online deployment for live demonstrations

---

# Author

Developed as a demonstration of autonomous multi-agent negotiation systems using optimization and strategy-based reasoning.
<img width="1907" height="876" alt="image" src="https://github.com/user-attachments/assets/af2a8f6d-1f12-474f-997b-7ddf8ceb1c5c" />
