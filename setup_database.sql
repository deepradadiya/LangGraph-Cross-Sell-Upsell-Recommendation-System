-- PostgreSQL Database Setup Script
-- Run this script to set up the database for the Cross-Sell/Upsell Recommendation System

-- Create database (run this as superuser)
CREATE DATABASE customer_db;

-- Connect to the database
\c customer_db;

-- Create the customer_data table
CREATE TABLE IF NOT EXISTS customer_data (
    customer_id VARCHAR(10) PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
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

-- Insert sample data
INSERT INTO customer_data 
(customer_id, customer_name, industry, annual_revenue, number_of_employees,
 customer_priority_rating, account_type, location, current_products,
 product_usage, cross_sell_synergy, last_activity_date, opportunity_stage,
 opportunity_amount, opportunity_type, competitors, activity_status,
 activity_priority, activity_type, product_sku)
VALUES 
('C001', 'Edge Communications', 'Electronics', 139000000, 1000, 'Medium', 'Hot Customer - Direct', 'Austin, TX, USA', 'Core Management Platform', 100, 'Collaboration Suite, E', '2024-11-19', 'Closed Won', 75000, 'New Customer', 'John Deere, Mitsubishi', 'Completed', 'High', 'Call', 'GC1060'),
('C002', 'Burlington Textiles Corp', 'Apparel', 350000000, 9000, 'High', 'Warm Customer - Direct', 'Burlington, NC, USA', 'Collaboration Suite', 85, 'Advanced Analytics, F', '2024-11-19', 'Closed Won', 235000, 'New Customer', 'John Deere', 'Completed', 'Medium', 'Email', 'GC1040'),
('C003', 'Pyramid Construction Inc.', 'Construction', 950000000, 2680, 'High', 'Warm Customer - Channel', 'Paris, France', 'Advanced Analytics', 70, 'Workflow Automation, G', '2024-11-19', 'Prospecting', 10000, 'Existing Customer - Upgrade', 'Caterpillar', 'Open', 'High', 'Call', 'GC5020'),
('C004', 'Grand Hotels & Resorts', 'Hospitality', 500000000, 5600, 'High', 'Warm Customer - Direct', 'Chicago, IL, USA', 'Reporting Dashboard', 65, 'API Integrations, H', '2024-11-19', 'Closed Won', 210000, 'Existing Customer - Upgrade', 'Fujitsu', 'Completed', 'High', 'Email', 'GC3040'),
('C005', 'United Oil & Gas Corp.', 'Energy', 5600000000, 145000, 'High', 'Hot Customer - Direct', 'New York, NY, USA', 'Workflow Automation', 60, 'AI Insights Module, J', '2024-11-19', 'Negotiation/Review', 270000, 'Existing Customer - Upgrade', 'Caterpillar, Hawkpower', 'Open', 'Medium', 'Call', 'SL9080'),
('C006', 'Green Energy Solutions', 'Energy', 420000000, 3200, 'Medium', 'Cold Customer - Channel', 'Houston, TX, USA', 'API Integrations', 45, 'IoT Monitoring, K', '2024-11-20', 'Qualification', 5000, 'New Customer', 'Schneider Electric', 'Open', 'Low', 'Email', 'SL2010'),
('C007', 'Global Retail Inc.', 'Retail', 780000000, 12000, 'High', 'Hot Customer - Direct', 'London, UK', 'AI Insights Module', 90, 'Predictive Analytics, L', '2024-11-20', 'Closed Won', 185000, 'Existing Customer - Upgrade', 'Amazon, Walmart', 'Completed', 'High', 'Meeting', 'GC5050'),
('C008', 'Tech Innovators LLC', 'Technology', 150000000, 800, 'Low', 'Warm Customer - Direct', 'San Francisco, CA, USA', 'IoT Monitoring', 55, 'Cloud Migration, M', '2024-11-20', 'Prospecting', 15000, 'New Customer', 'IBM', 'Open', 'Medium', 'Call', 'SL3020'),
('C009', 'Metro Health Systems', 'Healthcare', 670000000, 4500, 'High', 'Hot Customer - Channel', 'Boston, MA, USA', 'Predictive Analytics', 75, 'Telehealth Suite, N', '2024-11-21', 'Negotiation/Review', 95000, 'Existing Customer - Upgrade', 'GE Healthcare, Siemens', 'Open', 'High', 'Email', 'GC7080'),
('C010', 'Summit Manufacturing', 'Manufacturing', 890000000, 6000, 'Medium', 'Warm Customer - Direct', 'Detroit, MI, USA', 'Cloud Migration', 50, 'Robotics Automation, P', '2024-11-21', 'Closed Lost', 0, 'New Customer', 'ABB, Fanuc', 'Completed', 'Low', 'Call', 'SL4010'),
('C011', 'Alpha Financial Services', 'Finance', 1200000000, 8500, 'High', 'Hot Customer - Direct', 'Charlotte, NC, USA', 'Telehealth Suite', 80, 'Blockchain Security, Q', '2024-11-21', 'Closed Won', 320000, 'Existing Customer - Upgrade', 'Goldman Sachs, JPMorgan', 'Completed', 'High', 'Meeting', 'GC6060'),
('C012', 'Precision Tools Corp', 'Industrial', 290000000, 2000, 'Low', 'Cold Customer - Channel', 'Berlin, Germany', 'Robotics Automation', 40, 'Predictive Maintenance, R', '2024-11-22', 'Qualification', 8000, 'New Customer', 'Bosch', 'Open', 'Low', 'Email', 'SL2030'),
('C013', 'Oceanic Shipping', 'Logistics', 510000000, 3800, 'Medium', 'Warm Customer - Direct', 'Miami, FL, USA', 'Blockchain Security', 65, 'Supply Chain AI, S', '2024-11-22', 'Prospecting', 25000, 'Existing Customer - Upgrade', 'Maersk, FedEx', 'Open', 'Medium', 'Call', 'GC4040'),
('C014', 'Stellar Entertainment', 'Media', 230000000, 1500, 'Low', 'Warm Customer - Channel', 'Los Angeles, CA, USA', 'Predictive Maintenance', 70, 'Content Analytics, T', '2024-11-23', 'Closed Won', 110000, 'New Customer', 'Netflix, Disney', 'Completed', 'Medium', 'Email', 'GC8080'),
('C015', 'AgriGrowth Farms', 'Agriculture', 180000000, 1200, 'Medium', 'Cold Customer - Direct', 'Des Moines, IA, USA', 'Supply Chain AI', 30, 'AgriTech Sensors, U', '2024-11-23', 'Negotiation/Review', 45000, 'Existing Customer - Upgrade', 'Monsanto, Cargill', 'Open', 'Low', 'Call', 'SL1050');

-- Create indexes for better performance
CREATE INDEX idx_customer_industry ON customer_data(industry);
CREATE INDEX idx_customer_priority ON customer_data(customer_priority_rating);
CREATE INDEX idx_customer_revenue ON customer_data(annual_revenue);

-- Grant permissions (adjust username as needed)
-- GRANT ALL PRIVILEGES ON customer_data TO your_username;