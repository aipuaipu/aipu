# AI News Blog

This project is an automated AI blog that generates a daily summary of the top 10 AI news events using Google's Gemini API. It is designed to be hosted on GitHub Pages.

## How it works

- A GitHub Actions workflow runs every day at midnight UTC.
- The workflow executes a Python script (`main.py`) that:
  1. Fetches the latest AI news from [Event Registry](https://eventregistry.org/).
  2. Uses the [Google Gemini API](https://ai.google.dev/) to generate a one-sentence summary and a detailed summary for each of the top 10 articles.
- The script generates a new blog post in Markdown format with the summarized news.
- The new post is then automatically committed to the repository, which triggers a rebuild of the GitHub Pages site.

## Setup

To get this project running, you need to configure two API keys as GitHub Secrets.

### **IMPORTANT: API Key Security**
Never hard-code your API keys in the source code. Use GitHub Secrets to store them securely. If you have accidentally exposed a key, revoke it immediately and generate a new one.

### 1. Event Registry API Key (for fetching news)
- **Get the key**: Go to [Event Registry](https://eventregistry.org/register) and register for a free API key.
- **Create the secret**:
  - In your GitHub repository, go to `Settings` > `Secrets and variables` > `Actions`.
  - Click `New repository secret`.
  - Name: `EVENT_REGISTRY_API_KEY`
  - Value: Paste your API key here.

### 2. Google Gemini API Key (for summarization)
- **Get the key**: Go to the [Google AI for Developers](https://makersuite.google.com/app/apikey) page to generate your API key.
- **Create the secret**:
  - In your GitHub repository, go to `Settings` > `Secrets and variables` > `Actions`.
  - Click `New repository secret`.
  - Name: `GEMINI_API_KEY`
  - Value: Paste your API key here.

## Running the blog

Once you have completed the setup, the blog will update automatically every day. You can also trigger a manual update by going to the `Actions` tab in your repository, selecting the `Daily AI News Update` workflow, and clicking `Run workflow`.