from flask import Flask, request, jsonify, session, make_response
from flask_session import Session
from flask_cors import CORS
import logging
import os
import content_generation  # Import the content generation module

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("Flask_session_key")
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
# Allow CORS for all domains on all routes
CORS(app, resources={r"/generate_post": {"origins": "*"}})  # Setup CORS


def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response

# Generate Post Endpoint
@app.route('/generate_post', methods=['POST','OPTIONS'])
def generate_post():
    if request.method == 'OPTIONS':
        return _build_cors_prelight_response()
    elif request.method == 'POST':
        data = request.get_json(force=True)
    required_keys = ['objective','audience', 'topic', 'key_points', 'examples', 'structure', 'tone_style', 'engagement', 'post_examples']
    missing_keys = [key for key in required_keys if key not in data]
    if missing_keys:
        return jsonify({"error": f"Missing data for post generation: {missing_keys}"}), 400
    # Access session data safely
    topic = session.get('topic', 'Default Topic')
    trending_topic = content_generation.get_trending_topic(topic)

   # Assuming 'structure' and 'tone_style' are dictionaries stored in the session
    prompt = (
        f"Generate a LinkedIn post aimed at {session.get('audience')}, focusing on {topic} and {trending_topic}. "
        f"The objective of the post is: {session.get('objective')}. "
        f"The post should cover key points like {session.get('key_points')}. "
        f"It should start with {session.get('structure', {}).get('introduction')} and use examples such as {session.get('examples')}. "
        f"It will conclude with {session.get('structure', {}).get('conclusion')} and maintain a {session.get('tone_style', {}).get('tone')} tone and {session.get('tone_style', {}).get('style')} style. "
        f"The post should be {session.get('engagement')}. "
        f"Additionally, here are some examples from the field: {session.get('post_examples')}."
    )


    post_content = content_generation.call_openai_to_generate_post(prompt)
    print(f"Post content: {post_content}")
    return jsonify({"LinkedIn Post": post_content}), 200



@app.route('/start', methods=['GET'])
def start():
    session.clear()  # Clear previous session data
    return jsonify({"message": "What is the main goal of your LinkedIn post? Are you looking to inform, inspire, provoke thought, or network?"})

@app.route('/set_objective', methods=['POST'])
def set_objective():
    session['objective'] = request.json.get('objective')
    return jsonify({"message": "Who is the intended audience for your post? Please specify their professional background or industry."})

@app.route('/set_audience', methods=['POST'])
def set_audience():
    session['audience'] = request.json.get('audience')
    return jsonify({"message": "What topic would you like the post to cover?"})

@app.route('/set_topic', methods=['POST'])
def set_topic():
    session['topic'] = request.json.get('topic')
    return jsonify({"message": "Could you list some key points or tips that you want to include in the post?"})

@app.route('/set_key_points', methods=['POST'])
def set_key_points():
    session['key_points'] = request.json.get('key_points')
    return jsonify({"message": "Do you have any specific examples or case studies you'd like to mention in the post?"})

@app.route('/set_examples', methods=['POST'])
def set_examples():
    session['examples'] = request.json.get('examples')
    return jsonify({"message": "How would you like the post structured? Should it include an engaging introduction, a detailed body, and a thought-provoking conclusion?"})

@app.route('/set_structure', methods=['POST'])
def set_structure():
    session['structure'] = request.json.get('structure')
    return jsonify({"message": "What tone and style should the post convey? Should it be professional, authoritative, friendly, etc.?"})

@app.route('/set_tone_style', methods=['POST'])
def set_tone_style():
    session['tone_style'] = request.json.get('tone_style')
    return jsonify({"message": "Would you like to include any engagement features, such as a question for the audience or a call to action?"})

@app.route('/set_engagement', methods=['POST'])
def set_engagement():
    session['engagement'] = request.json.get('engagement')
    return jsonify({"message": "Thank you for providing the details. Can you add some examples post related to your subject ."})

@app.route('/set_post_examples', methods=['POST'])
def set_post_examples():
    example = request.json.get('post_examples')
    if not example:
        return jsonify({"error": "No example provided"}), 400
    session['post_examples'] = example
    return jsonify({"message": "Post examples added successfully. Let me prepare a draft for your LinkedIn post based on your inputs."}), 200


if __name__ == '__main__':
    app.run(debug=True)
