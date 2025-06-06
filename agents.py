import os
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from models import AgentState, CustomerProfile, ProductRecommendation
from database import CSVDataManager, DatabaseManager

class CustomerContextAgent:
    def __init__(self):
        self.use_database = os.getenv('USE_DATABASE', 'false').lower() == 'true'
        if self.use_database:
            self.data_manager = DatabaseManager()
        else:
            self.data_manager = CSVDataManager()

    def execute(self, state: AgentState) -> AgentState:
        """Extract customer profile from data source"""
        try:
            customer_data = self.data_manager.get_customer_by_id(state.customer_id)
            
            if not customer_data:
                state.error = f"Customer {state.customer_id} not found"
                return state
            
            if isinstance(self.data_manager, CSVDataManager):
                state.customer_profile = self.data_manager.parse_customer_profile(customer_data)
            else:
                # Parse database data to CustomerProfile
                current_products = [prod.strip() for prod in str(customer_data.get('current_products', '')).split(',')]
                cross_sell_synergy = [prod.strip() for prod in str(customer_data.get('cross_sell_synergy', '')).split(',')]
                competitors = [comp.strip() for comp in str(customer_data.get('competitors', '')).split(',')]
                
                state.customer_profile = CustomerProfile(
                    customer_id=customer_data.get('customer_id', ''),
                    customer_name=customer_data.get('customer_name', ''),
                    industry=customer_data.get('industry', ''),
                    annual_revenue=int(customer_data.get('annual_revenue', 0)),
                    number_of_employees=int(customer_data.get('number_of_employees', 0)),
                    customer_priority_rating=customer_data.get('customer_priority_rating', ''),
                    account_type=customer_data.get('account_type', ''),
                    location=customer_data.get('location', ''),
                    current_products=current_products,
                    product_usage=float(customer_data.get('product_usage', 0)),
                    cross_sell_synergy=cross_sell_synergy,
                    last_activity_date=customer_data.get('last_activity_date', ''),
                    opportunity_stage=customer_data.get('opportunity_stage', ''),
                    opportunity_amount=int(customer_data.get('opportunity_amount', 0)),
                    opportunity_type=customer_data.get('opportunity_type', ''),
                    competitors=competitors,
                    activity_status=customer_data.get('activity_status', ''),
                    activity_priority=customer_data.get('activity_priority', ''),
                    activity_type=customer_data.get('activity_type', ''),
                    product_sku=customer_data.get('product_sku', '')
                )
            
            return state
            
        except Exception as e:
            state.error = f"Error fetching customer data: {str(e)}"
            return state

class PurchasePatternAnalysisAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

    def execute(self, state: AgentState) -> AgentState:
        """Analyze purchase patterns and identify missing opportunities"""
        if not state.customer_profile:
            state.error = "No customer profile available"
            return state

        try:
            prompt = f"""
            Analyze the purchase patterns for this customer:
            
            Customer: {state.customer_profile.customer_name}
            Industry: {state.customer_profile.industry}
            Current Products: {', '.join(state.customer_profile.current_products)}
            Product Usage: {state.customer_profile.product_usage}%
            Cross-sell Synergy Products: {', '.join(state.customer_profile.cross_sell_synergy)}
            Annual Revenue: ${state.customer_profile.annual_revenue:,}
            
            Identify:
            1. Frequent product categories they use
            2. Missing product opportunities based on their industry and current usage
            3. Underutilized products (usage < 70%)
            
            Return a structured analysis of their purchase patterns and gaps.
            """

            messages = [
                SystemMessage(content="You are an expert in customer purchase pattern analysis."),
                HumanMessage(content=prompt)
            ]

            response = self.llm.invoke(messages)
            
            # Parse the response into structured data
            state.purchase_patterns = {
                "current_products": state.customer_profile.current_products,
                "usage_percentage": state.customer_profile.product_usage,
                "synergy_products": state.customer_profile.cross_sell_synergy,
                "analysis": response.content,
                "underutilized": state.customer_profile.product_usage < 70
            }

            return state

        except Exception as e:
            state.error = f"Error in purchase pattern analysis: {str(e)}"
            return state

class ProductAffinityAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.3)

    def execute(self, state: AgentState) -> AgentState:
        """Suggest related/co-purchased products"""
        if not state.customer_profile or not state.purchase_patterns:
            state.error = "Missing customer profile or purchase patterns"
            return state

        try:
            prompt = f"""
            Based on the customer profile and purchase patterns, suggest related products:
            
            Customer: {state.customer_profile.customer_name}
            Industry: {state.customer_profile.industry}
            Current Products: {', '.join(state.customer_profile.current_products)}
            Identified Synergy Products: {', '.join(state.customer_profile.cross_sell_synergy)}
            
            Purchase Pattern Analysis: {state.purchase_patterns.get('analysis', '')}
            
            Suggest 5-7 complementary products that are commonly purchased together with their current products
            or are essential for their industry. Focus on products that would enhance their current setup.
            
            Format as a simple list of product names.
            """

            messages = [
                SystemMessage(content="You are an expert in product affinity and cross-selling recommendations."),
                HumanMessage(content=prompt)
            ]

            response = self.llm.invoke(messages)
            
            # Extract product suggestions from response
            product_suggestions = []
            lines = response.content.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('Based on') and not line.startswith('Here are'):
                    # Clean up the line (remove bullets, numbers, etc.)
                    clean_line = line.lstrip('•-*1234567890. ').strip()
                    if clean_line:
                        product_suggestions.append(clean_line)
            
            state.product_affinities = product_suggestions[:7]  # Limit to 7 suggestions

            return state

        except Exception as e:
            state.error = f"Error in product affinity analysis: {str(e)}"
            return state

class OpportunityScoringAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)

    def execute(self, state: AgentState) -> AgentState:
        """Score cross-sell and upsell opportunities"""
        if not all([state.customer_profile, state.purchase_patterns, state.product_affinities]):
            state.error = "Missing required data for opportunity scoring"
            return state

        try:
            prompt = f"""
            Score and prioritize cross-sell/upsell opportunities for this customer:
            
            Customer: {state.customer_profile.customer_name}
            Industry: {state.customer_profile.industry}
            Annual Revenue: ${state.customer_profile.annual_revenue:,}
            Current Products: {', '.join(state.customer_profile.current_products)}
            Current Usage: {state.customer_profile.product_usage}%
            Account Priority: {state.customer_profile.customer_priority_rating}
            Opportunity Stage: {state.customer_profile.opportunity_stage}
            
            Suggested Products: {', '.join(state.product_affinities)}
            
            For each suggested product, provide:
            1. Product name
            2. Type (cross-sell or upsell)
            3. Confidence score (0-100)
            4. Brief rationale
            5. Estimated value ($)
            
            Format as JSON-like structure:
            Product: [name]
            Type: [cross-sell/upsell]
            Score: [0-100]
            Rationale: [explanation]
            Value: [dollar amount]
            ---
            """

            messages = [
                SystemMessage(content="You are an expert in sales opportunity scoring and revenue optimization."),
                HumanMessage(content=prompt)
            ]

            response = self.llm.invoke(messages)
            
            # Parse response into ProductRecommendation objects
            recommendations = []
            entries = response.content.split('---')
            
            for entry in entries:
                if not entry.strip():
                    continue
                    
                lines = [line.strip() for line in entry.strip().split('\n') if line.strip()]
                
                product_name = ""
                rec_type = ""
                score = 0
                rationale = ""
                value = 0
                
                for line in lines:
                    if line.startswith('Product:'):
                        product_name = line.replace('Product:', '').strip()
                    elif line.startswith('Type:'):
                        rec_type = line.replace('Type:', '').strip()
                    elif line.startswith('Score:'):
                        try:
                            score = float(line.replace('Score:', '').strip())
                        except:
                            score = 50
                    elif line.startswith('Rationale:'):
                        rationale = line.replace('Rationale:', '').strip()
                    elif line.startswith('Value:'):
                        value_str = line.replace('Value:', '').strip().replace('$', '').replace(',', '')
                        try:
                            value = int(float(value_str))
                        except:
                            value = 10000
                
                if product_name and rec_type:
                    recommendations.append(ProductRecommendation(
                        product_name=product_name,
                        recommendation_type=rec_type,
                        confidence_score=score / 100.0,
                        rationale=rationale,
                        estimated_value=value
                    ))
            
            # Sort by confidence score
            recommendations.sort(key=lambda x: x.confidence_score, reverse=True)
            
            # Initialize scored_opportunities even if empty
            state.scored_opportunities = recommendations
            
            return state

        except Exception as e:
            state.error = f"Error in opportunity scoring: {str(e)}"
            return state

class RecommendationReportAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.4)

    def execute(self, state: AgentState) -> AgentState:
        """Generate comprehensive research report"""
        # FIXED: Only check if customer_profile exists, allow empty scored_opportunities
        if not state.customer_profile:
            state.error = "Missing customer profile for report generation"
            return state

        try:
            # Prepare recommendations summary - handle empty list properly
            top_recommendations = (state.scored_opportunities or [])[:5]
            
            if top_recommendations:
                rec_summary = "\n".join([
                    f"- {rec.product_name} ({rec.recommendation_type}): {rec.confidence_score:.0%} confidence, ${rec.estimated_value:,} estimated value"
                    for rec in top_recommendations
                ])
            else:
                rec_summary = "- No high-confidence recommendations identified at this time"

            prompt = f"""
            Generate a comprehensive research report for cross-sell and upsell opportunities:
            
            Customer Profile:
            - Name: {state.customer_profile.customer_name}
            - Industry: {state.customer_profile.industry}
            - Annual Revenue: ${state.customer_profile.annual_revenue:,}
            - Employees: {state.customer_profile.number_of_employees:,}
            - Location: {state.customer_profile.location}
            - Current Products: {', '.join(state.customer_profile.current_products)}
            - Product Usage: {state.customer_profile.product_usage}%
            - Priority Rating: {state.customer_profile.customer_priority_rating}
            - Account Type: {state.customer_profile.account_type}
            - Opportunity Stage: {state.customer_profile.opportunity_stage}
            
            Top Recommendations:
            {rec_summary}
            
            Create a professional research report with these sections:
            1. Executive Summary
            2. Customer Overview
            3. Current State Analysis
            4. Market Context & Industry Insights
            5. Opportunity Analysis
            6. Recommendations (prioritized)
            7. Implementation Strategy
            8. Conclusion
            
            Make it comprehensive but concise, actionable, and business-focused.
            """

            messages = [
                SystemMessage(content="You are a senior business analyst creating executive-level research reports."),
                HumanMessage(content=prompt)
            ]

            response = self.llm.invoke(messages)
            
            state.research_report = response.content
            state.recommendations = top_recommendations
            
            return state

        except Exception as e:
            state.error = f"Error generating research report: {str(e)}"
            return state