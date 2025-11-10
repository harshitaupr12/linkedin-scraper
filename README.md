LinkedIn Profile Scraper 🔍

A powerful Flask web application to scrape LinkedIn profiles with anti-detection features and real-time progress tracking.
Features ✨

🌐 Web Interface - User-friendly dashboard for easy scraping
🔐 Secure Login - LinkedIn authentication handling
📊 Real-time Progress - Live progress tracking with progress bar
📁 CSV Export - Download results in CSV format
🛡️ Anti-Detection - Advanced techniques to avoid blocking
⚡ Multi-threading - Background scraping without blocking UI
📱 Responsive Design - Works on desktop and mobile

Installation 🚀
Prerequisites
Python 3.8+
Google Chrome browser
LinkedIn account

1. Clone Repository
git clone https://github.com/harshitaupr12/linkedin-scraper.git
cd linkedin-scraper

2. Install Dependencies
pip install -r REQUIREMENTS.TXT

3. Run Application
python app.py

4. Access Application
Open browser and navigate to:
http://localhost

Usage 📖
Login - Enter your LinkedIn credentials
Add URLs - Paste LinkedIn profile URLs (one per line)
Start Scraping - Click "Start Scraping" button
Monitor Progress - Watch real-time progress
Download Results - Export data as CSV file

Data Collected 📊
The scraper extracts following information:
👤 Name - Full name
💼 Headline - Professional headline
📝 About - Profile summary
📍 Location - Geographic location
🔗 Profile URL - LinkedIn profile link
⏰ Scraped At - Timestamp of scraping

Anti-Detection Features 🛡️
Random User Agents - Rotates browser signatures
Human-like Delays - Random timing between actions
Stealth Mode - Hides automation indicators
Window Randomization - Varies browser window sizes
Pattern Avoidance - No fixed timing patterns


Project Structure 📁
linkedin-scraper/
├── app.py                 # Main Flask application
├── REQUIREMENTS.TXT       # Python dependencies
├── runtime.txt            # Python version
├── templates/            # HTML templates
│   ├── login.html
│   ├── dashboard.html
│   └── index.html
├── static/              # CSS & JavaScript
│   ├── style.css
│   └── script.js
└── README.md            # Project documentation


Technologies Used 💻
Backend: Flask, Python
Web Scraping: Selenium, Chrome Driver
Frontend: HTML5, CSS3, JavaScript
Data Handling: Pandas
Authentication: Flask Sessions


Important Notes ⚠️
🔒 Credentials are not stored - Only used for current session
⚖️ Use responsibly - Respect LinkedIn's Terms of Service
🐛 Rate Limiting - Built-in delays to avoid blocking
📧 Test Accounts - Recommended to use test accounts


Troubleshooting 🔧
Common Issues:
Chrome Driver Errors
Ensure Google Chrome is installed
App automatically downloads ChromeDriver
Login Failures
Check LinkedIn credentials
Verify account is not locked
Scraping Blocked
Use anti-detection features
Try with different accounts

Debug Mode:
python app.py --debug


Contributing 🤝
Contributions are welcome! Please feel free to submit a Pull Request.
Fork the project
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request


License 📄
This project is for educational purposes. Please use responsibly and respect website terms of service.

Developer 
Harshita Upreti
GitHub: @harshitaupr12
Project: LinkedIn Scraper


