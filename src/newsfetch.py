from newsdataapi import NewsDataApiClient
import dotenv
import os
import pandas as pd  # Import pandas

# Load environment variables
dotenv.load_dotenv()

# Initialize the NewsDataAPI client
api = NewsDataApiClient(apikey=os.getenv("NewsDataAPIKey"))

# Take user input for the query
user_query = input("Enter your query: ")

# Make a request to the news API, specifying the country as 'IN' for India
response = api.news_api(q=user_query, country='IN')

# Check if the response was successful and contains articles
if response.get('status') == 'success' and response.get('totalResults', 0) > 0:
    # Create a list to hold the articles
    articles = []
    
    # Loop through the articles and extract the relevant information
    for article in response['results']:
        articles.append({
            'Title': article.get('title', 'N/A'),
            'Source': article.get('source_name', 'N/A'),
            'Published At': article.get('pubDate', 'N/A'),
            'Link': article.get('link', 'N/A')
        })

    # Create a DataFrame from the articles list
    df = pd.DataFrame(articles)

    # Display the DataFrame
    print(df)
else:
    print("No articles found or an error occurred.")
