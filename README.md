# AI News Blog

This project is an automated AI blog that generates a daily summary of the top 10 AI news events. It is designed to be hosted on GitHub Pages.

## How it works

- A GitHub Actions workflow runs every day at midnight UTC.
- The workflow executes a Python script (`main.py`) that fetches the latest AI news from [Event Registry](https://eventregistry.org/).
- The script generates a new blog post in Markdown format with the top 10 news items.
- The new post is then automatically committed to the repository, which triggers a rebuild of the GitHub Pages site.

## Setup

To get this project running in your own repository, you need to do the following:

1.  **Get an Event Registry API Key**:
    - Go to [Event Registry](https://eventregistry.org/register) and register for a free API key.

2.  **Add the API Key as a GitHub Secret**:
    - In your GitHub repository, go to `Settings` > `Secrets and variables` > `Actions`.
    - Click on `New repository secret`.
    - Name the secret `EVENT_REGISTRY_API_KEY`.
    - Paste your API key as the value.

3.  **Implement the Summarization Logic**:
    - The `main.py` script comes with placeholder functions for summarizing the news articles (`get_one_sentence_summary` and `get_detailed_summary`).
    - You need to replace the placeholder logic with actual calls to a Large Language Model (LLM) of your choice (e.g., GPT, Claude, etc.).
    - You will likely need another API key for the LLM service, which you should also add as a GitHub secret and access in the `main.py` script.

## Running the blog

Once you have completed the setup, the blog will update automatically every day. You can also trigger a manual update by going to the `Actions` tab in your repository, selecting the `Daily AI News Update` workflow, and clicking `Run workflow`.