import openai
import logging
import os
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Mapping of company names to assistant IDs
assistant_ids = {
    "Tadiran": "asst_gmdISWXu28k4tLfrXa2lKBiG",
    # Add more mappings as needed
}

# Generate posts using OpenAI API
def generate_posts(company_name, num_posts, post_length):
    posts = []
    assistant_id = assistant_ids.get(company_name)

    if not assistant_id:
        logging.error(f"Missing assistant ID for the company: {company_name}")
        return ["Error: No assistant ID found for the specified company."]

    logging.info(f"Generating {num_posts} {post_length} post(s) for company: {company_name}")

    # Create a new thread
    thread = client.beta.threads.create()
    thread_id = thread.id
    logging.info(f"Created thread with ID: {thread_id}")

    for _ in range(num_posts):
        try:
            message = f"Generate a {post_length} LinkedIn post."
            logging.info(f"Sending message: {message}")
            # Creating a message in the thread
            client.beta.threads.messages.create(thread_id=thread_id, role="user", content=message)

            if post_length == "short":
                instructions = "Please generate a short LinkedIn post. The post should be between 200 to 500 characters. Only provide the post content without any additional comments or context."
            else:
                instructions = "Please generate a long LinkedIn post. The post should be between 800 to 1500 characters. Only provide the post content without any additional comments or context."

            run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id,
                instructions=instructions
            )
            response = wait_for_run_completion(client, thread_id, run.id)
            if response.startswith("Error") or response == "No content received":
                posts.append({'error': response})
            else:
                posts.append({'content': response})
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            posts.append({'error': str(e)})

    return posts, thread_id  # Return a list of post contents or errors and the thread ID

# Regenerate post with modifications
def regenerate_post(company_name, original_content, modifications, thread_id):
    assistant_id = assistant_ids.get(company_name)
    if not assistant_id or not thread_id:
        logging.error(f"Missing ID for the company: {company_name} or thread ID")
        return "Error: No ID found for the specified company or thread."

    message = (
        f"Here is the original LinkedIn post: {original_content}\n"
        f"Here are the modifications needed: {modifications}\n"
        "Please regenerate the post incorporating these modifications."
    )
    client.beta.threads.messages.create(thread_id=thread_id, role="user", content=message)
    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id, instructions=modifications)
    response = wait_for_run_completion(client, thread_id, run.id)
    return response

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
                logging.info(f"Run completed in {formatted_elapsed_time}")
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                for message in reversed(messages.data):
                    if message.role == 'assistant' and message.content:
                        return message.content[0].text.value
                return "No content received"
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)
