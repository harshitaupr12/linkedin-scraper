from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import pandas as pd
import time
import os
import threading
import random
from datetime import datetime

load_dotenv()
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Global variable to store scraping status
scraping_status = {"running": False, "progress": 0, "current_profile": "", "total": 0, "data": []}

def setup_driver():
    print("Setting up Chrome driver with anti-detection features...")
    options = webdriver.ChromeOptions()
    
    # Basic options
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Anti-detection features
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Random user agents
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'
    ]
    options.add_argument(f'--user-agent={random.choice(user_agents)}')
    
    # Window size randomization
    window_sizes = ['--window-size=1920,1080', '--window-size=1366,768', '--window-size=1536,864']
    options.add_argument(random.choice(window_sizes))
    
    # Additional stealth options
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-images')
    options.add_argument('--disable-javascript')  # Optional: for faster loading
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Execute CDP commands to prevent detection
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": random.choice(user_agents)
    })
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def smart_delay(min_seconds=3, max_seconds=8):
    """Random delay to mimic human behavior"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def login_to_linkedin(driver, email, password):
    driver.get("https://www.linkedin.com/login")
    smart_delay(3, 5)
    
    email_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    
    # Type with human-like delays
    for char in email:
        email_field.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))
    
    smart_delay(1, 2)
    
    for char in password:
        password_field.send_keys(char)
        time.sleep(random.uniform(0.05, 0.2))
    
    smart_delay(1, 2)
    
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    smart_delay(4, 7)  # Longer delay for login processing
    
    # Check if login was successful
    if "feed" in driver.current_url or "dashboard" in driver.current_url:
        return True
    else:
        print("Login might have failed - check credentials or CAPTCHA")
        return False

def scrape_linkedin_profile(driver, profile_url, index, total):
    try:
        scraping_status["current_profile"] = f"Scraping {index}/{total}: {profile_url}"
        scraping_status["progress"] = int((index / total) * 100)
        
        driver.get(profile_url)
        smart_delay(3, 6)  # Random delay between page loads
        
        # Extract data
        name = driver.find_element(By.TAG_NAME, "h1").text
        
        try:
            headline = driver.find_element(By.CLASS_NAME, "text-body-medium").text
        except:
            headline = "Not found"
        
        try:
            about = driver.find_element(By.XPATH, "//section[contains(@class, 'core-section-container')]").text
        except:
            about = "Not found"
            
        # Try to get location
        try:
            location = driver.find_element(By.XPATH, "//span[contains(@class, 'text-body-small')]").text
        except:
            location = "Not found"
        
        # Try to get additional info
        try:
            experience = driver.find_element(By.XPATH, "//section[contains(@class, 'experience')]").text[:300] + "..."
        except:
            experience = "Not found"
            
        try:
            education = driver.find_element(By.XPATH, "//section[contains(@class, 'education')]").text[:300] + "..."
        except:
            education = "Not found"
        
        print(f"Scraped: {name}")
        
        return {
            'Name': name,
            'Headline': headline,
            'About': about[:500] + "..." if len(about) > 500 else about,
            'Location': location,
            'Experience_Snippet': experience,
            'Education_Snippet': education,
            'Profile URL': profile_url,
            'Scraped At': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        print(f"Error scraping {profile_url}: {str(e)}")
        return None

def scrape_profiles_async(profile_urls, email, password):
    global scraping_status
    scraping_status = {"running": True, "progress": 0, "current_profile": "", "total": len(profile_urls), "data": []}
    
    driver = setup_driver()
    scraped_data = []
    
    try:
        if login_to_linkedin(driver, email, password):
            for i, url in enumerate(profile_urls, 1):
                profile_data = scrape_linkedin_profile(driver, url, i, len(profile_urls))
                if profile_data:
                    scraped_data.append(profile_data)
                
                # Random delay between profiles (avoid pattern)
                if i < len(profile_urls):  # No delay after last profile
                    smart_delay(2, 5)
            
            # Save to CSV
            if scraped_data:
                df = pd.DataFrame(scraped_data)
                filename = f'scraped_profiles_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
                df.to_csv(filename, index=False)
                scraping_status["result"] = "success"
                scraping_status["message"] = f"Successfully scraped {len(scraped_data)} profiles"
                scraping_status["filename"] = filename
                scraping_status["data"] = scraped_data
            else:
                scraping_status["result"] = "error"
                scraping_status["message"] = "No data scraped"
                
    except Exception as e:
        scraping_status["result"] = "error"
        scraping_status["message"] = f"Error: {str(e)}"
    finally:
        driver.quit()
        scraping_status["running"] = False

# Routes (remain the same as before)
@app.route('/')
def index():
    if 'linkedin_email' not in session:
        return redirect('/login')
    return redirect('/dashboard')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['linkedin_email'] = request.form['email']
        session['linkedin_password'] = request.form['password']
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'linkedin_email' not in session:
        return redirect('/login')
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/start_scraping', methods=['POST'])
def start_scraping():
    if 'linkedin_email' not in session:
        return jsonify({"error": "Please login first"})
    
    if scraping_status["running"]:
        return jsonify({"error": "Scraping already in progress"})
    
    profile_urls = request.json.get('urls', [])
    if not profile_urls:
        return jsonify({"error": "No URLs provided"})
    
    # Start scraping in background thread
    thread = threading.Thread(
        target=scrape_profiles_async, 
        args=(profile_urls, session['linkedin_email'], session['linkedin_password'])
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({"message": "Scraping started", "total": len(profile_urls)})

@app.route('/scraping_status')
def get_scraping_status():
    return jsonify(scraping_status)

@app.route('/download_csv')
def download_csv():
    if 'filename' in scraping_status:
        return send_file(scraping_status['filename'], as_attachment=True)
    return "No file available"

@app.route('/results')
def results():
    if 'linkedin_email' not in session:
        return redirect('/login')
    return render_template('results.html', data=scraping_status.get('data', []))

if __name__ == '__main__':
    app.run(debug=True)
