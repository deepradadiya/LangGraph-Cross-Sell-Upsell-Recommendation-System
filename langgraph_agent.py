from typing import Dict, Any
from langgraph.graph import StateGraph, END
from models import AgentState, RecommendationResponse, CustomerProfile, ProductRecommendation
from agents import (
    CustomerContextAgent,
    PurchasePatternAnalysisAgent,
    ProductAffinityAgent,
    OpportunityScoringAgent,
    RecommendationReportAgent
)

class CrossSellUpsellAgent:
    def __init__(self):
        self.customer_context_agent = CustomerContextAgent()
        self.purchase_pattern_agent = PurchasePatternAnalysisAgent()
        self.product_affinity_agent = ProductAffinityAgent()
        self.opportunity_scoring_agent = OpportunityScoringAgent()
        self.report_agent = RecommendationReportAgent()
        
        self.workflow = self._build_workflow()

    def _build_workflow(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(dict)  # Use dict instead of AgentState
        
        # Add nodes - renamed to avoid conflict with state keys
        workflow.add_node("customer_context", self._customer_context_node)
        workflow.add_node("analyze_purchase_patterns", self._purchase_patterns_node)
        workflow.add_node("product_affinity", self._product_affinity_node)
        workflow.add_node("opportunity_scoring", self._opportunity_scoring_node)
        workflow.add_node("generate_report", self._generate_report_node)
        
        # Define the workflow
        workflow.set_entry_point("customer_context")
        workflow.add_edge("customer_context", "analyze_purchase_patterns")
        workflow.add_edge("analyze_purchase_patterns", "product_affinity")
        workflow.add_edge("product_affinity", "opportunity_scoring")
        workflow.add_edge("opportunity_scoring", "generate_report")
        workflow.add_edge("generate_report", END)
        
        return workflow.compile()

    def _customer_context_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Node for customer context extraction"""
        agent_state = self._dict_to_agent_state(state)
        
        # Skip if there's already an error
        if agent_state.error:
            return state
            
        # Execute the agent
        result_state = self.customer_context_agent.execute(agent_state)
        
        # Convert back to dict for LangGraph
        return self._agent_state_to_dict(result_state)

    def _purchase_patterns_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Node for purchase pattern analysis"""
        agent_state = self._dict_to_agent_state(state)
        
        # Skip if there's already an error
        if agent_state.error:
            return state
            
        # Execute the agent
        result_state = self.purchase_pattern_agent.execute(agent_state)
        
        # Convert back to dict for LangGraph
        return self._agent_state_to_dict(result_state)

    def _product_affinity_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Node for product affinity analysis"""
        agent_state = self._dict_to_agent_state(state)
        
        # Skip if there's already an error
        if agent_state.error:
            return state
            
        # Execute the agent
        result_state = self.product_affinity_agent.execute(agent_state)
        
        # Convert back to dict for LangGraph
        return self._agent_state_to_dict(result_state)

    def _opportunity_scoring_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Node for opportunity scoring"""
        agent_state = self._dict_to_agent_state(state)
        
        # Skip if there's already an error
        if agent_state.error:
            return state
            
        # Execute the agent
        result_state = self.opportunity_scoring_agent.execute(agent_state)
        
        # Convert back to dict for LangGraph
        return self._agent_state_to_dict(result_state)

    def _generate_report_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Node for report generation"""
        agent_state = self._dict_to_agent_state(state)
        
        # Skip if there's already an error
        if agent_state.error:
            return state
            
        # Execute the agent
        result_state = self.report_agent.execute(agent_state)
        
        # Convert back to dict for LangGraph
        return self._agent_state_to_dict(result_state)

    def _dict_to_agent_state(self, state_dict: Dict[str, Any]) -> AgentState:
        """Convert dictionary to AgentState object"""
        try:
            # Ensure we're working with a dictionary
            if not isinstance(state_dict, dict):
                raise ValueError(f"Expected dict, got {type(state_dict)}")
            
            # Handle nested objects properly
            customer_profile = None
            if state_dict.get('customer_profile'):
                cp_data = state_dict['customer_profile']
                if isinstance(cp_data, dict):
                    customer_profile = CustomerProfile(**cp_data)
                elif isinstance(cp_data, CustomerProfile):
                    customer_profile = cp_data
                else:
                    customer_profile = cp_data
            
            # Handle scored opportunities
            scored_opportunities = None
            if state_dict.get('scored_opportunities'):
                so_data = state_dict['scored_opportunities']
                if isinstance(so_data, list):
                    scored_opportunities = []
                    for item in so_data:
                        if isinstance(item, dict):
                            scored_opportunities.append(ProductRecommendation(**item))
                        elif isinstance(item, ProductRecommendation):
                            scored_opportunities.append(item)
                        else:
                            scored_opportunities.append(item)
                else:
                    scored_opportunities = so_data
            
            # Handle recommendations
            recommendations = None
            if state_dict.get('recommendations'):
                rec_data = state_dict['recommendations']
                if isinstance(rec_data, list):
                    recommendations = []
                    for item in rec_data:
                        if isinstance(item, dict):
                            recommendations.append(ProductRecommendation(**item))
                        elif isinstance(item, ProductRecommendation):
                            recommendations.append(item)
                        else:
                            recommendations.append(item)
                else:
                    recommendations = rec_data
            
            return AgentState(
                customer_id=state_dict.get('customer_id', ''),
                customer_profile=customer_profile,
                purchase_patterns=state_dict.get('purchase_patterns'),
                product_affinities=state_dict.get('product_affinities'),
                scored_opportunities=scored_opportunities,
                research_report=state_dict.get('research_report'),
                recommendations=recommendations,
                error=state_dict.get('error')
            )
        except Exception as e:
            # If conversion fails, create a minimal state with error
            return AgentState(
                customer_id=state_dict.get('customer_id', '') if isinstance(state_dict, dict) else '',
                error=f"State conversion error: {str(e)}"
            )

    def _agent_state_to_dict(self, agent_state: AgentState) -> Dict[str, Any]:
        """Convert AgentState object to dictionary"""
        try:
            result = {
                "customer_id": agent_state.customer_id,
                "customer_profile": None,
                "purchase_patterns": agent_state.purchase_patterns,
                "product_affinities": agent_state.product_affinities,
                "scored_opportunities": None,
                "research_report": agent_state.research_report,
                "recommendations": None,
                "error": agent_state.error
            }
            
            # Handle customer_profile
            if agent_state.customer_profile:
                if hasattr(agent_state.customer_profile, 'model_dump'):
                    result["customer_profile"] = agent_state.customer_profile.model_dump()
                elif hasattr(agent_state.customer_profile, '__dict__'):
                    result["customer_profile"] = agent_state.customer_profile.__dict__
                else:
                    result["customer_profile"] = agent_state.customer_profile
            
            # Handle scored_opportunities
            if agent_state.scored_opportunities:
                result["scored_opportunities"] = []
                for rec in agent_state.scored_opportunities:
                    if hasattr(rec, 'model_dump'):
                        result["scored_opportunities"].append(rec.model_dump())
                    elif hasattr(rec, '__dict__'):
                        result["scored_opportunities"].append(rec.__dict__)
                    else:
                        result["scored_opportunities"].append(rec)
            
            # Handle recommendations
            if agent_state.recommendations:
                result["recommendations"] = []
                for rec in agent_state.recommendations:
                    if hasattr(rec, 'model_dump'):
                        result["recommendations"].append(rec.model_dump())
                    elif hasattr(rec, '__dict__'):
                        result["recommendations"].append(rec.__dict__)
                    else:
                        result["recommendations"].append(rec)
            
            return result
            
        except Exception as e:
            # Fallback to basic conversion
            return {
                "customer_id": getattr(agent_state, 'customer_id', ''),
                "customer_profile": None,
                "purchase_patterns": getattr(agent_state, 'purchase_patterns', None),
                "product_affinities": getattr(agent_state, 'product_affinities', None),
                "scored_opportunities": None,
                "research_report": getattr(agent_state, 'research_report', None),
                "recommendations": None,
                "error": f"Dict conversion error: {str(e)}"
            }

    def process_customer(self, customer_id: str) -> RecommendationResponse:
        """Process a customer through the entire workflow"""
        try:
            # Initialize state as dict (LangGraph format)
            initial_state = {
                "customer_id": customer_id,
                "customer_profile": None,
                "purchase_patterns": None,
                "product_affinities": None,
                "scored_opportunities": None,
                "research_report": None,
                "recommendations": None,
                "error": None
            }
            
            # Run the workflow
            final_state_dict = self.workflow.invoke(initial_state)
            
            # Ensure we have a dictionary
            if not isinstance(final_state_dict, dict):
                raise ValueError(f"Workflow returned {type(final_state_dict)}, expected dict")
            
            # Convert final state back to AgentState for easier handling
            final_state = self._dict_to_agent_state(final_state_dict)
            
            if final_state.error:
                return RecommendationResponse(
                    customer_id=customer_id,
                    research_report="",
                    recommendations=[],
                    success=False,
                    error=final_state.error
                )
            
            return RecommendationResponse(
                customer_id=customer_id,
                research_report=final_state.research_report or "",
                recommendations=final_state.recommendations or [],
                success=True
            )
            
        except Exception as e:
            return RecommendationResponse(
                customer_id=customer_id,
                research_report="",
                recommendations=[],
                success=False,
                error=f"Workflow execution error: {str(e)}"
            )