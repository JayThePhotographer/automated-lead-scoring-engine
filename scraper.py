import json
import time
import csv  
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_images(target_url, company_name):
    print(f"Starting scrape for: {company_name} at {target_url}")
    
    # Configure Chrome to run in headless mode (no GUI)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    
    scraped_data = {
        "company_name": company_name,
        "url": target_url,
        "image_urls": []
    }
    
    try:
        driver.get(target_url)
        
        # Wait for the body to load to ensure JavaScript renders the images
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Give it a brief pause for lazy-loaded images
        time.sleep(3) 
        
        # Find all image elements on the page
        images = driver.find_elements(By.TAG_NAME, 'img')
        
        for img in images:
            src = img.get_attribute('src')
            # Filter out empty sources, tiny icons, or SVGs
            if src and src.startswith('http') and not src.endswith('.svg'):
                scraped_data["image_urls"].append(src)
                
        # Remove duplicates
        scraped_data["image_urls"] = list(set(scraped_data["image_urls"]))
        
        print(f"Successfully extracted {len(scraped_data['image_urls'])} image URLs.")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        driver.quit()
        
    return scraped_data

def save_to_json(data, filename="scraped_leads.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    all_results = []
    
    # 1. Open and read the CSV file
    print("Reading targets from targets.csv...")
    try:
        with open('targets.csv', mode='r', encoding='utf-8') as file:
            # DictReader automatically turns each row into a dictionary using the headers
            csv_reader = csv.DictReader(file)
            
            # 2. Loop through each row in the CSV
            for row in csv_reader:
                target_name = row['name']
                target_url = row['url']
                
                print(f"\n--- Initiating Scrape: {target_name} ---")
                
                # Run the scraper
                result = scrape_images(target_url, target_name)
                all_results.append(result)
                
                # Rest to prevent rate-limiting
                print("Resting for 5 seconds...")
                time.sleep(5)
                
        # 3. Save all results to JSON
        save_to_json(all_results)
        print("\nBatch scraping complete! All data saved.")
        
    except FileNotFoundError:
        print("Error: Could not find targets.csv. Please ensure it exists in the same folder.")