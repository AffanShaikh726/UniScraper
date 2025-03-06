from flask import Flask, jsonify, render_template
from flask_caching import Cache
from scraper import scrape_data
import threading

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
lock = threading.Lock()
is_fetching = False
cached_data = None

def fetch_data():
    global is_fetching, cached_data
    with lock:
        if not is_fetching:
            is_fetching = True
            try:
                print("Fetching new data")
                cached_data = scrape_data()
            finally:
                is_fetching = False
        else:
            print("Data is already being fetched")
    return cached_data

@cache.cached(timeout=2*100)
def get_cached_data():
    global cached_data
    if cached_data is None:
        cached_data = fetch_data()
    return cached_data

@app.route('/')
def index():
    return render_template('index.html', content="")

@app.route('/api/data', methods=['GET'])
def get_data():
    print("API endpoint hit")
    data = get_cached_data()
    if data is None:
        return jsonify({"error": "Data is currently being fetched, please try again later"}), 503
    return jsonify(data)

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Flask app name:", app.name)
    app.run(debug=True, host='0.0.0.0', port=5000)