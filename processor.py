import json
import sqlite3
import random

def setup_database():
    # Connect to SQLite (this creates a file named leads.db)
    conn = sqlite3.connect('leads.db')
    cursor = conn.cursor()
    
    # Create tables for our data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            website_url TEXT,
            overall_score INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS media_audits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER,
            image_url TEXT,
            deficit_tag TEXT,
            FOREIGN KEY(company_id) REFERENCES companies(id)
        )
    ''')
    
    conn.commit()
    return conn

def process_leads(json_file):
    conn = setup_database()
    cursor = conn.cursor()
    
    # Load the scraped data
    with open(json_file, 'r') as file:
        data = json.load(file)
        
    print(f"Processing {len(data)} companies...")
    
    # Possible visual flaws our "AI" might detect
    deficits = ["Low Resolution", "Poor Lighting", "Outdated Styling", "Improper Cropping", "No Deficit"]
    
    for item in data:
        company_name = item['company_name']
        url = item['url']
        images = item['image_urls']
        
        # Simulate business logic: Calculate a Lead Score (1-10)
        # In a real app, this would be based on the AI vision API results
        lead_score = random.randint(6, 10) if len(images) > 0 else 10
        
        # Insert company into database
        cursor.execute('''
            INSERT INTO companies (company_name, website_url, overall_score)
            VALUES (?, ?, ?)
        ''', (company_name, url, lead_score))
        
        company_id = cursor.lastrowid
        
        # Process and tag each image
        for img_url in images:
            # Simulate the vision AI assigning a deficit tag
            assigned_deficit = random.choice(deficits)
            
            cursor.execute('''
                INSERT INTO media_audits (company_id, image_url, deficit_tag)
                VALUES (?, ?, ?)
            ''', (company_id, img_url, assigned_deficit))
            
    conn.commit()
    conn.close()
    print("Data processing complete. Saved to leads.db")

if __name__ == "__main__":
    # Points to the JSON file generated
    process_leads('scraped_leads.json')
