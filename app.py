from flask import Flask, jsonify, render_template
from flask_caching import Cache
from scraper import scrape_data
import threading

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Lock and shared variables
lock = threading.Lock()
is_fetching = False
cached_data = None

def fetch_data():
    global is_fetching, cached_data
    # Check if data is already being fetched
    with lock:
        if is_fetching:
            print("Data is already being fetched. Waiting for it to complete...")
            return None  # Return None to indicate that fetching is in progress
        if cached_data is not None:
            print("Using cached data.")
            return cached_data  # Return cached data if available
        is_fetching = True  # Mark as fetching

    # Fetch data outside the lock to avoid blocking other threads
    try:
        print("Fetching new data...")
        data = scrape_data()  # Fetch the data
        with lock:
            cached_data = data  # Update the cached data
    except Exception as e:
        print(f"Error while fetching data: {e}")
        data = None
    finally:
        with lock:
            is_fetching = False  # Mark fetching as complete
    return data

@app.route('/')
def index():
    return render_template('index.html', content="")

@app.route('/api/data', methods=['GET'])
def get_data():
    print("API endpoint hit")
    global cached_data
    data = fetch_data()
    if data is None:
        # If data is still being fetched, return a message to the client
        return jsonify({"message": "Data is currently being fetched. Please try again later."}), 202
    return jsonify(data)

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Flask app name:", app.name)
    app.run(debug=True, host='0.0.0.0', port=5000)