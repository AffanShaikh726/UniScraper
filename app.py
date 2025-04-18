from flask import Flask, render_template
from flask_caching import Cache
from scraper import scrape_data
from threading import Lock

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Create a global lock for scrape_data
scrape_lock = Lock()

@cache.cached(timeout=2*60)
def get_cached_data():
    # Acquire the lock to ensure only one scrape_data runs at a time
    if not scrape_lock.acquire(blocking=False):
        # If another scrape_data is running, return a message or cached data
        return {"error": "Scraping is already in progress. Please try again later."}
    
    try:
        # Call the scrape_data function
        return scrape_data()
    finally:
        # Release the lock after scraping is complete
        scrape_lock.release()

@app.route('/')
def index():
    return render_template('index.html', content="")

@app.route('/api/data', methods=['GET'])
def get_data():
    print("API endpoint hit")
    data = get_cached_data()
    return data

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Flask app name:", app.name)
    app.run(debug=True, host='0.0.0.0', port=5000)
