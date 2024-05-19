import openai
import logging
import os
from dotenv import load_dotenv
import time
import logging
from datetime import datetime
from flask import jsonify

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Mapping of company names to assistant IDs
assistant_ids = {
    "Tadiran": "asst_gmdISWXu28k4tLfrXa2lKBiG",
    # Add more mappings as needed
}
threads_ids = {
    "Tadiran": "thread_sQ3KZOfoH1TKZqShKuhtMorC",
}
# Generate posts using OpenAI API
def generate_posts(company_name, num_posts, post_length):
    print(post_length)
    posts = []
    assistant_id = "asst_gmdISWXu28k4tLfrXa2lKBiG"
    thread_id = "thread_sQ3KZOfoH1TKZqShKuhtMorC"
    if not (assistant_id or thread_id):
        logging.error(f"Missing ID for the company: {company_name}")
        return ["Error: No ID found for the specified company."]

    for _ in range(num_posts):
        try:
            message = f"Generate a {post_length} LinkedIn post."
            # Creating a message in a thread
            client.beta.threads.messages.create(thread_id=thread_id, role="user", content=message)
            run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id, instructions=f"the post needs to be a {post_length} post")
            response = wait_for_run_completion(client, thread_id, run.id)
            if response.startswith("Error") or response == "No content received":
                posts.append({'error': response})
            else:
                posts.append({'content': response})
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            posts.append({'error': str(e)})

    return posts  # Return a list of post contents or errors

# Regenerate post with modifications
def regenerate_post(company_name, original_content, modifications):
    assistant_id = assistant_ids.get(company_name)
    thread_id = threads_ids.get(company_name)
    if not (assistant_id or thread_id):
        logging.error(f"Missing ID for the company: {company_name}")
        return "Error: No ID found for the specified company."
    
    message = (
        f"Here is the original LinkedIn post: {original_content}\n"
        f"Here are the modifications needed: {modifications}\n"
        "Please regenerate the post incorporating these modifications."
    )
    message = client.beta.threads.messages.create(thread_id=thread_id, role="user", content=message)
    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id, instructions=f"you need to do better")
    response = wait_for_run_completion(client=client ,thread_id= thread_id, run_id = run.id)
    return response



def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
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
