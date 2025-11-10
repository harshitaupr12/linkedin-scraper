function startScraping() {
    const urlsText = document.getElementById('profileUrls').value;
    const urls = urlsText.split('\n').filter(url => url.trim() !== '');
    
    if (urls.length === 0) {
        alert('Please enter at least one LinkedIn profile URL');
        return;
    }

    // Show progress section
    document.getElementById('progressSection').classList.remove('hidden');
    document.getElementById('resultSection').classList.add('hidden');
    
    // Start scraping
    fetch('/start_scraping', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ urls: urls })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        // Start checking progress
        checkProgress();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error starting scraping');
    });
}

function checkProgress() {
    fetch('/scraping_status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('progressFill').style.width = data.progress + '%';
            document.getElementById('progressText').textContent = `Progress: ${data.progress}%`;
            document.getElementById('currentProfile').textContent = data.current_profile;
            
            if (data.running) {
                // Continue checking every 2 seconds
                setTimeout(checkProgress, 2000);
            } else {
                // Show result
                document.getElementById('resultMessage').textContent = data.message;
                document.getElementById('resultSection').classList.remove('hidden');
                
                if (data.result === 'success') {
                    document.getElementById('progressFill').style.backgroundColor = '#28a745';
                } else {
                    document.getElementById('progressFill').style.backgroundColor = '#dc3545';
                }
            }
        });
}

function downloadCSV() {
    window.location.href = '/download_csv';
}