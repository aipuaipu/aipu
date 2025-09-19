import os
import google.generativeai as genai
from eventregistry import *
from datetime import date, timedelta

# --- Configuration ---
EVENT_REGISTRY_API_KEY = os.environ.get("EVENT_REGISTRY_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Configure the Gemini API
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# --- Summarization Logic using Gemini ---
def get_summary(text, prompt):
    """
    Generic function to get a summary from the Gemini API.
    """
    if not GEMINI_API_KEY:
        return "Error: Gemini API key is not configured."

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt + "\n\n" + text,
                                          generation_config=genai.types.GenerationConfig(
                                              # Only one candidate for now.
                                              candidate_count=1,
                                              # The Gemini models can be too creative for this task
                                              temperature=0.3,
                                          ))
        return response.text
    except Exception as e:
        return f"Error during summarization: {e}"

def get_one_sentence_summary(text):
    """
    Generates a one-sentence summary of the news event.
    """
    prompt = "Summarize the following news article in a single, concise sentence:"
    return get_summary(text, prompt)

def get_detailed_summary(text):
    """
    Generates a detailed summary of the news event (100-1000 words).
    """
    prompt = "Provide a detailed summary of the following news article, explaining the event from start to finish. The summary should be between 100 and 1000 words."
    return get_summary(text, prompt)

# --- Main Logic ---
def get_ai_news():
    """
    Fetches the top 10 AI news from the last 24 hours.
    """
    er = EventRegistry(apiKey=EVENT_REGISTRY_API_KEY)
    yesterday = date.today() - timedelta(1)

    q = QueryArticlesIter(
        keywords=QueryItems.OR(["Artificial Intelligence", "Machine Learning", "Deep Learning", "LLM", "AGI"]),
        lang="eng",
        dateStart=yesterday,
        dateEnd=yesterday
    )

    articles = []
    for art in q.execQuery(er, sortBy="socialScore", maxItems=10):
        # We need the article body for summarization
        if art.get('body'):
            articles.append(art)

    return articles

def generate_blog_post(articles):
    """
    Generates a Markdown blog post from the list of articles.
    """
    today_str = date.today().strftime("%Y-%m-%d")
    post_filename = f"_posts/{today_str}-top-10-ai-news.md"

    with open(post_filename, "w", encoding='utf-8') as f:
        f.write("---\n")
        f.write(f"title: Top 10 AI News for {today_str}\n")
        f.write(f"date: {today_str}\n")
        f.write("layout: post\n")
        f.write("---\n\n")

        for i, article in enumerate(articles):
            title = article.get('title', 'No Title')
            body = article.get('body', '')
            url = article.get('url', '#')

            f.write(f"## {i+1}. {title}\n\n")

            # 1. One-sentence summary
            one_sentence_summary = get_one_sentence_summary(body)
            f.write(f"**{one_sentence_summary}**\n\n")

            # 2. Detailed summary
            detailed_summary = get_detailed_summary(body)
            f.write(f"{detailed_summary}\n\n")

            f.write(f"[Read the full article]({url})\n\n")
            f.write("---\n")

    print(f"Blog post generated: {post_filename}")

if __name__ == "__main__":
    if not EVENT_REGISTRY_API_KEY or not GEMINI_API_KEY:
        print("Error: Please set both EVENT_REGISTRY_API_KEY and GEMINI_API_KEY environment variables.")
    else:
        top_10_articles = get_ai_news()
        if top_10_articles:
            generate_blog_post(top_10_articles)
        else:
            print("No articles found for the given criteria.")
