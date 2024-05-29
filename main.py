from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_session import Session
from flask_cors import CORS
import logging
import os
from content_generation import generate_posts, regenerate_post

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("Flask_session_key")
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
CORS(app, resources={r"/generate_post": {"origins": "*"}})

def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response

@app.route('/generate_post', methods=['POST', 'OPTIONS'])
def generate_post():
    if request.method == 'OPTIONS':
        return _build_cors_prelight_response()
    elif request.method == 'POST':
        data = request.get_json(force=True)
        required_keys = ['company_name', 'num_posts', 'post_length','additional_info']
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            return jsonify({"error": f"Missing data for post generation: {missing_keys}"}), 400

        company_name = data['company_name']
        num_posts = int(data['num_posts'])
        post_length = data['post_length']
        additional_info = data['additional_info']

        posts, thread_id = generate_posts(company_name, num_posts, post_length, additional_info)
        logging.info(f"Posts Data: {posts}")
        return jsonify({"LinkedIn Posts": posts, "thread_id": thread_id}), 200

@app.route('/edit_post/<int:post_index>', methods=['POST'])
def edit_post(post_index):
    data = request.get_json(force=True)
    modifications = data.get('modifications')
    original_content = data.get('original_content')
    company_name = data.get('company_name')
    thread_id = data.get('thread_id')

    regenerated_post = regenerate_post(company_name, original_content, modifications, thread_id)
    return jsonify({"LinkedIn Post": regenerated_post}), 200

@app.route('/')
def serve_interface():
    return send_from_directory('static', 'interface.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
