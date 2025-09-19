import os
from eventregistry import *
from datetime import date, timedelta

# --- Configuration ---
# TODO: Add your EVENT_REGISTRY_API_KEY as a secret in your GitHub repository
EVENT_REGISTRY_API_KEY = os.environ.get("EVENT_REGISTRY_API_KEY", "YOUR_API_KEY_HERE")

# --- Placeholder for Summarization Logic ---
def get_one_sentence_summary(text):
    """
    Placeholder for one-sentence summarization logic.
    This should be replaced with a call to an actual LLM.
    """
    return "This is a one-sentence summary of the news event."

def get_detailed_summary(text):
    """
    Placeholder for detailed summarization logic (100-1000 words).
    This should be replaced with a call to an actual LLM.
    """
    return "This is a detailed summary of the news event, providing the full story."

# --- Main Logic ---
def get_ai_news():
    """
    Fetches the top 10 AI news from the last 24 hours.
    """
    er = EventRegistry(apiKey=EVENT_REGISTRY_API_KEY)

    # Get yesterday's date
    yesterday = date.today() - timedelta(1)

    # Query for AI-related articles
    q = QueryArticlesIter(
        keywords=QueryItems.OR(["Artificial Intelligence", "Machine Learning", "Deep Learning", "LLM"]),
        lang="eng",
        dateStart=yesterday,
        dateEnd=yesterday
    )

    # Fetch articles and sort by social media score
    articles = []
    for art in q.execQuery(er, sortBy="socialScore", maxItems=10):
        articles.append(art)

    return articles

def generate_blog_post(articles):
    """
    Generates a Markdown blog post from the list of articles.
    """
    today_str = date.today().strftime("%Y-%m-%d")
    post_filename = f"_posts/{today_str}-top-10-ai-news.md"

    with open(post_filename, "w") as f:
        f.write("---\n")
        f.write(f"title: Top 10 AI News for {today_str}\n")
        f.write(f"date: {today_str}\n")
        f.write("layout: post\n")
        f.write("---\n\n")

        for i, article in enumerate(articles):
            f.write(f"## {i+1}. {article['title']}\n\n")

            # 1. One-sentence summary
            one_sentence_summary = get_one_sentence_summary(article['body'])
            f.write(f"**{one_sentence_summary}**\n\n")

            # 2. Detailed summary
            detailed_summary = get_detailed_summary(article['body'])
            f.write(f"{detailed_summary}\n\n")

            # Add a link to the original article
            f.write(f"[Read the full article]({article['url']})\n\n")
            f.write("---\n")

    print(f"Blog post generated: {post_filename}")

if __name__ == "__main__":
    if EVENT_REGISTRY_API_KEY == "YOUR_API_KEY_HERE":
        print("Please set the EVENT_REGISTRY_API_KEY environment variable.")
    else:
        top_10_articles = get_ai_news()
        if top_10_articles:
            generate_blog_post(top_10_articles)
        else:
            print("No articles found for the given criteria.")
