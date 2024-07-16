# Content Generator App

A Flask and OpenAI-based application designed to generate personalized LinkedIn posts using AI. By leveraging the power of GPT models, the app generates posts based on user preferences such as topic name, number of posts, and post length. It features an intuitive user interface for creating and editing posts.

## Features

- **Post Generation**: Dynamically generate LinkedIn posts with AI-driven suggestions.
- **User Interface**: Intuitive web interface to create and edit posts.
- **Version Management**: Store and retrieve different versions of posts.
- **CORS Support**: Configured to handle cross-origin requests, enabling seamless frontend integration.
- **Error Handling**: Comprehensive error handling for a reliable user experience.

## Prerequisites

- Python 3.12.0
- Flask
- OpenAI API
- Python-dotenv (for environment variable management)

## Installation and Setup

1. **Create an OpenAI Assistant and Obtain an Assistant ID:**

    a. Create an account on the OpenAI platform and log in.

    b. Go to the API section and create a new assistant.

    c. Note the Assistant ID provided after creation.

2. **Configure the Project:**

    a. Clone the repository:

    ```bash
    git clone https://github.com/YonathanAllouch/content_generator_app.git
    cd content_generator_app
    ```

    b. Create a `.env` file in the project root and add your API keys:

    ```env
    OPENAI_API_KEY=your-openai-api-key
    FLASK_SESSION_KEY=your-flask-session-key
    ```

    c. Modify the `content_generation.py` file to use the environment variables:

    ```python
    # content_generation.py

    assistant_ids = {
        "Topic1": "assistant_id_1",
        "Topic2": "assistant_id_2",
        "Topic3": "assistant_id_3"
        # Add more mappings as needed
    }
    
    ```

    d. Update the `interface.html` file to reflect the topics of the created assistants:

    ```html
    <div class="form-group">
        <label for="topic_name">Topic name:</label>
        <select id="topic_name" name="topic_name" required>
            <option value="Topic1">Topic1</option>
            <option value="Topic2">Topic2</option>
            <option value="Topic3">Topic3</option>
            <!-- Add more topics as needed -->
        </select>
    </div>
    ```

3. **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Flask server:**

    ```bash
    python main.py
    ```

## Usage

To generate LinkedIn posts, open your browser and go to the following address:
```bash
http://127.0.0.1:5000
```

Fill in the necessary fields and click "Submit" to generate the posts.

### Example Requests

To generate a LinkedIn post, send a POST request to `/generate_post` with the required parameters:

```json
{
  "topic_name": "Topic1",
  "num_posts": 3,
  "post_length": "medium",
  "additional_info": "Focus on AI advancements in healthcare."
}
```

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and create a pull request with your changes.

## License

MIT License

## Demo 



