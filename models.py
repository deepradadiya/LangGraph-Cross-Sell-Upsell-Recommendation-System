from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

class CustomerProfile(BaseModel):
    customer_id: str
    customer_name: str
    industry: str
    annual_revenue: int
    number_of_employees: int
    customer_priority_rating: str
    account_type: str
    location: str
    current_products: List[str]
    product_usage: float
    cross_sell_synergy: List[str]
    last_activity_date: str
    opportunity_stage: str
    opportunity_amount: int
    opportunity_type: str
    competitors: List[str]
    activity_status: str
    activity_priority: str
    activity_type: str
    product_sku: str

class ProductRecommendation(BaseModel):
    product_name: str
    recommendation_type: str  # cross-sell or upsell
    confidence_score: float
    rationale: str
    estimated_value: int

class AgentState(BaseModel):
    customer_id: str
    customer_profile: Optional[CustomerProfile] = None
    purchase_patterns: Optional[Dict[str, Any]] = None
    product_affinities: Optional[List[str]] = None
    scored_opportunities: Optional[List[ProductRecommendation]] = None
    research_report: Optional[str] = None
    recommendations: Optional[List[ProductRecommendation]] = None
    error: Optional[str] = None

class RecommendationResponse(BaseModel):
    customer_id: str
    research_report: str
    recommendations: List[ProductRecommendation]
    success: bool
    error: Optional[str] = None