# Cross-Sell/Upsell Recommendation System

A LangGraph-powered agent system that analyzes customer data to generate intelligent cross-sell and upsell recommendations along with detailed research reports.

## 🏗️ Architecture

The system uses LangGraph to orchestrate multiple specialized agents:

1. **Customer Context Agent** - Extracts customer profile from data source
2. **Purchase Pattern Analysis Agent** - Identifies buying patterns and gaps
3. **Product Affinity Agent** - Suggests complementary products
4. **Opportunity Scoring Agent** - Scores and prioritizes recommendations
5. **Recommendation Report Agent** - Generates comprehensive research reports

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- PostgreSQL (optional, uses CSV by default)

### Installation & Setup

1. **Clone/Download the project files**

2. **Set up environment variables**
   ```bash
   # Copy and edit the .env file
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```

3. **Run the application**
   ```bash
   python run.py
   ```
   
   This script will:
   - Install all required dependencies
   - Validate configuration
   - Start the FastAPI server

### Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 📊 Data Sources

### CSV Mode (Default)
The system uses `customer_data.csv` with customer information including:
- Customer profile (industry, revenue, employees)
- Current products and usage
- Cross-sell synergy opportunities
- Account status and activity

### PostgreSQL Mode (Optional)
1. Set up PostgreSQL database:
   ```bash
   psql -U postgres -f setup_database.sql
   ```

2. Update `.env` file:
   ```
   USE_DATABASE=true
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=customer_db
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```

## 🔌 API Usage

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Get Recommendations
```bash
GET /recommendation?customer_id=C001
```

**Example Response:**
```json
{
  "customer_id": "C001",
  "success": true,
  "research_report": "# Research Report: Cross-Sell and Upsell Opportunities for Edge Communications\n\n## Executive Summary\nThis report analyzes Edge Communications...",
  "recommendations": [
    {
      "product_name": "Advanced Security Suite",
      "recommendation_type": "cross-sell",
      "confidence_score": 0.85,
      "rationale": "High synergy with existing Core Management Platform",
      "estimated_value": 45000
    }
  ]
}
```

#### List Customers
```bash
GET /customers
```

#### Health Check
```bash
GET /health
```

### Example Usage

```bash
# Get recommendations for customer C001
curl "http://localhost:8000/recommendation?customer_id=C001"

# List all available customers
curl "http://localhost:8000/customers"

# Alternative path parameter format
curl "http://localhost:8000/recommendation/C003"
```

## 🎯 Sample Customer IDs

Try these customer IDs to test the system:
- `C001` - Edge Communications (Electronics)
- `C003` - Pyramid Construction Inc. (Construction)
- `C005` - United Oil & Gas Corp. (Energy)
- `C007` - Global Retail Inc. (Retail)
- `C009` - Metro Health Systems (Healthcare)

## 📋 API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `USE_DATABASE` | Use PostgreSQL instead of CSV | `false` |
| `DB_HOST` | Database host | `localhost` |
| `DB_PORT` | Database port | `5432` |
| `DB_NAME` | Database name | `customer_db` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | - |

### Agent Configuration

The LangGraph workflow can be customized by modifying:
- `agents.py` - Individual agent logic
- `langgraph_agent.py` - Workflow orchestration
- `models.py` - Data structures

## 🏢 Project Structure

```
├── main.py                 # FastAPI application
├── run.py                  # Convenience runner script
├── requirements.txt        # Python dependencies
├── .env                   # Environment configuration
├── customer_data.csv      # Sample customer data
├── models.py             # Pydantic models
├── database.py           # Data access layer
├── agents.py             # LangGraph agents
├── langgraph_agent.py    # Workflow orchestration
├── setup_database.sql    # PostgreSQL setup
└── README.md            # This file
```

## 🔍 How It Works

1. **Customer Context**: Retrieves customer profile from CSV/database
2. **Pattern Analysis**: Uses GPT to analyze purchase patterns and identify gaps
3. **Product Affinity**: Generates complementary product suggestions
4. **Opportunity Scoring**: Scores each opportunity with confidence and value estimates
5. **Report Generation**: Creates comprehensive business reports with actionable insights


## 📈 Sample Output

The system generates professional research reports with:

- **Executive Summary** - Key findings and recommendations
- **Customer Overview** - Profile and current state
- **Market Analysis** - Industry context and benchmarking  
- **Opportunity Analysis** - Detailed scoring and rationale
- **Recommendations** - Prioritized action items
- **Implementation Strategy** - Next steps

## 🔮 Future Enhancements

- Real-time data integration
- Advanced ML-based scoring
- Multi-language support
- Custom industry templates
- Integration with CRM systems
