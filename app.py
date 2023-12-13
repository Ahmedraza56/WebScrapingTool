import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib3

def simple_web_scraper(url, scrape_option):
    try:
        # Create a PoolManager with urllib3 to handle SSL
        http = urllib3.PoolManager()

        # Send an HTTP request
        response = http.request('GET', url)

        # Check if the request was successful (status code 200)
        if response.status == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.data, 'html.parser')
            
            # Extract information from the HTML based on user's choice
            if scrape_option == 'data':
                # Extract all text content from the page
                all_text = soup.get_text()
                
                # Prepare data for the table (split text by lines)
                table_data = [{'Data': line.strip()} for line in all_text.split('\n') if line.strip()]
                
                # Display the data in a table
                st.table(table_data)
            elif scrape_option == 'links':
                # Example: Extract all the links on the page
                links = soup.find_all('a')
                
                # Prepare data for the table
                table_data = [{'Links': link.get('href')} for link in links]
                
                # Display the data in a table
                st.table(table_data)
            else:
                st.write('Invalid scrape option. Please choose "data" or "links".')
        else:
            st.write(f'Error: {response.status}')
    
    except Exception as e:
        st.write(f'An error occurred: {e}')

# Streamlit UI
st.title("Web Scraping Tool")
website_url = st.text_input("Enter the URL to scrape:")
scrape_option = st.selectbox("Select what to scrape:", ['data', 'links'])

if st.button("Scrape"):
    simple_web_scraper(website_url, scrape_option)
