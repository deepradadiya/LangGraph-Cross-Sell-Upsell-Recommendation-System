from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from dotenv import load_dotenv
from langgraph_agent import CrossSellUpsellAgent
from models import RecommendationResponse
from database import DatabaseManager

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Validate OpenAI API key
openai_key = os.getenv('OPENAI_API_KEY')
if not openai_key or openai_key == 'your_actual_openai_api_key_here':
    logger.error("OPENAI_API_KEY environment variable is required and must be set to a valid key")
    raise ValueError("OPENAI_API_KEY environment variable is required and must be set to a valid key")

logger.info(f"OpenAI API Key configured: {bool(openai_key)}")

app = FastAPI(
    title="Cross-Sell/Upsell Recommendation API",
    description="LangGraph-powered agent for generating cross-sell and upsell recommendations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent with error handling
try:
    agent = CrossSellUpsellAgent()
    logger.info("CrossSellUpsellAgent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize agent: {e}")
    agent = None

@app.on_event("startup")
async def setup_database():
    """Setup database if using PostgreSQL"""
    try:
        if os.getenv('USE_DATABASE', 'false').lower() == 'true':
            db_manager = DatabaseManager()
            db_manager.create_table()
            db_manager.insert_sample_data()
            logger.info("Database setup completed")
        else:
            logger.info("Using CSV data source")
            # Verify CSV file exists
            if not os.path.exists('customer_data.csv'):
                logger.error("customer_data.csv file not found!")
                raise FileNotFoundError("customer_data.csv file not found!")
            logger.info("CSV file found and ready to use")
    except Exception as e:
        logger.error(f"Database/CSV setup error: {e}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Cross-Sell/Upsell Recommendation API is running",
        "status": "healthy",
        "data_source": "PostgreSQL" if os.getenv('USE_DATABASE', 'false').lower() == 'true' else "CSV",
        "agent_initialized": agent is not None,
        "endpoints": {
            "recommendations": "/recommendation?customer_id=<id>",
            "health": "/health",
            "customers": "/customers"
        }
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "openai_configured": bool(os.getenv('OPENAI_API_KEY')),
        "database_enabled": os.getenv('USE_DATABASE', 'false').lower() == 'true',
        "csv_file_exists": os.path.exists('customer_data.csv'),
        "agent_ready": agent is not None
    }

@app.get("/customers")
async def list_customers():
    """List available customer IDs"""
    try:
        import pandas as pd
        
        if not os.path.exists('customer_data.csv'):
            raise HTTPException(status_code=500, detail="customer_data.csv file not found")
            
        df = pd.read_csv('customer_data.csv')
        customers = df[['Customer ID', 'Customer Name', 'Industry']].to_dict('records')
        
        logger.info(f"Found {len(customers)} customers in CSV")
        
        return {
            "customers": customers,
            "total_count": len(customers)
        }
    except Exception as e:
        logger.error(f"Error loading customer list: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading customer list: {str(e)}")

@app.get("/recommendation", response_model=RecommendationResponse)
async def get_recommendation(
    customer_id: str = Query(..., description="Customer ID to analyze")
):
    """
    Generate cross-sell and upsell recommendations for a specific customer
    
    Args:
        customer_id: The ID of the customer to analyze (e.g., C001, C002, etc.)
    
    Returns:
        RecommendationResponse containing research report and recommendations
    """
    try:
        logger.info(f"Processing recommendation request for customer: {customer_id}")
        
        # Check if agent is initialized
        if agent is None:
            logger.error("Agent not initialized")
            raise HTTPException(status_code=500, detail="Agent not initialized properly")
        
        # Validate customer_id format
        if not customer_id or len(customer_id.strip()) == 0:
            raise HTTPException(status_code=400, detail="Customer ID cannot be empty")
        
        customer_id = customer_id.strip()
        logger.info(f"Processing customer: {customer_id}")
        
        # Process the customer through the agent workflow
        result = agent.process_customer(customer_id)
        
        logger.info(f"Agent processing completed. Success: {result.success}")
        
        if not result.success:
            logger.error(f"Agent processing failed: {result.error}")
            raise HTTPException(status_code=404, detail=result.error)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_recommendation: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/recommendation/{customer_id}", response_model=RecommendationResponse)
async def get_recommendation_path(customer_id: str):
    """
    Alternative endpoint with customer_id as path parameter
    """
    logger.info(f"Path parameter request for customer: {customer_id}")
    return await get_recommendation(customer_id=customer_id)

# Debug endpoint to check agent status
@app.get("/debug")
async def debug_info():
    """Debug information endpoint"""
    return {
        "agent_initialized": agent is not None,
        "openai_key_set": bool(os.getenv('OPENAI_API_KEY')),
        "csv_exists": os.path.exists('customer_data.csv'),
        "use_database": os.getenv('USE_DATABASE', 'false').lower() == 'true',
        "python_path": os.getcwd(),
        "env_vars": {
            "OPENAI_API_KEY": "***SET***" if os.getenv('OPENAI_API_KEY') else "NOT SET",
            "USE_DATABASE": os.getenv('USE_DATABASE', 'false')
        }
    }

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server manually...")
    uvicorn.run(app, host="0.0.0.0", port=8000)