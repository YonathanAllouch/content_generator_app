import openai
import requests
import logging
import os
from pytrends.request import TrendReq
import pandas as pd

# Initialize OpenAI client with API key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Google Trends client
pytrends = TrendReq(hl='en-US', tz=360)  # Set language and timezone

# Fetch Google Trends for a specific topic
def get_trending_topic(topic):
    try:
        pytrends.build_payload([topic], cat=0, timeframe='today 3-m', geo='', gprop='')
        related_queries = pytrends.related_queries()
        top_queries = related_queries[topic]['top']
        if top_queries and not top_queries.empty:
            return top_queries.iloc[0]['query']  # Return the top related query
        else:
            return topic  # Fallback to the original topic
    except Exception as e:
        logging.error(f"Failed to fetch trending topic for {topic}: {e}")
        return topic

# Call OpenAI to generate the LinkedIn post
def call_openai_to_generate_post(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Generate LinkedIn content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"OpenAI API call failed: {e}")
        return "Error generating post. Please try again."
