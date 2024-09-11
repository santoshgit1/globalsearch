# result_calling.py

from Scripts.sub_navigation import SentenceAnalyzer
from Scripts.navigation import Navigation
from Scripts.data_preprocessing import DataPreprocessing

class ResultHandler:
    def __init__(self, feature, translated_text, result):
        self.feature = feature
        self.translated_text = translated_text
        self.result = result

    def handle_specific_features(self):
        travel_extractor = SentenceAnalyzer()
        self.translated_text = travel_extractor.clean_sentence(self.translated_text)

        if self.feature == "Map":
            start_location, end_location = travel_extractor.extract_travel_info(self.translated_text)
            landmarks = travel_extractor.landmarks(self.translated_text)
            self.result["start_location"] = start_location
            self.result["end_location"] = end_location
            self.result["landmarks"] = landmarks
            


        elif self.feature in ["Flight booking", "Train booking", "Bus booking"]:
            start_location, end_location = travel_extractor.extract_travel_info(self.translated_text)
            time_ranges = travel_extractor.extract_times(self.translated_text)
            start_date, end_date = travel_extractor.extract_dates(self.translated_text)
            people_count = travel_extractor.count_people(self.translated_text)
            start_time, end_time = time_ranges[0] if time_ranges else (None, None)
            self.result["start_location"] = start_location
            self.result["end_location"] = end_location 
            self.result["start_date"] = start_date
            self.result["end_date"] = end_date
            self.result["start_time"] = start_time
            self.result["people_count"] = people_count


        elif self.feature == "Hotels booking":
            start_location, end_location = travel_extractor.extract_travel_info(self.translated_text)
            time_ranges = travel_extractor.extract_times(self.translated_text)
            start_date, end_date = travel_extractor.extract_dates(self.translated_text)
            start_time, end_time = time_ranges[0] if time_ranges else (None, None)
            self.result["start_location"] = start_location
            self.result["end_location"] = end_location 
            self.result["start_time"] = start_time
            self.result["start_date"] = start_date
            self.result["end_date"] = end_date

        elif self.feature == "Create Event":
            event_name = travel_extractor.extract_event_name(self.translated_text)
            person_names = travel_extractor.extract_person_names(self.translated_text)
            guest_names = travel_extractor.extract_guest_name(self.translated_text, person_names)
            start_date, end_date = travel_extractor.extract_dates(self.translated_text)
            print(start_date, end_date)
            time_ranges = travel_extractor.extract_times(self.translated_text)
            people_count = travel_extractor.count_people(self.translated_text)
            start_date, end_date, days = travel_extractor.extract_event_duration(self.translated_text, start_date=start_date, end_date=end_date)
            start_time, end_time = time_ranges[0] if time_ranges else (None, None)
            self.result["event_name"] = event_name
            self.result["guest_name"] = guest_names
            self.result["start_date"] = start_date
            self.result["end_date"] = end_date
            self.result["start_time"] = start_time
            self.result["end_time"] = end_time
            self.result["people_count"] = people_count
            self.result["days"] = days

        elif self.feature == "Event":
            sub_events = travel_extractor.sub_events(self.translated_text)
            start_date, end_date = travel_extractor.extract_dates(self.translated_text)
            start_location, end_location = travel_extractor.extract_travel_info(self.translated_text)
            self.result["sub_events"] = sub_events
            if start_date != "":
                self.result["start_date"] = start_date
            else:
                self.result["start_date"] = end_date
            self.result["start_location"] = start_location
            self.result["end_location"] = end_location

        elif self.feature == "My Booking":
            status = travel_extractor.extract_booking_status(self.translated_text)
            self.result["Booking_status"] = status


        for key, value in self.result.items():
            if value is None:
                self.result[key] = ""
        return self.result
        


    
