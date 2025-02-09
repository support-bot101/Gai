import os

# Uninstall and reinstall googlesearch-python
os.system("pip uninstall -y googlesearch-python")
os.system("pip install --upgrade googlesearch-python")

# Now import required libraries
import random
import re
import requests
from googlesearch import search
from bs4 import BeautifulSoup

# Function to fetch code snippets
def fetch_code_snippet(query):
    search_query = f"{query} site:stackoverflow.com OR site:github.com OR site:geeksforgeeks.org OR site:w3schools.com"
    
    try:
        results = search(search_query, num_results=5)
        for url in results:
            try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")

                # Skip cookie banners
                if any(word in soup.text.lower() for word in ["accept cookies", "cookies", "subscribe", "sign-up", "free trial"]):
                    continue  

                # Extract code snippets
                code_blocks = soup.find_all("code")
                for code in code_blocks:
                    code_text = clean_text(code.get_text())
                    if len(code_text.split()) > 5:
                        return f"Here's a possible solution from {url}:\n\n```{code_text}```"
            except Exception:
                continue

    except Exception:
        return "I couldn't find an exact code snippet, but I can help guide you!"

    return "I searched but didn't find an exact match. Try rephrasing!"

# Function to clean up scraped text
def clean_text(text):
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    text = re.sub(r"\[.*?\]", "", text)  # Remove citation references like [1], [2]
    return text.strip()

# Function to fetch Reddit answers while avoiding login-required pages
def fetch_reddit_response(query):
    search_query = f"{query} site:reddit.com"
    
    try:
        results = search(search_query, num_results=5)
        for url in results:
            try:
                response = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
                soup = BeautifulSoup(response.text, "html.parser")

                # Avoid cookie banners
                if any(word in soup.text.lower() for word in ["accept cookies", "sign-up", "free trial", "subscribe", "log in"]):
                    continue  

                # Extract relevant text (from comments)
                comments = soup.find_all("p")
                for comment in comments:
                    text = clean_text(comment.get_text())
                    if len(text.split()) > 10:  # Avoid short/unrelated results
                        return f"Here's a Reddit response from {url}:\n\n{text}"
            except Exception:
                continue

    except Exception:
        return "I couldn't find any relevant Reddit posts."

    return "I searched Reddit but didn't find a perfect answer. Try rephrasing!"

# Function to fetch general answers from Google
def fetch_google_response(query):
    try:
        results = search(query, num_results=5)
        for url in results:
            try:
                response = requests.get(url, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")

                # Avoid cookie banners
                if any(word in soup.text.lower() for word in ["accept cookies", "subscribe", "sign-up", "cookies"]):
                    continue  

                # Extract useful content
                paragraphs = soup.find_all("p")
                for p in paragraphs:
                    text = clean_text(p.get_text())
                    if len(text.split()) > 10 and "subscribe" not in text.lower():
                        return text
            except Exception:
                continue

    except Exception:
        return "I couldn't find an exact answer, but I can help figure it out!"

    return "I searched but didn't find a perfect match. Try rephrasing!"

# Function to generate responses
def generate_response(user_input):
    if re.search(r"\b(hi|hello|hey)\b", user_input, re.IGNORECASE):
        return random.choice(["Hey there!", "Hello! How can I assist you today?", "Hi! Need help with something?"])
    elif re.search(r"\b(how are you)\b", user_input, re.IGNORECASE):
        return "I'm just a chatbot, but I'm here to help! How about you?"
    elif re.search(r"\b(who are you|what is your name)\b", user_input, re.IGNORECASE):
        return "I'm Google AI, your chatbot assistant!"
    elif re.search(r"\b(exit|quit|bye)\b", user_input, re.IGNORECASE):
        return "Goodbye! Have a great day!"
    
    # Check for coding-related questions
    if re.search(r"\b(code|example|script|program|how to)\b", user_input, re.IGNORECASE):
        return fetch_code_snippet(user_input)
    
    # Check if the user specifically wants Reddit results
    if "reddit" in user_input.lower():
        return fetch_reddit_response(user_input)

    # Otherwise, fetch general Google results
    return fetch_google_response(user_input)

# Expose the function as `input`
def input(user_query):
    return generate_response(user_query)
