from flask import Flask, jsonify, render_template
from scraper import scrape_data

app = Flask(__name__)

# data = scrape_data()

# Method 1: Read entire file as string
with open("jsonFormat.txt", "r", encoding="utf-8") as file:
    data = file.read()

@app.route('/')
def index():
    return render_template('index.html',content="")

@app.route('/api/data', methods=['GET'])
def get_data():
    print("API endpoint hit")
    return data

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Flask app name:", app.name)
    app.run(debug=True, host='0.0.0.0', port=5000)
