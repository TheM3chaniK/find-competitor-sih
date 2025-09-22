# LinkedIn Competitor Scraper for SIH

So, picture this: I just rocked the SIH internal hackathon and snagged 2nd place. Feeling pretty good, right? Then I start scrolling through LinkedIn and BAM! It's a flood of posts from other teams. Some are celebrating their wins, others are crying into their keyboards, and a whole bunch are just posting selfies with their certificates, leaving everyone guessing.

As a developer with a knack for web scraping, I thought, "Why not put my skills to good use?" And so, this project was born! This scraper automatically hunts down your competitors' LinkedIn posts, uses a super-smart AI to figure out if they qualified, got kicked out, or are still waiting for their results, and then neatly organizes it all for you.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/TheM3chanik/find-competitor-sih.git
    cd find-competitor-sih
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright browsers:**
    ```bash
    playwright install
    ```

## Configuration

Before you can start your detective work, you need to set up your environment variables. Create a file named `.env` in the root directory of the project and add the following variables:

```
LINKEDIN_USERNAME="your_linkedin_username"
LINKEDIN_PASSWORD="your_linkedin_password"
GROQ_API_KEY="your_groq_api_key"
SEARCH_LINK="your_linkedin_search_link"
```

-   `LINKEDIN_USERNAME`: Your LinkedIn email or phone number.
-   `LINKEDIN_PASSWORD`: Your LinkedIn password.
-   `GROQ_API_KEY`: Your API key from [Groq](https://console.groq.com/keys).
-   `SEARCH_LINK`: This is where the magic happens. To create the perfect search link, follow these steps:
    1.  Go to LinkedIn and sign in.
    2.  In the search bar, type a query that includes keywords from your problem statement, and excludes the names of your team members. This helps to filter out your own team's posts.
    3.  Here is a template for your search query:
        ```
        "sih" "keyword1 from your problem statement" "keyword2" - "your team member name 1" - "team member name 2" - "team member name 3" - "team member name 4" - "team member name 5" - "team member name 6"
        ```
        For example, if your problem statement is about a "smart irrigation system" and your team members are "John" and "Jane", your query would look like this:
        ```
        "sih" "smart irrigation system" - "John" - "Jane"
        ```
    4.  After searching, click on the "Posts" filter.
    5.  Sort the results by "Latest" to get the most recent posts.
    6.  Now, copy the URL from your browser's address bar. It will look something like this:
        ```
        https://www.linkedin.com/search/results/posts/?keywords=%22sih%22%20%22smart%20irrigation%20system%22%20-"John"%20-"Jane"&origin=GLOBAL_SEARCH_HEADER&sid=...
        ```
    7.  Paste this URL as the value for `SEARCH_LINK` in your `.env` file.

## How to Run

1.  **Run the main script:**
    ```bash
    python main.py
    ```
    This will start the scraper, which will log in to LinkedIn, navigate to the search link, scrape the posts, and then use the Groq API to predict the status of each post. The results will be saved in a file named `predictions.csv`.

2.  **Get the percentage of each category:**
    After the `predictions.csv` file is created, you can run the `get_percentage.py` script to get a summary of the results.
    ```bash
    python get_percentage.py
    ```
    This will print the total number of posts and the percentage of posts in each category (Qualified, Not Qualified, Result Not Published).

## Disclaimer

**P.S.** The bot isn't 100% correct. The predictions are based on the content of the posts and the AI model's understanding, so there might be some inaccuracies.
