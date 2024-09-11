# # main.py
# from Scripts.data_ingestion import DataIngestion
# from Scripts.data_preprocessing import DataPreprocessing

# def main():
#     # api_url = 'https://api.example.com/endpoint'  # Replace with your API URL
#     # ingestion = DataIngestion(api_url)
#     # params = {'key': 'value'}  # Replace with any query parameters your API requires
#     # text_data = ingestion.get_text(params)

#     # if text_data:
#     #     preprocessing = DataPreprocessing(text_data)
#     #     preprocessing.pre_process()
#     # else:
#     #     print("Failed to fetch text data.")

#     # text_data = "Mumbai se Delhi ki sbhi flights dikhao"
#     text_data = "मुझे दिल्ली जाना है"

#     preprocessing = DataPreprocessing(text_data)  # Create an instance
#     translated_text = preprocessing.pre_process()  # Call the method on the instance
#     print("Processed Text:", translated_text)

# if __name__ == "__main__":
#     main()



# # main.py
# import json
# from Scripts.data_ingestion import DataIngestion
# from Scripts.data_preprocessing import DataPreprocessing
# from Scripts.navigation import Navigation  # Import the Navigation class
# # from Scripts.sub_navigation import SentenceAnalyzer  # Import TravelInfoExtractor
# from Scripts.result_calling import ResultHandler


# class Main:
#     def __init__(self, api_url=None, params=None, text_data=None):
#         """
#         Initialize the Main class with API URL, parameters, or text data.

#         Args:
#             api_url (str): URL for data ingestion, optional.
#             params (dict): Parameters for data ingestion, optional.
#             text_data (str): Text data for preprocessing, optional.
#         """
#         self.api_url = api_url
#         self.params = params
#         self.text_data = text_data

#     def fetch_text_data(self):
#         """
#         Fetch text data from API if API URL and parameters are provided.
#         """
#         if self.api_url and self.params:
#             ingestion = DataIngestion(self.api_url)
#             return ingestion.get_text(self.params)
#         else:
#             return None

#     def process_text_data(self):
#         """
#         Process the text data through preprocessing and feature extraction.
#         """
#         result = {"status": 1, "feature": "", "translated_text": "", "sub_events":"", "Booking_status": "", "start_location": "", "end_location": "", "landmarks": "", "time": "", "start_time": "", "end_time": "", "people_count": "", "start_date": "", "end_date": "", "person_names": "", "event_name": "", "guest_name": "", "days": "", "time_period": ""}
#         if self.text_data:
#             preprocessing = DataPreprocessing(self.text_data)  # Create an instance
#             translated_text = preprocessing.pre_process()  # Call the method on the instance
#             print("Processed Text:", translated_text)

#             # Perform feature extraction
#             navigation = Navigation()  # Create an instance of Navigation
#             feature = navigation.find_feature_with_max_match(translated_text)
#             if feature is not False:
#                 print("Identified Feature:", feature)

#                 result["status"] = 1
#                 result["feature"] = feature
#                 result["translated_text"] = translated_text

#                 result_call = ResultHandler(feature, translated_text, result)
#                 result = result_call.handle_specific_features()

#                 return result 

#             else:
#                 # result = {"status": 0, "feature": None, "translated_text": "Sorry i don't know that..."}
#                 result["status"] = 0
#                 result["feature"] = ""
#                 result["translated_text"] = "Sorry i don't know that..."
#                 # return result

#         else:
#             print("No text data to process.")
#             # result = {"status": 0, "feature": None, "translated_text": "Sorry! please come again..."}
#             result["status"] = 0
#             result["feature"] = ""
#             result["translated_text"] = "Sorry! please come again..."
#             # return result
#         return result

# def main():
#     # Example usage
#     api_url = 'https://api.example.com/endpoint'  # Replace with your API URL
#     params = {'key': 'value'}  # Replace with any query parameters your API requires

#     # Initialize Main with API URL and parameters
#     main_instance = Main(api_url=api_url, params=params)
#     text_data = main_instance.fetch_text_data()

#     if text_data:
#         # Initialize Main with fetched text data
#         main_instance = Main(text_data=text_data)
#         result = main_instance.process_text_data()
#     else:
#         # For testing with hardcoded text data
#         # text_data = "I want to travel to Kumbh from Pune"
#         # text_data = "What is the weather today"
#         text_data = ""
#         main_instance = Main(text_data=text_data)
#         result = main_instance.process_text_data()

#     # Save the result to a JSON file
#     with open('output.json', 'w', encoding='utf-8') as json_file:
#         json.dump(result, json_file, ensure_ascii=False, indent=4)
#         print("Output saved to output.json")

# if __name__ == "__main__":
#     main()
    
















import json
import logging
import os
from Scripts.data_ingestion import DataIngestion
from Scripts.data_preprocessing import DataPreprocessing
from Scripts.navigation import Navigation
from Scripts.result_calling import ResultHandler
from Scripts.global_history import StoreData

# Ensure the log directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging for main.py
logging.basicConfig(
    filename='logs/main.log',  # Log file path
    level=logging.INFO,        # Log level (INFO, DEBUG, ERROR, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Main:
    def __init__(self, api_url=None, params=None, text_data=None):
        self.api_url = api_url
        self.params = params
        self.text_data = text_data
        logging.info(f"Initialized Main with text data: {self.text_data}")

    def fetch_text_data(self):
        if self.api_url and self.params:
            logging.info(f"Fetching text data from API: {self.api_url} with params: {self.params}")
            ingestion = DataIngestion(self.api_url)
            return ingestion.get_text(self.params)
        else:
            logging.warning("No API URL or parameters provided.")
            return None

    def process_text_data(self):
        # # storing in the database
        # logging.info("Storing to Database history")
        # store_instance = StoreData(self.text_data)
        # store_instance.execute()
        # logging.info("Stored to Database history successfully")

        logging.info("Started processing text data.")
        result = {
            "status": 1, "feature": "", "translated_text": "", "sub_events": "", "Booking_status": "", 
            "start_location": "", "end_location": "", "landmarks": "", "time": "", "start_time": "", 
            "end_time": "", "people_count": "", "start_date": "", "end_date": "", "person_names": "", 
            "event_name": "", "guest_name": "", "days": "", "time_period": ""
        }

        if self.text_data:
            try:
                preprocessing = DataPreprocessing(self.text_data)
                translated_text = preprocessing.pre_process()
                logging.info(f"Preprocessed text: {translated_text}")

                navigation = Navigation()
                feature = navigation.find_feature_with_max_match(translated_text)

                if feature is not False:
                    logging.info(f"Identified feature: {feature}")
                    result["status"] = 1
                    result["feature"] = feature
                    result["translated_text"] = translated_text

                    result_call = ResultHandler(feature, translated_text, result)
                    result = result_call.handle_specific_features()

                    logging.info(f"Final result after handling features: {result}")
                    return result
                else:
                    logging.warning("Feature identification failed.")
                    result["status"] = 0
                    result["translated_text"] = "Sorry, I don't know that..."
            except Exception as e:
                logging.error(f"Error during processing: {e}")
                result["status"] = 0
                result["translated_text"] = "An error occurred."
        else:
            logging.warning("No text data provided for processing.")
            result["status"] = 0
            result["translated_text"] = "Sorry! Please come again..."

        return result

def main():
    # Example usage
    api_url = 'https://api.example.com/endpoint'
    params = {'key': 'value'}

    main_instance = Main(api_url=api_url, params=params)
    text_data = main_instance.fetch_text_data()

    if text_data:
        # search_term = result.get("translated_text", "")
        # storing in Database history
        logging.info("Storing to Database history")
        store_instance = StoreData(text_data)
        store_instance.execute()
        logging.info("Stored to Database history successfully")

        main_instance = Main(text_data=text_data)
        result = main_instance.process_text_data()
    else:
        text_data = "Example text"
        main_instance = Main(text_data=text_data)
        result = main_instance.process_text_data()

    # Save the result to a JSON file
    with open('output.json', 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)
        logging.info("Output saved to output.json")

if __name__ == "__main__":
    main()
