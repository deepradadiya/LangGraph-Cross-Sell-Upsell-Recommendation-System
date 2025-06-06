import psycopg2
from psycopg2 import sql
import os
from typing import Optional, Dict, Any
import pandas as pd
from models import CustomerProfile

class DatabaseManager:
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '5432')
        self.database = os.getenv('DB_NAME', 'customer_db')
        self.user = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD', '')

    def get_connection(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )

    def create_table(self):
        """Create the customer_data table"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS customer_data (
            customer_id VARCHAR(10) PRIMARY KEY,
            customer_name VARCHAR(255),
            industry VARCHAR(100),
            annual_revenue BIGINT,
            number_of_employees INTEGER,
            customer_priority_rating VARCHAR(50),
            account_type VARCHAR(100),
            location VARCHAR(255),
            current_products TEXT,
            product_usage FLOAT,
            cross_sell_synergy TEXT,
            last_activity_date DATE,
            opportunity_stage VARCHAR(100),
            opportunity_amount INTEGER,
            opportunity_type VARCHAR(100),
            competitors TEXT,
            activity_status VARCHAR(50),
            activity_priority VARCHAR(50),
            activity_type VARCHAR(50),
            product_sku VARCHAR(50)
        );
        """
        
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(create_table_sql)
                    conn.commit()
            print("Table created successfully")
        except Exception as e:
            print(f"Error creating table: {e}")

    def insert_sample_data(self):
        """Insert sample data from CSV"""
        try:
            df = pd.read_csv('customer_data.csv')
            
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    for _, row in df.iterrows():
                        insert_sql = """
                        INSERT INTO customer_data 
                        (customer_id, customer_name, industry, annual_revenue, number_of_employees,
                         customer_priority_rating, account_type, location, current_products,
                         product_usage, cross_sell_synergy, last_activity_date, opportunity_stage,
                         opportunity_amount, opportunity_type, competitors, activity_status,
                         activity_priority, activity_type, product_sku)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (customer_id) DO NOTHING;
                        """
                        cursor.execute(insert_sql, tuple(row))
                    conn.commit()
            print("Sample data inserted successfully")
        except Exception as e:
            print(f"Error inserting sample data: {e}")

    def get_customer_by_id(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Fetch customer data by ID"""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM customer_data WHERE customer_id = %s",
                        (customer_id,)
                    )
                    row = cursor.fetchone()
                    if row:
                        columns = [desc[0] for desc in cursor.description]
                        return dict(zip(columns, row))
            return None
        except Exception as e:
            print(f"Error fetching customer: {e}")
            return None

class CSVDataManager:
    def __init__(self, csv_file: str = 'customer_data.csv'):
        self.csv_file = csv_file
        self.df = pd.read_csv(csv_file)

    def get_customer_by_id(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Fetch customer data by ID from CSV"""
        try:
            customer_row = self.df[self.df['Customer ID'] == customer_id]
            if not customer_row.empty:
                return customer_row.iloc[0].to_dict()
            return None
        except Exception as e:
            print(f"Error fetching customer: {e}")
            return None

    def parse_customer_profile(self, customer_data: Dict[str, Any]) -> CustomerProfile:
        """Parse raw customer data into CustomerProfile model"""
        current_products = [prod.strip() for prod in str(customer_data.get('Current Products', '')).split(',')]
        cross_sell_synergy = [prod.strip() for prod in str(customer_data.get('Cross-Sell Synergy', '')).split(',')]
        competitors = [comp.strip() for comp in str(customer_data.get('Competitors', '')).split(',')]
        
        return CustomerProfile(
            customer_id=customer_data.get('Customer ID', ''),
            customer_name=customer_data.get('Customer Name', ''),
            industry=customer_data.get('Industry', ''),
            annual_revenue=int(customer_data.get('Annual Revenue (USD)', 0)),
            number_of_employees=int(customer_data.get('Number of Employees', 0)),
            customer_priority_rating=customer_data.get('Customer Priority Rating', ''),
            account_type=customer_data.get('Account Type', ''),
            location=customer_data.get('Location', ''),
            current_products=current_products,
            product_usage=float(customer_data.get('Product Usage (%)', 0)),
            cross_sell_synergy=cross_sell_synergy,
            last_activity_date=customer_data.get('Last Activity Date', ''),
            opportunity_stage=customer_data.get('Opportunity Stage', ''),
            opportunity_amount=int(customer_data.get('Opportunity Amount (USD)', 0)),
            opportunity_type=customer_data.get('Opportunity Type', ''),
            competitors=competitors,
            activity_status=customer_data.get('Activity Status', ''),
            activity_priority=customer_data.get('Activity Priority', ''),
            activity_type=customer_data.get('Activity Type', ''),
            product_sku=customer_data.get('Product SKU', '')
        )