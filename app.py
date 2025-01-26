from flask import Flask, jsonify
from scraper import scrape_data

app = Flask(__name__)
data = scrape_data()

@app.route('/api/data', methods=['GET'])
def get_data():
    print("API endpoint hit")
    # print("Data scraped:", data)
    return jsonify({"data": data})

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Flask app name:", app.name)
    app.run(debug=True, host='0.0.0.0', port=5000)
    