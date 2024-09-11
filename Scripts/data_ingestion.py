
import requests

class DataIngestion:
    def __init__(self, api_url):
        """
        Initialize the DataIngestion with the API URL.

        Args:
            api_url (str): The URL of the API endpoint.
        """
        self.api_url = api_url

    def get_text(self, params=None):
        """
        Get text data from the API.

        Args:
            params (dict, optional): Dictionary of query parameters to send with the request.

        Returns:
            str: The text data fetched from the API, or None if an error occurs.
        """
        try:
            # Make a GET request to the API
            response = requests.get(self.api_url, params=params)
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Return the text content from the response
            return response.text
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None
