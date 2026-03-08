"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           NegotiAI — Autonomous Multi-Agent Negotiation System              ║
║           Run with:  streamlit run negotiation_agent.py                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import random
import math
import time
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG — must be first Streamlit call
# ──────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NegotiAI War Room",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS — dark cyberpunk theme
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&family=Space+Grotesk:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: #040d1a;
    color: #e2eaf5;
}
.stApp { background: #040d1a; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060f20 0%, #04080f 100%);
    border-right: 1px solid rgba(0,200,255,0.12);
}
[data-testid="stSidebar"] * { color: #c0d4e8 !important; }

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(0,40,80,0.4);
    border: 1px solid rgba(0,200,255,0.15);
    border-radius: 10px;
    padding: 12px 16px;
}
[data-testid="stMetricValue"] { color: #00d4ff !important; font-family: 'IBM Plex Mono' !important; font-size: 1.6rem !important; }
[data-testid="stMetricLabel"] { color: #4a7fa8 !important; font-size: 0.7rem !important; letter-spacing: 0.15em; text-transform: uppercase; }
[data-testid="stMetricDelta"] { color: #00ff96 !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #0066cc, #00aaff) !important;
    color: #040d1a !important;
    font-weight: 700 !important;
    font-family: 'IBM Plex Mono' !important;
    letter-spacing: 0.12em !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.2s !important;
    text-transform: uppercase !important;
}
.stButton > button:hover { box-shadow: 0 0 20px rgba(0,170,255,0.4) !important; transform: translateY(-1px) !important; }

/* Selectboxes / sliders */
.stSelectbox > div > div, .stSlider { background: rgba(0,20,50,0.8) !important; border-radius: 6px !important; }

/* Expanders */
.streamlit-expanderHeader {
    background: rgba(0,20,50,0.6) !important;
    border: 1px solid rgba(0,200,255,0.12) !important;
    border-radius: 8px !important;
    font-family: 'IBM Plex Mono' !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    color: #00d4ff !important;
}

/* Dataframes */
.stDataFrame { background: rgba(0,20,50,0.6) !important; border: 1px solid rgba(0,200,255,0.1) !important; border-radius: 8px !important; }

/* Custom cards */
.war-room-header {
    background: linear-gradient(135deg, rgba(0,40,100,0.6), rgba(0,80,120,0.3));
    border: 1px solid rgba(0,200,255,0.25);
    border-radius: 12px;
    padding: 20px 28px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 16px;
}
.agent-panel {
    background: rgba(8,20,45,0.85);
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 12px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.8;
}
.buyer-panel { border: 1px solid rgba(0,150,255,0.3); border-left: 3px solid #00aaff; }
.seller-panel { border: 1px solid rgba(255,120,0,0.3); border-left: 3px solid #ff8c00; }
.market-panel { border: 1px solid rgba(0,255,150,0.25); border-left: 3px solid #00ff96; }
.deal-panel {
    background: linear-gradient(135deg, rgba(0,255,150,0.05), rgba(0,100,200,0.08));
    border: 1px solid rgba(0,255,150,0.3);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.round-item-buyer {
    background: rgba(0,60,150,0.1);
    border: 1px solid rgba(0,150,255,0.2);
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.76rem;
}
.round-item-seller {
    background: rgba(150,60,0,0.1);
    border: 1px solid rgba(255,120,0,0.2);
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 8px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.76rem;
}
.tag-buyer { color: #00aaff; font-weight: 700; }
.tag-seller { color: #ff8c00; font-weight: 700; }
.tag-green { color: #00ff96; font-weight: 700; }
.tag-gold { color: #ffd700; font-weight: 700; }
.section-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: #4a7fa8;
    text-transform: uppercase;
    margin-bottom: 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid rgba(0,200,255,0.08);
}
.status-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    font-family: 'IBM Plex Mono', monospace;
    text-transform: uppercase;
}
.badge-live { background: rgba(0,255,100,0.1); border: 1px solid rgba(0,255,100,0.3); color: #00ff96; }
.badge-ready { background: rgba(0,150,255,0.1); border: 1px solid rgba(0,150,255,0.3); color: #00aaff; }
.badge-done { background: rgba(255,200,0,0.1); border: 1px solid rgba(255,200,0,0.3); color: #ffd700; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class ScenarioConfig:
    """Holds all parameters for a negotiation scenario."""
    name: str
    item: str
    buyer_budget: float
    buyer_target: float
    seller_ask: float
    seller_floor: float
    seller_cost: float
    currency: str = "$"


@dataclass
class MarketData:
    """Simulated market intelligence data."""
    competitor_price: float
    demand_level: str        # Low / Medium / High
    price_trend: str         # Rising / Stable / Falling
    inventory_signal: str    # Scarce / Normal / Surplus
    urgency_factor: float    # 0.0 – 1.0


@dataclass
class RoundRecord:
    """One complete round of negotiation."""
    round_num: int
    buyer_offer: float
    seller_offer: float
    buyer_thinking: List[str]
    seller_thinking: List[str]
    buyer_utility: float
    seller_utility: float
    gap: float


@dataclass
class NegotiationResult:
    """Final outcome of a completed negotiation."""
    deal_price: float
    total_rounds: int
    original_ask: float
    savings: float
    savings_pct: float
    buyer_utility: float
    seller_utility: float
    buyer_offers: List[float]
    seller_offers: List[float]
    rounds: List[RoundRecord]
    strategy_used_buyer: str
    strategy_used_seller: str
    converged: bool


# ══════════════════════════════════════════════════════════════════════════════
# PREDEFINED SCENARIOS
# ══════════════════════════════════════════════════════════════════════════════

SCENARIOS: dict[str, ScenarioConfig] = {
    "🛒 E-Commerce Bulk Order": ScenarioConfig(
        name="E-Commerce Bulk Order",
        item="500 units of Product SKU-X7",
        buyer_budget=8000, buyer_target=6000,
        seller_ask=10000, seller_floor=6500, seller_cost=5500,
    ),
    "☁️ SaaS Subscription": ScenarioConfig(
        name="SaaS Subscription",
        item="Enterprise Annual Plan",
        buyer_budget=3000, buyer_target=1800,
        seller_ask=4200, seller_floor=2200, seller_cost=800,
    ),
    "🏭 Supply Chain Contract": ScenarioConfig(
        name="Supply Chain Contract",
        item="Raw Material Batch Q4",
        buyer_budget=50000, buyer_target=38000,
        seller_ask=60000, seller_floor=40000, seller_cost=32000,
    ),
    "💼 Freelance Contract": ScenarioConfig(
        name="Freelance Contract",
        item="Full-Stack Dev Project (3 months)",
        buyer_budget=12000, buyer_target=8000,
        seller_ask=18000, seller_floor=10000, seller_cost=7000,
    ),
}

BUYER_STRATEGIES = ["Concession", "Aggressive Bargaining", "Deadline Pressure", "Anchoring Low"]
SELLER_STRATEGIES = ["Anchoring High", "Counter-Offer", "Dynamic Discount", "Scarcity Pressure"]


# ══════════════════════════════════════════════════════════════════════════════
# MARKET INTELLIGENCE AGENT
# ══════════════════════════════════════════════════════════════════════════════

class MarketAgent:
    """
    Simulates external market conditions that influence negotiation behavior.
    In a production system this would fetch live data via APIs.
    """

    def __init__(self, scenario: ScenarioConfig):
        self.scenario = scenario

    def gather_intelligence(self) -> MarketData:
        """Generate simulated market signals based on scenario parameters."""
        sc = self.scenario
        # Competitor price floats ±10% around seller floor
        competitor = round(sc.seller_floor * random.uniform(0.90, 1.10), 2)
        demand = random.choice(["Low", "Low", "Medium", "Medium", "Medium", "High"])
        trend  = random.choice(["Rising", "Stable", "Stable", "Falling"])
        inventory = random.choice(["Scarce", "Normal", "Normal", "Surplus"])
        urgency = round(random.uniform(0.2, 0.9), 2)
        return MarketData(
            competitor_price=competitor,
            demand_level=demand,
            price_trend=trend,
            inventory_signal=inventory,
            urgency_factor=urgency,
        )


# ══════════════════════════════════════════════════════════════════════════════
# STRATEGY ENGINE
# ══════════════════════════════════════════════════════════════════════════════

class StrategyEngine:
    """
    Implements game-theory inspired negotiation logic:
      - Utility function evaluation
      - Bayesian belief updates on opponent's reservation price
      - Pareto optimal deal computation
      - Concession curves (Zeuthen / time-pressure models)
    """

    def __init__(self, scenario: ScenarioConfig):
        self.sc = scenario
        # Bayesian priors on opponent's reservation price
        self._buyer_belief_seller_floor = scenario.seller_floor * random.uniform(0.95, 1.05)
        self._seller_belief_buyer_budget = scenario.buyer_budget * random.uniform(0.90, 1.00)

    # ── Utility ────────────────────────────────────────────────────────────
    def buyer_utility(self, price: float) -> float:
        return self.sc.buyer_budget - price

    def seller_utility(self, price: float) -> float:
        return price - self.sc.seller_cost

    # ── Pareto optimal midpoint ────────────────────────────────────────────
    def pareto_deal(self, buyer_offer: float, seller_offer: float) -> float:
        """
        Compute Pareto-optimal price as weighted midpoint that maximises
        the product of both utilities (Nash Bargaining Solution).
        """
        lo, hi = buyer_offer, seller_offer
        best_price, best_product = lo, -1.0
        for candidate in [lo + (hi - lo) * t / 100 for t in range(101)]:
            bu = self.buyer_utility(candidate)
            su = self.seller_utility(candidate)
            if bu > 0 and su > 0:
                product = bu * su
                if product > best_product:
                    best_product = product
                    best_price = candidate
        return round(best_price, 2)

    # ── Bayesian belief update ─────────────────────────────────────────────
    def update_beliefs(self, opponent_offer: float, role: str):
        """
        Update beliefs about opponent's reservation price based on observed offer.
        Uses a simple Bayesian update: blend old belief with new evidence.
        """
        alpha = 0.35  # learning rate
        if role == "buyer":
            # We observe buyer's offer; update our belief about their true budget
            self._seller_belief_buyer_budget = (
                (1 - alpha) * self._seller_belief_buyer_budget + alpha * opponent_offer * 1.15
            )
        else:
            # We observe seller's offer; update belief about their floor
            self._buyer_belief_seller_floor = (
                (1 - alpha) * self._buyer_belief_seller_floor + alpha * opponent_offer * 0.90
            )

    # ── Concession curve ────────────────────────────────────────────────────
    def concession_step(self, current: float, target: float, round_num: int,
                        max_rounds: int, urgency: float) -> float:
        """
        Time-dependent concession: more aggressive as rounds progress.
        Uses exponential decay towards target price.
        """
        progress = round_num / max_rounds
        # Zeuthen-style concession factor
        factor = (1 - progress) ** (1.5 - urgency)
        step = (current - target) * (1 - factor) * random.uniform(0.4, 0.7)
        return current - step

    # ── Convergence check ────────────────────────────────────────────────
    def is_converged(self, buyer_offer: float, seller_offer: float, threshold: float = 0.04) -> bool:
        """Return True when offers are within threshold% of each other."""
        mid = (buyer_offer + seller_offer) / 2.0
        if mid == 0:
            return False
        return abs(buyer_offer - seller_offer) / mid < threshold


# ══════════════════════════════════════════════════════════════════════════════
# BUYER AGENT
# ══════════════════════════════════════════════════════════════════════════════

class BuyerAgent:
    """
    Autonomous agent that negotiates on behalf of the buyer.
    Goal: minimize final price while staying within budget.
    """

    def __init__(self, scenario: ScenarioConfig, strategy: str,
                 urgency: float, engine: StrategyEngine, market: MarketData):
        self.sc = scenario
        self.strategy = strategy
        self.urgency = urgency          # 0–1
        self.engine = engine
        self.market = market
        # Start with a low anchor offer
        self._current_offer = self._initial_offer()
        self._offer_history: List[float] = []

    def _initial_offer(self) -> float:
        """First offer depends on strategy."""
        sc = self.sc
        if self.strategy == "Anchoring Low":
            return round(sc.buyer_target * random.uniform(0.78, 0.86), 2)
        elif self.strategy == "Aggressive Bargaining":
            return round(sc.buyer_target * random.uniform(0.82, 0.90), 2)
        elif self.strategy == "Deadline Pressure":
            return round(sc.buyer_target * random.uniform(0.85, 0.92), 2)
        else:  # Concession
            return round(sc.buyer_target * random.uniform(0.88, 0.94), 2)

    def make_offer(self, round_num: int, max_rounds: int,
                   last_seller_offer: Optional[float]) -> Tuple[float, List[str]]:
        """
        Compute next buyer offer and return it alongside reasoning thoughts.
        """
        sc = self.sc
        thinking = []

        # React to seller's last offer
        if last_seller_offer:
            self.engine.update_beliefs(last_seller_offer, role="seller")
            gap = last_seller_offer - self._current_offer
            thinking.append(f"→ Seller offered ${last_seller_offer:,.0f} — gap: ${gap:,.0f}")

        # Market influence
        if self.market.demand_level == "Low":
            demand_mod = 0.97   # low demand → press harder
            thinking.append("→ Demand signal: LOW — reducing offer by ~3%")
        elif self.market.demand_level == "High":
            demand_mod = 1.02
            thinking.append("→ Demand signal: HIGH — slight concession")
        else:
            demand_mod = 1.0
            thinking.append("→ Demand signal: MEDIUM — holding position")

        if self.market.competitor_price < sc.seller_ask * 0.95:
            thinking.append(f"→ Competitor price ${self.market.competitor_price:,.0f} below ask — using leverage")

        # Core concession logic
        target = sc.buyer_target
        progress = round_num / max_rounds
        urgency_boost = 1.0 + self.urgency * 0.06 * progress

        if self.strategy == "Concession":
            new_offer = self.engine.concession_step(
                self._current_offer, sc.buyer_budget * 0.9,
                round_num, max_rounds, self.urgency
            ) * demand_mod
            thinking.append(f"→ [Concession] stepping toward ${sc.buyer_budget * 0.9:,.0f}")

        elif self.strategy == "Aggressive Bargaining":
            # Stay low, move slowly
            new_offer = self._current_offer * random.uniform(1.015, 1.03) * demand_mod
            thinking.append("→ [Aggressive] minimal concession — holding pressure")

        elif self.strategy == "Deadline Pressure":
            # Stay low until last rounds, then jump
            if progress > 0.75:
                new_offer = self._current_offer * random.uniform(1.06, 1.12) * urgency_boost
                thinking.append("→ [Deadline] urgency rising — closing gap quickly")
            else:
                new_offer = self._current_offer * random.uniform(1.01, 1.025)
                thinking.append("→ [Deadline] early rounds — maintaining low anchor")

        else:  # Anchoring Low
            new_offer = self._current_offer * random.uniform(1.02, 1.04) * demand_mod
            thinking.append("→ [Anchor Low] gradual upward creep from anchor")

        # Clamp to budget
        new_offer = max(sc.buyer_target * 0.75, min(new_offer, sc.buyer_budget * 0.97))
        new_offer = round(new_offer, 2)
        self._current_offer = new_offer
        self._offer_history.append(new_offer)
        thinking.append(f"→ Utility if accepted: ${self.engine.buyer_utility(new_offer):,.0f}")
        return new_offer, thinking


# ══════════════════════════════════════════════════════════════════════════════
# SELLER AGENT
# ══════════════════════════════════════════════════════════════════════════════

class SellerAgent:
    """
    Autonomous agent that negotiates on behalf of the seller.
    Goal: maximize price above cost.
    """

    def __init__(self, scenario: ScenarioConfig, strategy: str,
                 engine: StrategyEngine, market: MarketData):
        self.sc = scenario
        self.strategy = strategy
        self.engine = engine
        self.market = market
        self._current_offer = self._initial_offer()
        self._offer_history: List[float] = []

    def _initial_offer(self) -> float:
        """Open with a high anchor."""
        sc = self.sc
        if self.strategy == "Anchoring High":
            return round(sc.seller_ask * random.uniform(1.00, 1.04), 2)
        elif self.strategy == "Scarcity Pressure":
            return round(sc.seller_ask * random.uniform(0.98, 1.02), 2)
        elif self.strategy == "Dynamic Discount":
            return round(sc.seller_ask * random.uniform(0.95, 0.99), 2)
        else:  # Counter-Offer
            return round(sc.seller_ask * random.uniform(0.96, 1.00), 2)

    def make_offer(self, round_num: int, max_rounds: int,
                   last_buyer_offer: Optional[float]) -> Tuple[float, List[str]]:
        """
        Compute next seller counter-offer and return reasoning.
        """
        sc = self.sc
        thinking = []

        if last_buyer_offer:
            self.engine.update_beliefs(last_buyer_offer, role="buyer")
            estimated_budget = self.engine._seller_belief_buyer_budget
            thinking.append(f"→ Buyer offered ${last_buyer_offer:,.0f} — estimated budget ~${estimated_budget:,.0f}")

        # Market influence
        if self.market.inventory_signal == "Scarce":
            inv_mod = 1.02
            thinking.append("→ Inventory: SCARCE — maintaining premium price")
        elif self.market.inventory_signal == "Surplus":
            inv_mod = 0.97
            thinking.append("→ Inventory: SURPLUS — willing to discount more")
        else:
            inv_mod = 1.0
            thinking.append("→ Inventory: NORMAL — standard pricing")

        progress = round_num / max_rounds

        if self.strategy == "Anchoring High":
            discount_rate = random.uniform(0.02, 0.04) * (1 + progress * 0.5)
            new_offer = self._current_offer * (1 - discount_rate) * inv_mod
            thinking.append(f"→ [Anchor High] discounting {discount_rate*100:.1f}% from high anchor")

        elif self.strategy == "Counter-Offer":
            # Mirror 40% of buyer's concession
            if last_buyer_offer:
                midpoint = (self._current_offer + last_buyer_offer) / 2
                new_offer = self._current_offer - (self._current_offer - midpoint) * 0.4
            else:
                new_offer = self._current_offer * random.uniform(0.96, 0.98)
            thinking.append("→ [Counter] splitting difference at 40% toward buyer")

        elif self.strategy == "Dynamic Discount":
            # Larger discounts as pressure grows
            discount = 0.03 + progress * 0.04
            new_offer = self._current_offer * (1 - discount) * inv_mod
            thinking.append(f"→ [Dynamic] round-based discount: {discount*100:.1f}%")

        else:  # Scarcity Pressure
            # Tiny concessions, emphasise scarcity
            new_offer = self._current_offer * random.uniform(0.975, 0.990) * inv_mod
            thinking.append("→ [Scarcity] minimal concession — emphasising limited supply")

        # Clamp to floor
        new_offer = max(sc.seller_floor, min(new_offer, sc.seller_ask * 1.05))
        new_offer = round(new_offer, 2)
        self._current_offer = new_offer
        self._offer_history.append(new_offer)
        thinking.append(f"→ Margin if accepted: ${self.engine.seller_utility(new_offer):,.0f}")
        return new_offer, thinking


# ══════════════════════════════════════════════════════════════════════════════
# NEGOTIATION ENVIRONMENT
# ══════════════════════════════════════════════════════════════════════════════

class NegotiationEnvironment:
    """
    Orchestrates all agents, runs the negotiation loop,
    and returns a structured result.
    """

    def __init__(
        self,
        scenario: ScenarioConfig,
        buyer_strategy: str,
        seller_strategy: str,
        urgency: float,
        max_rounds: int,
    ):
        self.scenario = scenario
        self.max_rounds = max_rounds

        # Instantiate agents
        self.market_agent = MarketAgent(scenario)
        self.market_data = self.market_agent.gather_intelligence()
        self.engine = StrategyEngine(scenario)
        self.buyer = BuyerAgent(scenario, buyer_strategy, urgency, self.engine, self.market_data)
        self.seller = SellerAgent(scenario, seller_strategy, self.engine, self.market_data)

    def run(self) -> NegotiationResult:
        """Execute the full negotiation loop."""
        sc = self.scenario
        rounds: List[RoundRecord] = []
        buyer_offers: List[float] = []
        seller_offers: List[float] = []
        converged = False

        last_buyer_offer: Optional[float] = None
        last_seller_offer: Optional[float] = None

        for r in range(1, self.max_rounds + 1):
            # Buyer turn
            b_offer, b_thinking = self.buyer.make_offer(r, self.max_rounds, last_seller_offer)
            buyer_offers.append(b_offer)
            last_buyer_offer = b_offer

            # Seller turn
            s_offer, s_thinking = self.seller.make_offer(r, self.max_rounds, last_buyer_offer)
            seller_offers.append(s_offer)
            last_seller_offer = s_offer

            # Record round
            gap = s_offer - b_offer
            rounds.append(RoundRecord(
                round_num=r,
                buyer_offer=b_offer,
                seller_offer=s_offer,
                buyer_thinking=b_thinking,
                seller_thinking=s_thinking,
                buyer_utility=self.engine.buyer_utility(b_offer),
                seller_utility=self.engine.seller_utility(s_offer),
                gap=gap,
            ))

            # Check convergence
            if self.engine.is_converged(b_offer, s_offer):
                converged = True
                break

        # Final deal — Pareto optimal midpoint
        deal_price = self.engine.pareto_deal(last_buyer_offer, last_seller_offer)
        savings = sc.seller_ask - deal_price
        savings_pct = (savings / sc.seller_ask) * 100 if sc.seller_ask > 0 else 0

        return NegotiationResult(
            deal_price=deal_price,
            total_rounds=len(rounds),
            original_ask=sc.seller_ask,
            savings=savings,
            savings_pct=savings_pct,
            buyer_utility=self.engine.buyer_utility(deal_price),
            seller_utility=self.engine.seller_utility(deal_price),
            buyer_offers=buyer_offers,
            seller_offers=seller_offers,
            rounds=rounds,
            strategy_used_buyer=self.buyer.strategy,
            strategy_used_seller=self.seller.strategy,
            converged=converged,
        )


# ══════════════════════════════════════════════════════════════════════════════
# MAIN NEGOTIATION RUNNER (called by UI)
# ══════════════════════════════════════════════════════════════════════════════

def run_negotiation(
    scenario_key: str,
    buyer_strategy: str,
    seller_strategy: str,
    urgency_pct: int,
    max_rounds: int,
) -> NegotiationResult:
    """Wrapper called by the Streamlit UI to start a negotiation."""
    scenario = SCENARIOS[scenario_key]
    urgency = urgency_pct / 100.0
    env = NegotiationEnvironment(scenario, buyer_strategy, seller_strategy, urgency, max_rounds)
    return env.run()


# ══════════════════════════════════════════════════════════════════════════════
# CHART HELPERS
# ══════════════════════════════════════════════════════════════════════════════

CHART_THEME = {
    "paper_bgcolor": "rgba(4,13,26,0)",
    "plot_bgcolor": "rgba(4,13,26,0)",
    "font": {"color": "#c0d4e8", "family": "IBM Plex Mono"},
    "gridcolor": "rgba(0,100,180,0.1)",
    "linecolor": "rgba(0,150,255,0.2)",
}


def build_offer_chart(result: NegotiationResult, scenario: ScenarioConfig) -> go.Figure:
    """Line chart comparing buyer vs seller offer progression."""
    rounds = list(range(1, len(result.buyer_offers) + 1))
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=rounds, y=result.buyer_offers, name="Buyer Offers",
        line=dict(color="#00aaff", width=2.5, dash="solid"),
        marker=dict(size=7, color="#00aaff", line=dict(width=1, color="#001030")),
        mode="lines+markers",
    ))
    fig.add_trace(go.Scatter(
        x=rounds, y=result.seller_offers, name="Seller Offers",
        line=dict(color="#ff8c00", width=2.5, dash="solid"),
        marker=dict(size=7, color="#ff8c00", line=dict(width=1, color="#200800")),
        mode="lines+markers",
    ))
    fig.add_hline(
        y=result.deal_price, line_dash="dot", line_color="#00ff96", line_width=1.5,
        annotation_text=f"Deal ${result.deal_price:,.0f}",
        annotation_font_color="#00ff96", annotation_font_size=11,
    )
    fig.add_hline(
        y=scenario.seller_ask, line_dash="dash", line_color="rgba(255,80,80,0.4)", line_width=1,
        annotation_text="Original Ask", annotation_font_color="#ff5050", annotation_font_size=10,
    )

    fig.update_layout(
        title=dict(text="📈 Offer Progression", font=dict(size=13, color="#4a7fa8")),
        xaxis=dict(title="Round", gridcolor=CHART_THEME["gridcolor"], linecolor=CHART_THEME["linecolor"], tickcolor="#4a7fa8"),
        yaxis=dict(title="Price ($)", gridcolor=CHART_THEME["gridcolor"], linecolor=CHART_THEME["linecolor"]),
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=CHART_THEME["font"],
        legend=dict(bgcolor="rgba(0,20,50,0.5)", bordercolor="rgba(0,150,255,0.2)", borderwidth=1),
        height=320,
        margin=dict(l=40, r=20, t=40, b=40),
    )
    return fig


def build_utility_chart(result: NegotiationResult) -> go.Figure:
    """Area chart showing buyer vs seller utility over rounds."""
    rounds = list(range(1, len(result.rounds) + 1))
    buyer_utils = [r.buyer_utility for r in result.rounds]
    seller_utils = [r.seller_utility for r in result.rounds]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=rounds, y=buyer_utils, name="Buyer Utility",
        fill="tozeroy", fillcolor="rgba(0,170,255,0.12)",
        line=dict(color="#00aaff", width=2),
    ))
    fig.add_trace(go.Scatter(
        x=rounds, y=seller_utils, name="Seller Utility",
        fill="tozeroy", fillcolor="rgba(255,140,0,0.12)",
        line=dict(color="#ff8c00", width=2),
    ))

    fig.update_layout(
        title=dict(text="⚡ Utility Functions", font=dict(size=13, color="#4a7fa8")),
        xaxis=dict(title="Round", gridcolor=CHART_THEME["gridcolor"]),
        yaxis=dict(title="Utility ($)", gridcolor=CHART_THEME["gridcolor"]),
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=CHART_THEME["font"],
        legend=dict(bgcolor="rgba(0,20,50,0.5)", bordercolor="rgba(0,150,255,0.2)", borderwidth=1),
        height=280,
        margin=dict(l=40, r=20, t=40, b=40),
    )
    return fig


def build_gap_chart(result: NegotiationResult) -> go.Figure:
    """Bar chart of the offer gap per round."""
    rounds = [f"R{r.round_num}" for r in result.rounds]
    gaps = [r.gap for r in result.rounds]
    colors = [f"rgba(0,{int(200*(1-i/len(gaps)))},{int(255*i/len(gaps))},0.7)" for i in range(len(gaps))]

    fig = go.Figure(go.Bar(
        x=rounds, y=gaps, marker_color=colors,
        text=[f"${g:,.0f}" for g in gaps], textposition="outside",
        textfont=dict(size=10, color="#c0d4e8"),
    ))
    fig.update_layout(
        title=dict(text="🔻 Offer Gap Per Round", font=dict(size=13, color="#4a7fa8")),
        xaxis=dict(gridcolor=CHART_THEME["gridcolor"]),
        yaxis=dict(title="Gap ($)", gridcolor=CHART_THEME["gridcolor"]),
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        font=CHART_THEME["font"],
        height=260,
        margin=dict(l=40, r=20, t=40, b=40),
    )
    return fig


def savings_gauge(savings_pct: float) -> go.Figure:
    """Gauge chart showing savings percentage."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=savings_pct,
        number={"suffix": "%", "font": {"size": 28, "color": "#00ff96", "family": "IBM Plex Mono"}},
        delta={"reference": 0, "increasing": {"color": "#00ff96"}},
        gauge={
            "axis": {"range": [0, 50], "tickcolor": "#4a7fa8", "tickfont": {"size": 10}},
            "bar": {"color": "#00ff96", "thickness": 0.3},
            "bgcolor": "rgba(0,20,50,0.6)",
            "bordercolor": "rgba(0,200,255,0.2)",
            "steps": [
                {"range": [0, 15], "color": "rgba(255,80,80,0.1)"},
                {"range": [15, 30], "color": "rgba(255,200,0,0.1)"},
                {"range": [30, 50], "color": "rgba(0,255,150,0.1)"},
            ],
            "threshold": {"line": {"color": "#ffd700", "width": 2}, "thickness": 0.8, "value": savings_pct},
        },
        title={"text": "SAVINGS ACHIEVED", "font": {"size": 11, "color": "#4a7fa8", "family": "IBM Plex Mono"}},
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        height=200,
        margin=dict(l=20, r=20, t=30, b=10),
        font=dict(color="#c0d4e8"),
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# STREAMLIT UI
# ══════════════════════════════════════════════════════════════════════════════

def render_header(status: str = "ready"):
    badge_class = {"ready": "badge-ready", "live": "badge-live", "done": "badge-done"}.get(status, "badge-ready")
    badge_text  = {"ready": "● READY", "live": "● LIVE", "done": "● COMPLETE"}.get(status, "● READY")
    st.markdown(f"""
    <div class="war-room-header">
        <div style="font-size:2.4rem">⚔️</div>
        <div style="flex:1">
            <div style="font-family:'IBM Plex Mono',monospace;font-size:1.35rem;font-weight:700;
                        color:#00d4ff;letter-spacing:0.12em;text-transform:uppercase;">
                NegotiAI War Room
            </div>
            <div style="font-size:0.65rem;letter-spacing:0.25em;color:#4a7fa8;text-transform:uppercase;">
                Autonomous Multi-Agent Negotiation System
            </div>
        </div>
        <span class="status-badge {badge_class}">{badge_text}</span>
    </div>
    """, unsafe_allow_html=True)


def render_market_panel(market: MarketData, scenario: ScenarioConfig):
    trend_color  = "#ff8c00" if "Rising"  in market.price_trend    else ("#00aaff" if "Falling" in market.price_trend    else "#ffd700")
    demand_color = "#ff5050" if market.demand_level    == "High"   else ("#00aaff" if market.demand_level    == "Low"    else "#ffd700")
    inv_color    = "#ff5050" if market.inventory_signal == "Scarce" else ("#00aaff" if market.inventory_signal == "Surplus" else "#aaa")

    st.markdown("**📡 Market Intelligence Agent**")
    r1, r2 = st.columns(2)
    r1.metric("Competitor Price", f"${market.competitor_price:,.0f}")
    r2.metric("Urgency Factor",   f"{market.urgency_factor*100:.0f}%")
    r3, r4, r5 = st.columns(3)
    r3.markdown(f"<div style='font-size:0.75rem;color:#4a7fa8'>Demand<br>"
                f"<b style='color:{demand_color}'>{market.demand_level}</b></div>", unsafe_allow_html=True)
    r4.markdown(f"<div style='font-size:0.75rem;color:#4a7fa8'>Price Trend<br>"
                f"<b style='color:{trend_color}'>{market.price_trend}</b></div>", unsafe_allow_html=True)
    r5.markdown(f"<div style='font-size:0.75rem;color:#4a7fa8'>Inventory<br>"
                f"<b style='color:{inv_color}'>{market.inventory_signal}</b></div>", unsafe_allow_html=True)
    st.caption(f"Seller Floor Estimate: ${scenario.seller_floor:,.0f}")


def render_thinking_panels(round_rec: RoundRecord):
    def clean(lines):
        return "\n".join(l.replace("$", "USD ") for l in lines)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"<div class='agent-panel buyer-panel'>"
            f"<div class='section-title'>🤖 Buyer Agent — Round {round_rec.round_num}</div>"
            f"<div style='color:#00aaff;font-size:1.05rem;font-weight:700;margin-bottom:6px'>"
            f"Offer: ${round_rec.buyer_offer:,.0f}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
        for line in round_rec.buyer_thinking:
            st.caption(line.replace("$", "USD "))
    with c2:
        st.markdown(
            f"<div class='agent-panel seller-panel'>"
            f"<div class='section-title'>🤖 Seller Agent — Round {round_rec.round_num}</div>"
            f"<div style='color:#ff8c00;font-size:1.05rem;font-weight:700;margin-bottom:6px'>"
            f"Counter: ${round_rec.seller_offer:,.0f}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
        for line in round_rec.seller_thinking:
            st.caption(line.replace("$", "USD "))


def render_deal_card(result: NegotiationResult, scenario: ScenarioConfig):
    """Render deal summary using only native Streamlit components."""
    convergence_label = "✅ Converged Early" if result.converged else "⏱ Max Rounds Reached"

    # Header banner
    st.success(f"{convergence_label} — PARETO-OPTIMAL DEAL REACHED")

    # Big price display
    st.markdown(
        f"<h1 style='text-align:center;color:#00d4ff;font-family:IBM Plex Mono,monospace;"
        f"font-size:2.6rem;margin:8px 0 2px'>"
        f"${result.deal_price:,.0f}</h1>"
        f"<p style='text-align:center;color:#4a7fa8;font-size:0.75rem;"
        f"letter-spacing:0.2em;margin-bottom:16px'>FINAL NEGOTIATED PRICE</p>",
        unsafe_allow_html=True,
    )

    # Stats row using st.columns + st.metric (fully native — no $ issues)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("💰 SAVINGS",       f"${result.savings:,.0f}")
    c2.metric("📉 DISCOUNT",      f"{result.savings_pct:.1f}%")
    c3.metric("🔄 ROUNDS",        str(result.total_rounds))
    c4.metric("🔵 BUYER UTILITY", f"${result.buyer_utility:,.0f}")
    c5.metric("🟠 SELLER PROFIT", f"${result.seller_utility:,.0f}")

    # Strategy footer
    st.markdown(
        f"<p style='text-align:center;font-size:0.75rem;color:#4a7fa8;"
        f"font-family:IBM Plex Mono,monospace;margin-top:8px'>"
        f"Buyer: <b style='color:#00aaff'>{result.strategy_used_buyer}</b>"
        f"&nbsp;&nbsp;|&nbsp;&nbsp;"
        f"Seller: <b style='color:#ff8c00'>{result.strategy_used_seller}</b></p>",
        unsafe_allow_html=True,
    )


def render_timeline(result: NegotiationResult):
    st.markdown("**📋 Negotiation Timeline**")
    for r in result.rounds:
        b_thoughts = " | ".join(
            l.replace("$", "USD ").replace("→ ", "") for l in r.buyer_thinking[:2]
        )
        s_thoughts = " | ".join(
            l.replace("$", "USD ").replace("→ ", "") for l in r.seller_thinking[:2]
        )
        with st.container():
            bc, sc_ = st.columns([1, 1])
            with bc:
                st.markdown(
                    f"<div class='round-item-buyer'>"
                    f"<span class='tag-buyer'>↑ BUYER R{r.round_num}</span>"
                    f"&nbsp; Offer: <b style='color:#00d4ff'>${r.buyer_offer:,.0f}</b><br>"
                    f"<span style='color:#607080;font-size:0.7rem'>{b_thoughts}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
            with sc_:
                st.markdown(
                    f"<div class='round-item-seller'>"
                    f"<span class='tag-seller'>↓ SELLER R{r.round_num}</span>"
                    f"&nbsp; Counter: <b style='color:#ffaa44'>${r.seller_offer:,.0f}</b><br>"
                    f"<span style='color:#607080;font-size:0.7rem'>{s_thoughts}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )


# ══════════════════════════════════════════════════════════════════════════════
# MAIN — STREAMLIT ENTRY POINT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    # ── Sidebar Config ────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.65rem;
                    letter-spacing:0.2em;color:#4a7fa8;padding:8px 0 12px;
                    border-bottom:1px solid rgba(0,200,255,0.1);margin-bottom:16px">
            ⚙ SCENARIO CONFIGURATION
        </div>
        """, unsafe_allow_html=True)

        scenario_key = st.selectbox("Scenario", list(SCENARIOS.keys()))
        sc = SCENARIOS[scenario_key]

        st.markdown(f"""
        <div style="background:rgba(0,30,60,0.5);border:1px solid rgba(0,200,255,0.12);
                    border-radius:8px;padding:10px;margin-bottom:12px;
                    font-family:'IBM Plex Mono',monospace;font-size:0.72rem;color:#7ab4d0">
            📦 {sc.item}<br>
            <span style="color:#00aaff">Ask: &#36;{sc.seller_ask:,.0f}</span> &nbsp;·&nbsp;
            <span style="color:#00d4ff">Target: &#36;{sc.buyer_target:,.0f}</span><br>
            <span style="color:#4a7fa8">Budget: &#36;{sc.buyer_budget:,.0f}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="font-size:0.65rem;letter-spacing:0.2em;color:#4a7fa8;margin-bottom:6px">🤖 AGENT STRATEGIES</div>', unsafe_allow_html=True)
        buyer_strategy  = st.selectbox("Buyer Strategy",  BUYER_STRATEGIES)
        seller_strategy = st.selectbox("Seller Strategy", SELLER_STRATEGIES)

        st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)
        urgency = st.slider("Buyer Urgency", 0, 100, 50, help="Higher urgency → buyer concedes faster")
        max_rounds = st.slider("Max Rounds", 3, 15, 8)

        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
        start = st.button("▶ LAUNCH NEGOTIATION", use_container_width=True)

        st.markdown("""
        <div style="margin-top:24px;font-family:'IBM Plex Mono',monospace;font-size:0.6rem;
                    color:#2a4a6a;letter-spacing:0.1em;line-height:1.8">
            Multi-Agent System<br>
            ├ Buyer Agent<br>
            ├ Seller Agent<br>
            ├ Strategy Engine<br>
            └ Market Intelligence
        </div>
        """, unsafe_allow_html=True)

    # ── Main Content ──────────────────────────────────────────────────────
    if "result" not in st.session_state:
        st.session_state.result = None
        st.session_state.market = None
        st.session_state.scenario_used = None

    status = "done" if st.session_state.result else "ready"
    render_header(status)

    if start:
        render_header("live")
        with st.spinner("🔄 Agents negotiating…"):
            env = NegotiationEnvironment(sc, buyer_strategy, seller_strategy, urgency / 100, max_rounds)
            result = env.run()
            st.session_state.result = result
            st.session_state.market = env.market_data
            st.session_state.scenario_used = sc
        st.rerun()

    result: Optional[NegotiationResult] = st.session_state.result
    market: Optional[MarketData] = st.session_state.market
    scenario_used: Optional[ScenarioConfig] = st.session_state.scenario_used

    if result is None:
        # ── Welcome state ─────────────────────────────────────────────────
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;font-family:'IBM Plex Mono',monospace">
            <div style="font-size:3rem;margin-bottom:16px">⚔️</div>
            <div style="font-size:1.1rem;color:#00d4ff;letter-spacing:0.15em;font-weight:700;margin-bottom:8px">
                AUTONOMOUS NEGOTIATION WAR ROOM
            </div>
            <div style="color:#4a7fa8;font-size:0.8rem;letter-spacing:0.1em;max-width:500px;margin:0 auto;line-height:1.8">
                Configure your scenario and agent strategies in the sidebar,<br>
                then launch a negotiation to watch AI agents battle it out.
            </div>
            <div style="margin-top:32px;display:flex;gap:24px;justify-content:center;flex-wrap:wrap">
                <div style="color:#4a7fa8;font-size:0.7rem;letter-spacing:0.12em">🤖 Buyer Agent</div>
                <div style="color:#4a7fa8;font-size:0.7rem">⚡</div>
                <div style="color:#4a7fa8;font-size:0.7rem;letter-spacing:0.12em">🤖 Seller Agent</div>
                <div style="color:#4a7fa8;font-size:0.7rem">⚡</div>
                <div style="color:#4a7fa8;font-size:0.7rem;letter-spacing:0.12em">📡 Market Intelligence</div>
                <div style="color:#4a7fa8;font-size:0.7rem">⚡</div>
                <div style="color:#4a7fa8;font-size:0.7rem;letter-spacing:0.12em">⚙️ Strategy Engine</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── Results Layout ────────────────────────────────────────────────────
    # Row 1: KPI metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Final Price",    f"${result.deal_price:,.0f}", f"-${result.savings:,.0f}")
    col2.metric("Savings",        f"{result.savings_pct:.1f}%", "vs original ask")
    col3.metric("Rounds",         result.total_rounds, "negotiation cycles")
    col4.metric("Buyer Utility",  f"${result.buyer_utility:,.0f}")
    col5.metric("Seller Profit",  f"${result.seller_utility:,.0f}")

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Row 2: Charts + Market
    col_charts, col_market = st.columns([2.8, 1])

    with col_charts:
        tab1, tab2, tab3 = st.tabs(["📈 Offer Progression", "⚡ Utility Functions", "🔻 Gap Analysis"])
        with tab1:
            st.plotly_chart(build_offer_chart(result, scenario_used), use_container_width=True)
        with tab2:
            st.plotly_chart(build_utility_chart(result), use_container_width=True)
        with tab3:
            st.plotly_chart(build_gap_chart(result), use_container_width=True)

    with col_market:
        render_market_panel(market, scenario_used)
        st.plotly_chart(savings_gauge(result.savings_pct), use_container_width=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Row 3: Deal card
    render_deal_card(result, scenario_used)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Row 4: Agent Thinking (latest round) + Timeline
    col_think, col_timeline = st.columns([1.2, 1])

    with col_think:
        st.markdown('<div class="section-title">🧠 Agent Reasoning (Final Round)</div>', unsafe_allow_html=True)
        render_thinking_panels(result.rounds[-1])

        # Show all rounds in expander
        with st.expander("🔍 View All Agent Reasoning Rounds"):
            for r in result.rounds:
                render_thinking_panels(r)

    with col_timeline:
        render_timeline(result)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Row 5: Raw data table
    with st.expander("📊 Raw Negotiation Data Table"):
        df = pd.DataFrame([{
            "Round": r.round_num,
            "Buyer Offer ($)": f"${r.buyer_offer:,.0f}",
            "Seller Offer ($)": f"${r.seller_offer:,.0f}",
            "Gap ($)": f"${r.gap:,.0f}",
            "Buyer Utility": f"${r.buyer_utility:,.0f}",
            "Seller Utility": f"${r.seller_utility:,.0f}",
        } for r in result.rounds])
        st.dataframe(df, use_container_width=True, hide_index=True)


# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()