#!/usr/bin/env python3
"""
Improved convenience script to run the Cross-Sell/Upsell Recommendation API
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if required files exist"""
    required_files = [
        'requirements.txt',
        'customer_data.csv',
        'main.py',
        'models.py',
        'agents.py',
        'langgraph_agent.py',
        'database.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files found")
    return True

def setup_env_file():
    """Setup .env file if it doesn't exist"""
    env_file = Path('.env')
    
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_content = """# OpenAI API Configuration
OPENAI_API_KEY=your_actual_openai_api_key_here

# Database Configuration (optional)
USE_DATABASE=false
DB_HOST=localhost
DB_PORT=5432
DB_NAME=customer_db
DB_USER=postgres
DB_PASSWORD=
"""
        env_file.write_text(env_content)
        print("✅ .env file created")
        print("⚠️  Please edit .env file and add your actual OpenAI API key")
        return False
    
    return True

def check_env_variables():
    """Check if required environment variables are set"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key or openai_key == 'your_actual_openai_api_key_here':
            print("❌ Please set your OPENAI_API_KEY in the .env file")
            print("   Edit the .env file and replace 'your_actual_openai_api_key_here' with your actual OpenAI API key")
            return False
        
        print("✅ OpenAI API key is configured")
        return True
        
    except ImportError:
        print("⚠️  python-dotenv not installed yet, will install with requirements")
        return True

def install_requirements():
    """Install Python requirements"""
    try:
        print("📦 Installing requirements...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True, check=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    try:
        print("🧪 Testing module imports...")
        
        # Test basic imports
        import pandas as pd
        import fastapi
        from dotenv import load_dotenv
        
        # Load environment
        load_dotenv()
        
        # Test OpenAI key
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key or openai_key == 'your_actual_openai_api_key_here':
            print("❌ OpenAI API key not properly configured")
            return False
            
        # Test project imports
        from models import AgentState, CustomerProfile
        from database import CSVDataManager
        
        # Test CSV data
        csv_manager = CSVDataManager()
        test_customer = csv_manager.get_customer_by_id('C001')
        if not test_customer:
            print("❌ Could not load test customer data")
            return False
            
        print("✅ All imports successful and data accessible")
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def run_server():
    """Run the FastAPI server"""
    try:
        print("🚀 Starting the Cross-Sell/Upsell Recommendation API...")
        print("📍 Server will be available at: http://localhost:8000")
        print("📖 API Documentation: http://localhost:8000/docs")
        print("🔍 Health Check: http://localhost:8000/health")
        print("👥 Customer List: http://localhost:8000/customers")
        print("🐛 Debug Info: http://localhost:8000/debug")
        print("\nSample test commands:")
        print("  curl http://localhost:8000/health")
        print("  curl http://localhost:8000/customers")
        print("  curl 'http://localhost:8000/recommendation?customer_id=C001'")
        print("\nPress Ctrl+C to stop the server\n")
        
        # Start with more verbose logging
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'main:app', 
            '--host', '0.0.0.0', 
            '--port', '8000', 
            '--reload',
            '--log-level', 'info'
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

def main():
    """Main function"""
    print("🤖 Cross-Sell/Upsell Recommendation API Setup")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Setup .env file
    if not setup_env_file():
        print("\n⚠️  Please edit the .env file with your OpenAI API key and run again")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Check environment variables after installation
    if not check_env_variables():
        sys.exit(1)
    
    # Test imports and data access
    if not test_imports():
        sys.exit(1)
    
    # Run server
    run_server()

if __name__ == "__main__":
    main()