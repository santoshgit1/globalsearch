
# import spacy
# import re

# class SentenceAnalyzer:
#     def __init__(self):
#         self.nlp = spacy.load("en_core_web_sm")
#         self.manual_locations = ['Kumbh', 'maha kumbh', 'Prayagraj']

#     def extract_locations(self, text):
#         doc = self.nlp(text)
#         extracted_locations = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]

#         # Add only those manual locations that are mentioned in the text
#         for location in self.manual_locations:
#             if location.lower() in text.lower():
#                 extracted_locations.append(location)

#         return extracted_locations

#     def find_starting_location(self, text, locations):
#         # Define a regex pattern to capture the starting location
#         pattern = re.compile(r'\bfrom\b\s+([A-Za-z\s]+?)(?:\s+to\s+|$)')
#         match = pattern.search(text)
#         if match:
#             start_location = match.group(1).strip()
#             # Ensure the starting location is in the list of extracted locations
#             if start_location in locations:
#                 return start_location
#         return None

#     def extract_travel_info(self, text):
#         locations = self.extract_locations(text)
#         start_location = self.find_starting_location(text, locations)

#         if not start_location:
#             start_location = "current location"

#         if start_location in locations:
#             # Remove the starting location from the list to find the ending location
#             locations.remove(start_location)

#         end_location = locations[0] if locations else None

#         return start_location, end_location
















# import spacy
# import re
# from datetime import datetime, timedelta

# class SentenceAnalyzer:
#     def __init__(self):
#         self.nlp = spacy.load("en_core_web_sm")
#         self.manual_locations = ['Kumbh', 'maha kumbh', 'Prayagraj']
#         # Regular expression pattern to match time expressions
#         self.time_pattern = r"(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm)|(?:twelve|one|two|three|four|five|six|seven|eight|nine|ten|eleven)\s*(?:AM|PM|am|pm))"

#         # Regular expression pattern to match date expressions
#         self.date_patterns = [
#             r'\b(\d{2}/\d{2}/\d{4})\b',  # DD/MM/YYYY
#             r'\b(\d{2}-\d{2}-\d{4})\b',  # DD-MM-YYYY
#             r'\b(\d{4}/\d{2}/\d{2})\b',  # YYYY/MM/DD
#             r'\b(\d{4}-\d{2}-\d{2})\b',  # YYYY-MM-DD
#             r'\b(\w+ \d{1,2}(?:st|nd|rd|th)?,? \d{4})\b',  # Month DD, YYYY or Month DDth, YYYY
#             r'\b(\d{1,2}(?:st|nd|rd|th)? \w+,? \d{4})\b',  # DD Month YYYY or DDth Month YYYY
#             r'\b(\w+ \d{1,2}(?:st|nd|rd|th)?)\b'  # Month DD or Month DDth (assumes current year)
#         ]

#         # Dictionary to map phrases to specific times
#         self.phrase_time_mapping = {
#             "late night": ("11:00 PM", None),
#             "early morning": ("5:00 AM", None),
#             "morning": ("9:00 AM", None),
#             "afternoon": ("12:00 PM", None),
#             "evening": ("6:00 PM", None),
#             "night": ("8:00 PM", None)
#         }

#     def extract_locations(self, text):
#         doc = self.nlp(text)
#         extracted_locations = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]

#         # Add only those manual locations that are mentioned in the text
#         for location in self.manual_locations:
#             if location.lower() in text.lower():
#                 extracted_locations.append(location)

#         return extracted_locations

#     def find_starting_location(self, text, locations):
#         # Define a regex pattern to capture the starting location
#         pattern = re.compile(r'\bfrom\b\s+([A-Za-z\s]+?)(?:\s+to\s+|$)')
#         match = pattern.search(text)
#         if match:
#             start_location = match.group(1).strip()
#             # Ensure the starting location is in the list of extracted locations
#             if start_location in locations:
#                 return start_location
#         return None

#     def extract_travel_info(self, text):
#         locations = self.extract_locations(text)
#         start_location = self.find_starting_location(text, locations)

#         if not start_location:
#             start_location = "current location"

#         if start_location in locations:
#             # Remove the starting location from the list to find the ending location
#             locations.remove(start_location)

#         end_location = locations[0] if locations else None

#         return start_location, end_location
    

#     # Function to convert time string to standardized format
#     def standardize_time(self, time_str):
#         if not time_str:
#             return None

#         # Convert word numbers to digits
#         word_to_num = {
#             'twelve': '12', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
#             'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
#             'ten': '10', 'eleven': '11'
#         }
#         for word, num in word_to_num.items():
#             time_str = time_str.replace(word, num)

#         # Try parsing with various formats
#         for fmt in ['%I:%M %p', '%I %p', '%I%p']:
#             try:
#                 return datetime.strptime(time_str.upper(), fmt).strftime('%I:%M %p')
#             except ValueError:
#                 pass
#         return None

#     # Function to extract dates from a sentence
#     def extract_dates(self, sentence):
#         dates = []
#         today = datetime.now().date()

#         if "day after tomorrow" in sentence.lower():
#             return [(today + timedelta(days=2)).strftime('%Y-%m-%d')]

#         after_days_match = re.search(r'(\w+|\d+) days?', sentence.lower())
#         if after_days_match:
#             days_text = after_days_match.group(1)
#             if days_text.isdigit():
#                 days = int(days_text)
#             else:
#                 text_to_num = {
#                     'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
#                     'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
#                 }
#                 days = text_to_num.get(days_text, 0)
#             if days > 0:
#                 return [(today + timedelta(days=days)).strftime('%Y-%m-%d')]

#         for pattern in self.date_patterns:
#             matches = re.findall(pattern, sentence)
#             for match in matches:
#                 try:
#                     for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%Y-%m-%d', '%B %d, %Y', '%B %d %Y', '%d %B %Y', '%B %d', '%d %B']:
#                         try:
#                             parsed_date = datetime.strptime(match, fmt)
#                             if fmt in ['%B %d', '%d %B']:
#                                 parsed_date = parsed_date.replace(year=today.year)
#                             formatted_date = parsed_date.strftime('%Y-%m-%d')
#                             dates.append(formatted_date)
#                             break
#                         except ValueError:
#                             continue
#                 except ValueError:
#                     continue

#         relative_date_keywords = {
#             "today": 0,
#             "tomorrow": 1,
#             "yesterday": -1,
#         }

#         for keyword, offset in relative_date_keywords.items():
#             if keyword in sentence.lower():
#                 relative_date = (today + timedelta(days=offset)).strftime('%Y-%m-%d')
#                 dates.append(relative_date)

#         unique_dates = list(set(dates))
#         return unique_dates if unique_dates else None

#     # Function to extract start and end times from a sentence
#     def extract_times(self, sentence):
#         times = []

#         # First, check for specific time mentions
#         specific_time_pattern = r'(\d{1,2})(?:\s*:\s*\d{2})?\s*(in the|at)\s*(morning|afternoon|evening|night)'
#         specific_time_match = re.search(specific_time_pattern, sentence, re.IGNORECASE)
#         if specific_time_match:
#             hour = int(specific_time_match.group(1))
#             period = specific_time_match.group(3).lower()
#             if period == 'morning' and hour < 12:
#                 return [(f"{hour:02d}:00 AM", None)]
#             elif period in ['afternoon', 'evening', 'night'] or (period == 'morning' and hour == 12):
#                 return [(f"{hour:02d}:00 PM", None)]

#         time_range_pattern = r'from\s+(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm))\s+to\s+(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm))'
#         time_range_match = re.search(time_range_pattern, sentence, re.IGNORECASE)

#         if time_range_match:
#             start_time = self.standardize_time(time_range_match.group(1))
#             end_time = self.standardize_time(time_range_match.group(2))
#             if start_time and end_time:
#                 return [(start_time, end_time)]

#         # Apply regex to find time expressions
#         matches = re.findall(self.time_pattern, sentence, re.IGNORECASE)
#         matches = [self.standardize_time(match) for match in matches if self.standardize_time(match)]

#         # Handle phrases like "early morning"
#         for phrase, (start_time, end_time) in self.phrase_time_mapping.items():
#             if phrase in sentence.lower():
#                 times.append((start_time, end_time))

#         # Handle explicit end times
#         lower_sentence = sentence.lower()

#         end_keywords = ['end', 'finish', 'until', 'to']
#         end_time = None
#         for keyword in end_keywords:
#             if keyword in lower_sentence:
#                 end_index = lower_sentence.index(keyword)
#                 end_time_matches = re.findall(self.time_pattern, sentence[end_index:], re.IGNORECASE)
#                 if end_time_matches:
#                     end_time = self.standardize_time(end_time_matches[0])
#                     break

#         start_keywords = ['start', 'begin', 'from', 'commence', 'at']
#         start_time = None

#         for keyword in start_keywords:
#             if keyword in lower_sentence:
#                 start_index = lower_sentence.index(keyword)
#                 start_time_matches = re.findall(self.time_pattern, sentence[start_index:], re.IGNORECASE)
#                 if start_time_matches:
#                     start_time = self.standardize_time(start_time_matches[0])
#                     break

#         # If we have both start and end times, or just one of them
#         if start_time or end_time:
#             times.append((start_time, end_time))

#         # If no specific start/end times found, fall back to any times detected
#         if not times and matches:
#             if len(matches) >= 2:
#                 times.append((matches[0], matches[1]))
#             else:
#                 times.append((matches[0], None))

#         return times if times else [(None, None)]

#     # Function to count the number of people in a sentence
#     def count_people(self, sentence):
#         doc = self.nlp(sentence)

#         # Count people based on named entities
#         named_people_count = sum(1 for ent in doc.ents if ent.label_ == "PERSON")

#         # Count personal pronouns and family relations
#         personal_pronouns = ["i", "me", "you"]
#         family_relations = ["brother", "sister", "mother", "father", "parent", "child", "son", "daughter", "sibling", "cousin", "aunt", "uncle", "grandparent", "grandfather", "grandmother"]
#         other_person_indicators = ["friend", "colleague", "coworker"]

#         pronoun_count = sum(1 for token in doc if token.text.lower() in personal_pronouns)
#         family_count = sum(1 for token in doc if token.text.lower() in family_relations)
#         other_count = sum(1 for token in doc if token.text.lower() in other_person_indicators)

#         # Handle cases where people are mentioned by numbers (e.g., "two people")
#         numeric_people_count = 0
#         text_to_num = {
#             "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
#             "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
#             "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
#             "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
#             "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30,
#             "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80,
#             "ninety": 90, "hundred": 100, "thousand": 1000
#         }

#         # Search for numeric values and associated "people" or "colleagues" in the sentence
#         tokens = sentence.lower().split()
#         for i, token in enumerate(tokens):
#             if token.isdigit() or token in text_to_num:
#                 if i + 1 < len(tokens) and tokens[i + 1] in ["people", "person", "colleagues"]:
#                     numeric_people_count = int(token) if token.isdigit() else text_to_num[token]
#                     return numeric_people_count  # Return immediately if we find a specific number of people

#         # If no specific number is found, calculate total as before
#         total_people_count = named_people_count + pronoun_count + family_count + other_count

#         # Return None if the total count is zero
#         return None if total_people_count == 0 else total_people_count

#     # Function to extract name of people in a sentence
#     def extract_person_names(self, sentence):
#         doc = self.nlp(sentence)
#         person_names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
#         Name = list(set(person_names))
#         return Name if Name else None

#     # Function to extract event name in a sentence
#     def extract_event_name(self, sentence):
#         # List of common event-indicating words
#         event_indicators = ["event", "meeting", "conference", "ceremony", "celebration", "party", "concert", "festival", "show", "seminar", "workshop"]
#         # Words that should not be considered as event names on their own
#         non_event_words = ["tomorrow", "today", "yesterday", "next", "last", "this", "that", "the", "a", "an"]
#         # First, check for quoted event names
#         quoted_name_match = re.search(r"['\"](.*?)['\"]", sentence)
#         if quoted_name_match:
#             return quoted_name_match.group(1)

#         # Use SpaCy to analyze the sentence
#         doc = self.nlp(sentence)

#         for token in doc:
#             if token.text.lower() in event_indicators:
#                 # Look for event name to the left of the indicator
#                 left_tokens = []
#                 for left_token in reversed(list(token.lefts)):
#                     if left_token.pos_ in ["PROPN", "NOUN", "ADJ"] and left_token.text.lower() not in non_event_words:
#                         left_tokens.insert(0, left_token.text)
#                     else:
#                         break

#                 # Look for event name to the right of the indicator
#                 right_tokens = []
#                 for right_token in token.rights:
#                     if right_token.pos_ in ["PROPN", "NOUN", "ADJ"] and right_token.text.lower() not in non_event_words:
#                         right_tokens.append(right_token.text)
#                     else:
#                         break

#                 # Combine left and right tokens
#                 event_name_tokens = left_tokens + right_tokens

#                 # Remove common words that might not be part of the event name
#                 event_name_tokens = [t for t in event_name_tokens if t.lower() not in ["the", "a", "an"]]

#                 if event_name_tokens:
#                     return " ".join(event_name_tokens)

#         # If no event name is found, return None
#         return None

#     # Function to extract guest in a sentence
#     def extract_guest_name(self, sentence):
#         doc = self.nlp(sentence)
#         guest_keywords = [
#             "guest", "honor", "special guest", "keynote speaker", "speaker", "visitor",
#             "invitee", "chief guest", "special invitee", "guest of honor", "featured", "invite"
#         ]

#         guest_mentions = []

#         for token in doc:
#             if any(keyword in token.lemma_.lower() for keyword in guest_keywords):
#                 # Look for the closest person entity
#                 closest_person = None
#                 min_distance = float('inf')

#                 for ent in doc.ents:
#                     if ent.label_ == "PERSON":
#                         distance = abs(ent.start - token.i)
#                         if distance < min_distance:
#                             min_distance = distance
#                             closest_person = ent.text

#                 if closest_person:
#                     guest_mentions.append(closest_person)

#         # Remove duplicates and return the cleaned list of guest names
#         guest_mentions = list(set(guest_mentions))
#         return guest_mentions if guest_mentions else None



#     # Update the main analysis function
#     def analyze_sentence(self, sentence):
#         time_ranges = self.extract_times(sentence)
#         people_count = self.count_people(sentence)
#         dates = self.extract_dates(sentence)
#         person_names = self.extract_person_names(sentence)
#         event_name = self.extract_event_name(sentence)
#         guest_name = self.extract_guest_name(sentence)  # Properly calling the new function

#         # Extract the first time range or default to None
#         start_time, end_time = time_ranges[0] if time_ranges else (None, None)

#         return {
#             "start_time": start_time,
#             "end_time": end_time,
#             "people_count": people_count,
#             "dates": dates,
#             "person_names": person_names,
#             "event_name": event_name,
#             "guest_name": guest_name,  # Include guest name in the result
#         }



























import spacy
import re
from datetime import datetime, timedelta, time

class SentenceAnalyzer:
    def __init__(self):
        # Load SpaCy's small English model
        self.nlp = spacy.load("en_core_web_sm")
        self.manual_locations = ['Kumbh', 'maha kumbh', 'Prayagraj']

        # Regular expression pattern to match time expressions
        self.time_pattern = r"(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm)|(?:twelve|one|two|three|four|five|six|seven|eight|nine|ten|eleven)\s*(?:AM|PM|am|pm))"

        # Person Names to classify them in text
        self.predefined_names = ["Narendra Modi", "Modi", "Yogi Adityanath", "Yogi","Amit Shah"]

        # event names to classify them in text
        self.predefined_event_names = ["Maha Kumbh Aarti", "Kumbh Aarti","Maha Aarti", "Aarti"]

        # Regular expression pattern to match date expressions
        self.date_patterns = [
            r'\b(\d{2}/\d{2}/\d{4})\b',  # DD/MM/YYYY
            r'\b(\d{2}-\d{2}-\d{4})\b',  # DD-MM-YYYY
            r'\b(\d{4}/\d{2}/\d{2})\b',  # YYYY/MM/DD
            r'\b(\d{4}-\d{2}-\d{2})\b',  # YYYY-MM-DD
            r'\b(\w+ \d{1,2}(?:st|nd|rd|th)?,? \d{4})\b',  # Month DD, YYYY or Month DDth, YYYY
            r'\b(\d{1,2}(?:st|nd|rd|th)? \w+,? \d{4})\b',  # DD Month YYYY or DDth Month YYYY
            r'\b(\w+ \d{1,2}(?:st|nd|rd|th)?)\b'  # Month DD or Month DDth (assumes current year)
        ]

        # Dictionary to map phrases to specific times
        self.phrase_time_mapping = {
            "late night": ("11:00 PM", None),
            "mid night": ("12:00 AM", None),
            "early morning": ("5:00 AM", None),
            "morning": ("9:00 AM", None),
            "afternoon": ("12:00 PM", None),
            "noon": ("2:00 PM", None),
            "evening": ("6:00 PM", None),
            "night": ("8:00 PM", None)
        }

    #clean
    def clean_sentence(self,sentence):
        # First, remove all commas
        sentence = sentence.replace(',', '')

        # Then, remove specific periods
        result = []
        for i, char in enumerate(sentence):
            if char == '.':
                if i == len(sentence) - 1 or sentence[i+1].isspace() or not sentence[i+1].isalnum():
                    continue
            result.append(char)

        return ''.join(result)

    def extract_locations(self, text):
        doc = self.nlp(text)
        extracted_locations = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]

        # Add only those manual locations that are mentioned in the text
        for location in self.manual_locations:
            if location.lower() in text.lower():
                extracted_locations.append(location)

        return extracted_locations

    def find_starting_location(self, text, locations):
        # Define a regex pattern to capture the starting location
        pattern = re.compile(r'\bfrom\b\s+([A-Za-z\s]+?)(?:\s+to\s+|$)')
        match = pattern.search(text)
        if match:
            start_location = match.group(1).strip()
            # Ensure the starting location is in the list of extracted locations
            if start_location in locations:
                return start_location
        return None

    def extract_travel_info(self, text):
        locations = self.extract_locations(text)
        start_location = self.find_starting_location(text, locations)

        if not start_location:
            start_location = "current location"

        if start_location in locations:
            # Remove the starting location from the list to find the ending location
            locations.remove(start_location)

        end_location = locations[0] if locations else None

        return start_location, end_location

    # Function to convert time string to standardized format
    def standardize_time(self, time_str):
        if not time_str:
            return None

        # Convert word numbers to digits
        word_to_num = {
            'twelve': '12', 'one': '1', 'two': '2', 'three': '3', 'four': '4',
            'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
            'ten': '10', 'eleven': '11'
        }
        for word, num in word_to_num.items():
            time_str = time_str.replace(word, num)

        # Try parsing with various formats
        for fmt in ['%I:%M %p', '%I %p', '%I%p']:
            try:
                return datetime.strptime(time_str.upper(), fmt).strftime('%I:%M %p')
            except ValueError:
                pass
        return None

    # Function to extract start and end dates from a sentence
    def extract_dates(self, sentence):
        today = datetime.now().date()
        start_date = None
        end_date = None

        start_keywords = ['from', 'start', 'starts', 'begin', 'begins', 'starting', 'commencing', 'takes place', 'travel']
        end_keywords = ['to', 'till', 'last', 'until', 'end', 'ended', 'ending', 'finishing', 'take place', 'deadline', 'by', 'before', 'expires', 'expire', 'conclude']

        lower_sentence = sentence.lower()

        if "day after tomorrow" in lower_sentence:
            start_date = (today + timedelta(days=2)).strftime('%Y-%m-%d')
            end_date = None
            return start_date, end_date

        # Handle "X days from today" pattern
        days_from_today_match = re.search(r'(\d+)\s*days?\s*from\s*(today|now)', lower_sentence)
        if days_from_today_match:
            days = int(days_from_today_match.group(1))
            start_date = (today + timedelta(days=days)).strftime('%Y-%m-%d')
            return start_date, None

        after_days_match = re.search(r'after (\w+|\d+) days?', lower_sentence)
        if after_days_match:
            days_text = after_days_match.group(1)
            if days_text.isdigit():
                days = int(days_text)
            else:
                text_to_num = {
                    'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
                    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
                }
                days = text_to_num.get(days_text, 0)
            if days > 0:
                # start_date = today.strftime('%Y-%m-%d')
                start_date = (today + timedelta(days=days)).strftime('%Y-%m-%d')
                return start_date, end_date

        dates = []
        for pattern in self.date_patterns:
            matches = re.findall(pattern, sentence)
            for match in matches:
                try:
                    for fmt in ['%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%Y-%m-%d', '%B %d, %Y', '%d %B, %Y', '%B %d %Y', '%d %B %Y', '%B %d', '%d %B', '%m/%d/%y']:
                        try:
                            # Remove any ordinal suffixes before parsing
                            cleaned_match = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', match)
                            parsed_date = datetime.strptime(cleaned_match, fmt)
                            if fmt in ['%B %d', '%d %B']:
                                parsed_date = parsed_date.replace(year=today.year)
                            elif fmt == '%m/%d/%y':
                                # Adjust the year for two-digit year format
                                if parsed_date.year > today.year % 100 + 2000:
                                    parsed_date = parsed_date.replace(year=parsed_date.year - 100)
                            formatted_date = parsed_date.strftime('%Y-%m-%d')
                            dates.append(formatted_date)
                            break
                        except ValueError:
                            continue
                except ValueError:
                    continue

        # Handle additional date formats
        month_names = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month_abbr = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        ordinal_pattern = r'(\d{1,2})(?:st|nd|rd|th)'

        # Dictionary to map month abbreviations to full names
        month_abbr_to_full = {
            'Jan': 'January', 'Feb': 'February', 'Mar': 'March', 'Apr': 'April',
            'May': 'May', 'Jun': 'June', 'Jul': 'July', 'Aug': 'August',
            'Sep': 'September', 'Oct': 'October', 'Nov': 'November', 'Dec': 'December'
        }

        # pattern for "September 2nd" format
        month_day_pattern = r'([A-Za-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?'
        month_day_match = re.search(month_day_pattern, sentence, re.IGNORECASE)

        if month_day_match:
            month, day = month_day_match.groups()  # Correct order of groups
            current_year = datetime.now().year

            try:
                date = datetime.strptime(f"{month} {day} {current_year}", "%B %d %Y").date()
                date_str = date.strftime('%Y-%m-%d')
                sentence_lower = sentence.lower()
                start_found = any(keyword in sentence_lower for keyword in start_keywords)
                end_found = any(keyword in sentence_lower for keyword in end_keywords)
                if start_found and not end_found:
                    return date_str, None  # Start date found
                elif end_found and not start_found:
                    return None, date_str  # End date found
                elif start_found and end_found:
                    start_pos = min(sentence_lower.find(k) for k in start_keywords if k in sentence_lower)
                    end_pos = min(sentence_lower.find(k) for k in end_keywords if k in sentence_lower)

                    if start_pos < end_pos:
                        return date_str, None  # More likely a start date
                    else:
                        return None, date_str  # More likely an end date
                else:
                    return date_str, None
            except ValueError as e:
                pass

        # Handle date ranges like "July 1st to 7th"
        date_range_pattern = r'(\w+)\s+(\d{1,2})(?:st|nd|rd|th)?\s+to\s+(\d{1,2})(?:st|nd|rd|th)?'
        date_range_match = re.search(date_range_pattern, sentence, re.IGNORECASE)

        if date_range_match:
            month, start_day, end_day = date_range_match.groups()
            year = datetime.now().year
            try:
                start_date = datetime.strptime(f"{month} {start_day} {year}", "%B %d %Y").date()
                end_date = datetime.strptime(f"{month} {end_day} {year}", "%B %d %Y").date()
                return {start_date.strftime('%Y-%m-%d'),end_date.strftime('%Y-%m-%d')}
            except ValueError as e:
                pass

        # pattern for "2nd September" format
        month_day_pattern3 = r'(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)'
        month_day_match3 = re.search(month_day_pattern3, sentence, re.IGNORECASE)

        if month_day_match3:
            day, month = month_day_match3.groups()
            current_year = datetime.now().year

            try:
                date = datetime.strptime(f"{day} {month} {current_year}", "%d %B %Y").date()
                date_str = date.strftime('%Y-%m-%d')
                sentence_lower = sentence.lower()
                start_found = any(keyword in sentence_lower for keyword in start_keywords)
                end_found = any(keyword in sentence_lower for keyword in end_keywords)
                if start_found and not end_found:
                    return date_str, None  # Start date found
                elif end_found and not start_found:
                    return None, date_str  # End date found
                elif start_found and end_found:
                    start_pos = min(sentence_lower.find(k) for k in start_keywords if k in sentence_lower)
                    end_pos = min(sentence_lower.find(k) for k in end_keywords if k in sentence_lower)
                    if start_pos < end_pos:
                        return date_str, None  # More likely a start date
                    else:
                        return None, date_str  # More likely an end date
                else:
                    return date_str, None
            except ValueError as e:
                pass

        # pattern for "DD(st|nd|rd|th) of Month" format
        month_day_pattern = r'(\d{1,2})(?:st|nd|rd|th)?\s+of\s+(\w+)'
        month_day_match = re.search(month_day_pattern, sentence, re.IGNORECASE)

        if month_day_match:
            day, month = month_day_match.groups()
            current_year = datetime.now().year
            try:
                date = datetime.strptime(f"{day} {month} {current_year}", "%d %B %Y")
                date_str = date.strftime('%Y-%m-%d')
                sentence_lower = sentence.lower()
                start_found = any(keyword in sentence_lower for keyword in start_keywords)
                end_found = any(keyword in sentence_lower for keyword in end_keywords)
                if start_found and not end_found:
                    return date_str, None  # Start date found
                elif end_found and not start_found:
                    return None, date_str  # End date found
                elif start_found and end_found:
                    start_pos = min(sentence_lower.find(k) for k in start_keywords if k in sentence_lower)
                    end_pos = min(sentence_lower.find(k) for k in end_keywords if k in sentence_lower)
                    if start_pos < end_pos:
                        return date_str, None  # More likely a start date
                    else:
                        return None, date_str  # More likely an end date
                else:
                    return date_str, None
            except ValueError as e:
                pass

        # Pattern to match dates like "22nd Nov"
        date_without_year_pattern = r'(\d{1,2})(?:st|nd|rd|th)?\s+(\w{3})'
        date_without_year_match = re.search(date_without_year_pattern, sentence, re.IGNORECASE)

        if date_without_year_match:
            day, month_abbr = date_without_year_match.groups()
            month_abbr = month_abbr.capitalize()  # Ensure first letter is capitalized

            if month_abbr in month_abbr_to_full:
                month_full = month_abbr_to_full[month_abbr]
                try:
                    parsed_date = datetime.strptime(f"{day} {month_full} {today.year}", "%d %B %Y").date()
                    if parsed_date < today:
                        parsed_date = parsed_date.replace(year=today.year + 1)
                    date_str = parsed_date.strftime('%Y-%m-%d')
                    sentence_lower = sentence.lower()
                    start_found = any(keyword in sentence_lower for keyword in start_keywords)
                    end_found = any(keyword in sentence_lower for keyword in end_keywords)
                    if start_found and not end_found:
                        return date_str, None  # Start date found
                    elif end_found and not start_found:
                        return None, date_str  # End date found
                    elif start_found and end_found:
                        start_pos = min(sentence_lower.find(k) for k in start_keywords if k in sentence_lower)
                        end_pos = min(sentence_lower.find(k) for k in end_keywords if k in sentence_lower)
                        if start_pos < end_pos:
                            return date_str, None  # More likely a start date
                        else:
                            return None, date_str  # More likely an end date
                    else:
                        return date_str, None
                except ValueError:
                    pass

        # Pattern to match dates like "Nov 22nd"
        date_without_year_pattern = r'(\w{3})\s+(\d{1,2})(?:st|nd|rd|th)'
        date_without_year_match = re.search(date_without_year_pattern, sentence, re.IGNORECASE)

        if date_without_year_match:
            month_abbr, day = date_without_year_match.groups()  # Corrected to properly assign day and month_abbr
            month_abbr = month_abbr.capitalize()  # Ensure first letter is capitalized

            if month_abbr in month_abbr_to_full:
                month_full = month_abbr_to_full[month_abbr]
                try:
                    parsed_date = datetime.strptime(f"{day} {month_full} {today.year}", "%d %B %Y").date()
                    if parsed_date < today:
                        parsed_date = parsed_date.replace(year=today.year + 1)
                    date_str = parsed_date.strftime('%Y-%m-%d')
                    sentence_lower = sentence.lower()
                    start_found = any(keyword in sentence_lower for keyword in start_keywords)
                    end_found = any(keyword in sentence_lower for keyword in end_keywords)
                    if start_found and not end_found:
                        return date_str, None  # Start date found
                    elif end_found and not start_found:
                        return None, date_str  # End date found
                    elif start_found and end_found:
                        start_pos = min(sentence_lower.find(k) for k in start_keywords if k in sentence_lower)
                        end_pos = min(sentence_lower.find(k) for k in end_keywords if k in sentence_lower)
                        if start_pos < end_pos:
                            return date_str, None  # More likely a start date
                        else:
                            return None, date_str  # More likely an end date
                    else:
                        return date_str, None
                except ValueError:
                    pass

        # Check for recurring monthly patterns
        recurring_pattern = r'(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?(?:every|each)\s+month'
        recurring_match = re.search(recurring_pattern, lower_sentence)
        if recurring_match:
            day = int(recurring_match.group(1))
            next_occurrence = today.replace(day=1)  # Start from the first of the current month
            while next_occurrence.day != day:
                next_occurrence += timedelta(days=1)
            if next_occurrence <= today:
                next_occurrence = next_occurrence.replace(month=next_occurrence.month % 12 + 1)
                if next_occurrence.month == 1:
                    next_occurrence = next_occurrence.replace(year=next_occurrence.year + 1)
            end_date = next_occurrence.strftime('%Y-%m-%d')
            return start_date, end_date

        # Handle "MM-DD-YYYY" format (e.g., "11-22-2024")
        hyphen_date_pattern = r'(\d{1,2}-\d{1,2}-\d{4})'
        hyphen_date_match = re.search(hyphen_date_pattern, sentence)
        if hyphen_date_match:
            try:
                parsed_date = datetime.strptime(hyphen_date_match.group(1), '%m-%d-%Y').date()
                return parsed_date.strftime('%Y-%m-%d'), None
            except ValueError:
                pass

        # Handle "DD.MM.YYYY" format
        dot_date_pattern = r'(\d{1,2}\.\d{1,2}\.\d{4})'
        dot_date_matches = re.findall(dot_date_pattern, sentence)
        for match in dot_date_matches:
            try:
                parsed_date = datetime.strptime(match, '%d.%m.%Y')
                formatted_date = parsed_date.strftime('%Y-%m-%d')
                if not start_date:
                    start_date = formatted_date
                else:
                    end_date = formatted_date
            except ValueError:
                continue

        # pattern for MM.DD.YY format
        dot_date_pattern = r'(\d{1,2}\.\d{1,2}\.\d{2})'
        dot_date_matches = re.findall(dot_date_pattern, sentence)
        for match in dot_date_matches:
            try:
                parsed_date = datetime.strptime(match, '%d.%m.%y')
                if parsed_date.year > datetime.now().year % 100 + 2000:
                    parsed_date = parsed_date.replace(year=parsed_date.year - 100)
                formatted_date = parsed_date.strftime('%Y-%m-%d')
                if not start_date:
                    start_date = formatted_date
                else:
                    end_date = formatted_date
            except ValueError:
                continue

        # Handle "DD-MM-YYYY" format
        dot_date_pattern = r'(\d{1,2}\-\d{1,2}\-\d{4})'
        dot_date_matches = re.findall(dot_date_pattern, sentence)
        for match in dot_date_matches:
            try:
                parsed_date = datetime.strptime(match, '%d.%m.%Y')
                formatted_date = parsed_date.strftime('%Y-%m-%d')
                if not start_date:
                    start_date = formatted_date
                else:
                    end_date = formatted_date
            except ValueError:
                continue

        # Pattern for date ranges like "May 1 - June 30, 2025"
        date_range_pattern = r'(\w+\s+\d{1,2})\s*-\s*(\w+\s+\d{1,2}),?\s*(\d{4})?'
        date_range_match = re.search(date_range_pattern, sentence)

        if date_range_match:
            start_date_str, end_date_str, year = date_range_match.groups()
            year = int(year) if year else today.year

            try:
                start_date = datetime.strptime(f"{start_date_str} {year}", "%B %d %Y").date()
                end_date = datetime.strptime(f"{end_date_str} {year}", "%B %d %Y").date()

                # If end date is earlier than start date, assume it's in the next year
                if end_date < start_date:
                    end_date = end_date.replace(year=year + 1)

                return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
            except ValueError:
                pass
        date_range_pattern = r'(\w+\s+\d{1,2})\s*-\s*(\w+\s+\d{1,2}),?\s*(\d{4})'
        date_range_match = re.search(date_range_pattern, sentence)

        if date_range_match:
            start_date_str, end_date_str, year = date_range_match.groups()
            try:
                start_date = datetime.strptime(f"{start_date_str} {year}", "%b %d %Y").date()
                end_date = datetime.strptime(f"{end_date_str} {year}", "%b %d %Y").date()
                return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
            except ValueError:
                pass

        # Pattern for date ranges like "May 1 to June 30, 2025"
        date_range_pattern = r'(\w+\s+\d{1,2})\s+to\s+(\w+\s+\d{1,2}),?\s+(\d{4})?'
        date_range_match = re.search(date_range_pattern, sentence)

        if date_range_match:
            start_date_str, end_date_str, year = date_range_match.groups()
            year = int(year) if year else today.year

            try:
                start_date = datetime.strptime(f"{start_date_str} {year}", "%B %d %Y").date()
                end_date = datetime.strptime(f"{end_date_str} {year}", "%B %d %Y").date()

                # If end date is earlier than start date, assume it's in the next year
                if end_date < start_date:
                    end_date = end_date.replace(year=year + 1)

                return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
            except ValueError:
                pass

        # Handle date ranges like "July 1 to 7, 2024"
        date_range_pattern = r'\s+(\w+\s+\d{1,2})\s+to\s+(\d{1,2})(?:,?\s+(\d{4}))?'
        date_range_match = re.search(date_range_pattern, sentence, re.IGNORECASE)
        if date_range_match:
            start_date_str = date_range_match.group(1)
            end_day = date_range_match.group(2)
            year = date_range_match.group(3) or str(today.year)

            try:
                start_date = datetime.strptime(f"{start_date_str} {year}", "%B %d %Y").date()
                end_date = datetime.strptime(f"{start_date.strftime('%B')} {end_day} {year}", "%B %d %Y").date()
                return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
            except ValueError:
                pass

        # Handle date ranges like "July 1-7, 2024"
        date_range_pattern = r'\s+(\w+\s+\d{1,2})\s*-\s*(\d{1,2})(?:,?\s*(\d{4}))?'
        date_range_match = re.search(date_range_pattern, sentence, re.IGNORECASE)
        if date_range_match:
            start_date_str = date_range_match.group(1)
            end_day = date_range_match.group(2)
            year = date_range_match.group(3) or str(today.year)

            try:
                start_date = datetime.strptime(f"{start_date_str} {year}", "%B %d %Y").date()
                end_date = datetime.strptime(f"{start_date.strftime('%B')} {end_day} {year}", "%B %d %Y").date()
                return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
            except ValueError:
                pass

        # Handle "Month D-D, YYYY" format
        month_range_pattern = r'(\w+)\s+(\d{1,2})-(\d{1,2}),?\s+(\d{4})'
        month_range_matches = re.findall(month_range_pattern, sentence)
        for match in month_range_matches:
            try:
                month, start_day, end_day, year = match
                start_parsed = datetime.strptime(f"{month} {start_day} {year}", '%B %d %Y')
                end_parsed = datetime.strptime(f"{month} {end_day} {year}", '%B %d %Y')
                start_date = start_parsed.strftime('%Y-%m-%d')
                end_date = end_parsed.strftime('%Y-%m-%d')
            except ValueError:
                continue

        # Add or modify this pattern to handle "Month Day, Year" format
        mul_date_pattern = r'(\w+\s+\d{1,2},?\s*\d{4})\s+to\s+(\w+\s+\d{1,2},?\s*\d{4})'
        mul_date_match = re.search(mul_date_pattern, sentence)
        single_date_pattern = r'(\w+\s+\d{1,2},?\s*\d{4})'
        single_date_match = re.search(single_date_pattern, sentence)

        if mul_date_match:
            start_date_str, end_date_str = mul_date_match.groups()

            try:
                # Parse start and end dates with the year
                start_date = datetime.strptime(start_date_str, "%B %d, %Y").date()
                end_date = datetime.strptime(end_date_str, "%B %d, %Y").date()

                # Adjust the end date if it's earlier than the start date, assuming the next year
                if end_date < start_date:
                    end_date = end_date.replace(year=start_date.year + 1)

                return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
            except ValueError as e:
                pass
        elif single_date_match:
            date_str = single_date_match.group(1)
            try:
                parsed_date = datetime.strptime(date_str, "%B %d, %Y").date()
                start_date = parsed_date.strftime('%Y-%m-%d')
                end_date = None  # No end date for single date mentions
                return start_date, end_date
            except ValueError:
                pass


        # Handle "D-M-YYYY" format
        hyphen_date_pattern = r'(\d{1,2}-\d{1,2}-\d{4})'
        hyphen_date_matches = re.findall(hyphen_date_pattern, sentence)
        for match in hyphen_date_matches:
            try:
                parsed_date = datetime.strptime(match, '%d-%m-%Y')
                formatted_date = parsed_date.strftime('%Y-%m-%d')
                if not start_date:
                    start_date = formatted_date
                else:
                    end_date = formatted_date
            except ValueError:
                continue


        def parse_two_digit_year(year):
            year = int(year)
            if year < 70:
                return 2000 + year
            else:
                return 1900 + year

        # Add new pattern for MM/DD/YY format
        short_date_pattern = r'(\d{1,2})/(\d{1,2})/(\d{2})'
        short_date_matches = re.findall(short_date_pattern, sentence)
        for match in short_date_matches:
            month, day, year = match
            full_year = parse_two_digit_year(year)
            try:
                parsed_date = datetime(full_year, int(month), int(day))
                formatted_date = parsed_date.strftime('%Y-%m-%d')
                if not start_date:
                    start_date = formatted_date
                else:
                    end_date = formatted_date
            except ValueError:
                continue


        if len(dates) == 1:
            end_keyword_present = any(keyword in lower_sentence for keyword in end_keywords)
            start_keyword_present = any(keyword in lower_sentence for keyword in start_keywords)

            if end_keyword_present and not start_keyword_present:
                start_date = today.strftime('%Y-%m-%d')
                end_date = dates[0]
            else:
                start_date = dates[0]
                end_date = None

        elif len(dates) > 1:
            start_date_index = float('inf')
            end_date_index = -1

            for keyword in start_keywords:
                if keyword in lower_sentence:
                    start_index = lower_sentence.index(keyword)
                    start_date_index = min(start_date_index, start_index)

            for keyword in end_keywords:
                if keyword in lower_sentence:
                    end_index = lower_sentence.index(keyword)
                    end_date_index = max(end_date_index, end_index)

            if start_date_index < end_date_index:
                start_date = dates[0]
                end_date = dates[-1]
            elif end_date_index < start_date_index:
                start_date = dates[-1]
                end_date = dates[0]
            else:
                start_date = dates[0]
                end_date = dates[-1]

        # Dictionary for handling relative date expressions
        relative_dates = {
            'today': 0,
            'tomorrow': 1,
            'yesterday': -1
        }

        lower_sentence = sentence.lower()
        # Handle "next week" separately
        if "next week" in lower_sentence:
            # Calculate the start of next week (Monday)
            days_until_next_monday = (7 - today.weekday()) % 7
            if days_until_next_monday == 0:
                days_until_next_monday = 7  # If today is Monday, we want next Monday
            start_of_next_week = today + timedelta(days=days_until_next_monday)
            start_date = start_of_next_week.strftime('%Y-%m-%d')
            end_date = None
            return start_date, end_date

        # Check for relative date expressions
        for expression, offset in relative_dates.items():
            if expression in lower_sentence:
                start_date = (today + timedelta(days=offset)).strftime('%Y-%m-%d')
                end_date = start_date
                return start_date, end_date

        if start_date is None and end_date is None:
            return None, None
        return start_date, end_date

    # Function to extract start and end times from a sentence
    def extract_times(self,sentence):
        times = []
        word_to_digit = {
            'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
            'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10',
            'eleven': '11', 'twelve': '12'
        }

        start_keywords = ['from', 'start', 'starts', 'begin', 'begins', 'starting', 'commencing', 'started', 'commence']
        end_keywords = ['to', 'till', 'last', 'until', 'end', 'ended', 'ending', 'finishing','finish', 'deadline', 'by', 'before', 'expires', 'expire', 'conclude', 'ends']

        # Pattern to match time expressions like "nine in the morning" or "eight at night"
        word_time_pattern = r'(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\s+(in the|at)\s+(morning|afternoon|evening|night)'

        word_time_matches = re.findall(word_time_pattern, sentence, re.IGNORECASE)

        for match in word_time_matches:
            hour = word_to_digit[match[0].lower()]
            period = match[2].lower()

            if period in ['morning', 'afternoon']:
                time = f"{hour}:00 AM" if int(hour) < 12 else f"{hour}:00 PM"
            elif period in ['evening', 'night']:
                time = f"{hour}:00 PM" if int(hour) < 12 else f"{int(hour) % 12 or 12}:00 AM"

            times.append(self.standardize_time(time))

        # If we found word-based times, determine if they are start or end times
        if times:
            start_time = None
            end_time = None
            for keyword in start_keywords:
                if keyword in sentence.lower():
                    start_time = times[0]
                    end_time = times[1] if len(times) > 1 else None
                    break
            if not start_time:
                for keyword in end_keywords:
                    if keyword in sentence.lower():
                        end_time = times[0]
                        start_time = times[1] if len(times) > 1 else None
                        break
            return [(start_time, end_time)]

        # If no word-based times found, fall back to the original time extraction logic
        time_pattern1 = r"(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm)|(?:twelve|one|two|three|four|five|six|seven|eight|nine|ten|eleven)\s*(?:AM|PM|am|pm))"
        matches = re.findall(time_pattern1, sentence, re.IGNORECASE)
        matches = [self.standardize_time(match) for match in matches if self.standardize_time(match)]

        if matches:
            start_time = None
            end_time = None
            for keyword in start_keywords:
                if keyword in sentence.lower():
                    start_time = matches[0]
                    end_time = matches[1] if len(matches) > 1 else None
                    break
            if not start_time:
                for keyword in end_keywords:
                    if keyword in sentence.lower():
                        end_time = matches[0]
                        start_time = matches[1] if len(matches) > 1 else None
                        break
            return [(start_time, end_time)]

        # Check for "from X to Y" pattern where X and Y are time periods
        time_range_pattern = r'from\s+(morning|afternoon|evening|night)\s+(to|till|until)\s+(morning|afternoon|evening|night)'
        time_range_match = re.search(time_range_pattern, sentence, re.IGNORECASE)
        if time_range_match:
            start_period = time_range_match.group(1).lower()
            end_period = time_range_match.group(3).lower()
            start_time = self.phrase_time_mapping.get(start_period, (None, None))[0]
            end_time = self.phrase_time_mapping.get(end_period, (None, None))[0]
            if start_time and end_time:
                return [(start_time, end_time)]

        # Check for "from X to Y" pattern
        time_range_pattern1 = r'from\s+(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm))\s+(?:to|till|until)\s+(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm))'
        time_range_match1 = re.search(time_range_pattern1, sentence, re.IGNORECASE)

        if time_range_match1:
            start_time = self.standardize_time(time_range_match1.group(1))
            end_time = self.standardize_time(time_range_match1.group(2))
            if start_time and end_time:
                return [(start_time, end_time)]

        # If no specific pattern is found, fall back to finding individual times
        times = re.findall(self.time_pattern, sentence, re.IGNORECASE)
        if times:
            if len(times) == 1:
                end_keyword_present = any(keyword in lower_sentence for keyword in end_keywords)
                start_keyword_present = any(keyword in lower_sentence for keyword in start_keywords)

                if end_keyword_present and not start_keyword_present:
                    start_date = None
                    end_date = self.standardize_time(times[0])
                else:
                    start_date = self.standardize_time(times[0])
                    end_date = None
            elif len(times) >= 2:
                return [(self.standardize_time(times[0]), self.standardize_time(times[1]))]


        time_range_pattern = r'from\s+(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm))\s+to\s+(\d{1,2}(?::\d{2})?\s*(?:AM|PM|am|pm))'
        time_range_match = re.search(time_range_pattern, sentence, re.IGNORECASE)

        if time_range_match:
            start_time = self.standardize_time(time_range_match.group(1))
            end_time = self.standardize_time(time_range_match.group(2))
            if start_time and end_time:
                return [(start_time, end_time)]

        # Check for "period X:XX" time format
        specific_time_pattern1 = r'(morning|afternoon|evening|night)\s*(\d{1,2})(?:\s*:\s*(\d{2}))?'
        specific_time_match1 = re.search(specific_time_pattern1, sentence, re.IGNORECASE)

        if specific_time_match1:
            period = specific_time_match1.group(1).lower()
            hour = int(specific_time_match1.group(2))
            minute = specific_time_match1.group(3)
            minute = int(minute) if minute else 0

            if period == 'morning':
                if hour == 12:
                    time_str = f"12:{minute:02d} AM"
                else:
                    time_str = f"{hour:02d}:{minute:02d} AM"
            elif period == 'afternoon':
                if hour < 12:
                    hour += 12
                time_str = f"{hour%12 or 12:02d}:{minute:02d} PM"
            elif period == 'evening':
                if hour < 12:
                    hour += 12
                time_str = f"{hour%12 or 12:02d}:{minute:02d} PM"
            elif period == 'night':
                if hour == 12:
                    time_str = f"12:{minute:02d} AM"
                elif hour < 12:
                    time_str = f"{hour:02d}:{minute:02d} PM"
                else:
                    time_str = f"{hour%12:02d}:{minute:02d} AM"

            times.append((time_str, None))

        # First, check for specific time mentions
        specific_time_pattern = r'(\d{1,2})(?:\s*:\s*(\d{2}))?\s*(in the|at)\s*(morning|afternoon|evening|night)'
        specific_time_match = re.search(specific_time_pattern, sentence, re.IGNORECASE)
        if specific_time_match:
            hour = int(specific_time_match.group(1))
            minute = specific_time_match.group(2)
            minute = int(minute) if minute else 0
            period = specific_time_match.group(4).lower()

            if period == 'morning' and hour < 12:
                times.append((f"{hour:02d}:{minute:02d} AM", None))
            elif period in ['afternoon', 'evening'] or (period == 'morning' and hour == 12):
                if hour < 12:
                    hour += 12
                times.append((f"{hour%12 or 12:02d}:{minute:02d} PM", None))
            elif period == 'night':
                if hour == 12:
                    times.append((f"{hour:02d}:{minute:02d} AM", None))
                else:
                    hour += 12 if hour < 12 else 0
                    times.append((f"{hour%12 or 12:02d}:{minute:02d} PM", None))

        # Apply regex to find time expressions
        matches = re.findall(self.time_pattern, sentence, re.IGNORECASE)
        matches = [self.standardize_time(match) for match in matches if self.standardize_time(match)]

        # Handle phrases like "early morning"
        for phrase, (start_time, end_time) in self.phrase_time_mapping.items():
            if phrase in sentence.lower():
                times.append((start_time, end_time))

        start_keywords = ['start', 'begin', 'begins', 'from']
        end_keywords = ['end', 'finish', 'until', 'to']

        start_time = None
        end_time = None

        lower_sentence = sentence.lower()

        # Capture start time
        for keyword in start_keywords:
            if keyword in lower_sentence:
                start_index = lower_sentence.index(keyword)
                start_time_matches = re.findall(self.time_pattern, sentence[start_index:], re.IGNORECASE)
                if start_time_matches:
                    start_time = self.standardize_time(start_time_matches[0])
                    break

        # Capture end time
        for keyword in end_keywords:
            if keyword in lower_sentence:
                end_index = lower_sentence.index(keyword)
                end_time_matches = re.findall(self.time_pattern, sentence[end_index:], re.IGNORECASE)
                if end_time_matches:
                    end_time = self.standardize_time(end_time_matches[0])
                    break

        if start_time and end_time:
            times.append((start_time, end_time))
        elif start_time:
            times.append((start_time, None))
        elif end_time:
            times.append((None, end_time))

        # If no specific start/end times found, fall back to any times detected
        if not times and matches:
            if len(matches) >= 2:
                times.append((matches[0], matches[1]))
            else:
                end_keyword_present = any(keyword in lower_sentence for keyword in self.end_keyword)
                start_keyword_present = any(keyword in lower_sentence for keyword in self.start_keyword)

                if end_keyword_present and not start_keyword_present:
                    start_date = None
                    end_date = self.standardize_time(times[0])
                else:
                    start_date = self.standardize_time(times[0])
                    end_date = None

        # Check if start and end times are the same, and adjust accordingly
        if times and times[0][0] == times[0][1]:
            return [(times[0][0], None)]

        return times if times else [(None, None)]   

    # Function to count the number of people in a sentence
    def count_people(self, sentence):
        doc = self.nlp(sentence)

        # Count people based on named entities
        named_people_count = sum(1 for ent in doc.ents if ent.label_ == "PERSON")

        # Count personal pronouns and family relations
        personal_pronouns = ["i", "me", "you"]
        family_relations = ["brother", "sister", "mother", "father", "parent", "child", "son", "daughter", "sibling", "cousin", "aunt", "uncle", "grandparent", "grandfather", "grandmother"]
        other_person_indicators = ["friend", "colleague", "coworker"]

        pronoun_count = sum(1 for token in doc if token.text.lower() in personal_pronouns)
        family_count = sum(1 for token in doc if token.text.lower() in family_relations)
        other_count = sum(1 for token in doc if token.text.lower() in other_person_indicators)

        # Handle cases where people are mentioned by numbers (e.g., "two people")
        numeric_people_count = 0
        text_to_num = {
            "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
            "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
            "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13,
            "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
            "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30,
            "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80,
            "ninety": 90, "hundred": 100, "thousand": 1000
        }

        # Search for numeric values and associated "people" or "colleagues" in the sentence
        tokens = sentence.lower().split()
        for i, token in enumerate(tokens):
            if token.isdigit() or token in text_to_num:
                if i + 1 < len(tokens) and tokens[i + 1] in ["people", "person", "colleagues"]:
                    numeric_people_count = int(token) if token.isdigit() else text_to_num[token]
                    return numeric_people_count  # Return immediately if we find a specific number of people

        # If no specific number is found, calculate total as before
        total_people_count = named_people_count + pronoun_count + family_count + other_count

        # Get the list of person names
        person_names = self.extract_person_names(sentence)

        # Compare the count of person names with the total_people_count
        if person_names and len(person_names) > total_people_count:
            total_people_count = len(person_names)

        # Return None if the total count is zero
        return None if total_people_count == 0 else total_people_count

    # Function to extract name of people in a sentence
    def extract_person_names(self, sentence):
        doc = self.nlp(sentence)
        person_names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

        # Extract event name
        event_name = self.extract_event_name(sentence)

        # Check for predefined names
        found_names = []
        for name in self.predefined_names:
            if name in sentence and not any(name in found_name for found_name in found_names):
                found_names.append(name)

        # Combine and remove duplicates
        all_names = list(set(person_names + found_names))

        # Remove shorter versions of names if longer version exists
        final_names = []
        for name in all_names:
            if not any(name != other_name and name in other_name for other_name in all_names):
                # Exclude the event name from person names
                if event_name and name in event_name:
                    continue
                final_names.append(name)

        return final_names if final_names else None
  
    # Function to extract event name in a sentence
    def extract_event_name(self, sentence):
        # Convert the sentence to lowercase for case-insensitive matching
        lower_sentence = sentence.lower()

        # Check for predefined event names
        for event_name in self.predefined_event_names:
            if event_name.lower() in lower_sentence:
                return event_name

        # If no predefined event name is found, continue with the existing logic
        event_indicators = ["event", "meeting", "conference", "ceremony", "celebration", "party", "concert", "festival", "show", "seminar", "workshop"]
        non_event_words = ["tomorrow", "today", "yesterday", "next", "last", "this", "that", "the", "a", "an"]

        # First, check for quoted event names
        quoted_name_match = re.search(r"['\"](.*?)['\"]", sentence)
        if quoted_name_match:
            return quoted_name_match.group(1)

        # Use SpaCy to analyze the sentence
        doc = self.nlp(sentence)

        for token in doc:
            if token.text.lower() in event_indicators:
                # Look for event name to the left of the indicator
                left_tokens = []
                for left_token in reversed(list(token.lefts)):
                    if left_token.pos_ in ["PROPN", "NOUN", "ADJ"] and left_token.text.lower() not in non_event_words:
                        left_tokens.insert(0, left_token.text)
                    else:
                        break

                # Look for event name to the right of the indicator
                right_tokens = []
                for right_token in token.rights:
                    if right_token.pos_ in ["PROPN", "NOUN", "ADJ"] and right_token.text.lower() not in non_event_words:
                        right_tokens.append(right_token.text)
                    else:
                        break

                # Combine left and right tokens
                event_name_tokens = left_tokens + right_tokens

                # Remove common words that might not be part of the event name
                event_name_tokens = [t for t in event_name_tokens if t.lower() not in ["the", "a", "an"]]

                if event_name_tokens:
                    return " ".join(event_name_tokens)

        # If no event name is found, return None
        return None
    
    # Function to extract guest in a sentence
    def extract_guest_name(self, sentence, person_names):
        doc = self.nlp(sentence)
        guest_keywords = [
            "guest", "honor", "special guest", "keynote speaker", "speaker", "visitor",
            "invitee", "chief guest", "special invitee", "guest of honor", "featured", "invite"
        ]

        guest_mentions = []
        guest_keyword_found = False

        # Extract event name
        event_name = self.extract_event_name(sentence)

        for token in doc:
            if any(keyword in token.lemma_.lower() for keyword in guest_keywords):
                guest_keyword_found = True
                # Look for the closest person entity or predefined name
                closest_person = None
                min_distance = float('inf')

                for ent in doc.ents:
                    if ent.label_ == "PERSON":
                        distance = abs(ent.start - token.i)
                        if distance < min_distance:
                            min_distance = distance
                            closest_person = ent.text

                # Check predefined names
                for name in self.predefined_names:
                    if name in sentence:
                        name_index = sentence.index(name)
                        distance = abs(name_index - token.idx)
                        if distance < min_distance:
                            min_distance = distance
                            closest_person = name

                if closest_person and (not event_name or closest_person not in event_name):
                    guest_mentions.append(closest_person)

        # If no guests were found but a guest keyword was present, use person_names
        if not guest_mentions and guest_keyword_found and person_names:
            guest_mentions = person_names

        # Additional check for invitation-like phrases
        invite_patterns = [
            r'invite\s+(\w+(?:\s+\w+)?)',
            r'inviting\s+(\w+(?:\s+\w+)?)',
            r'invitation\s+to\s+(\w+(?:\s+\w+)?)',
            r'welcome\s+(\w+(?:\s+\w+)?)\s+as'
        ]

        for pattern in invite_patterns:
            matches = re.findall(pattern, sentence, re.IGNORECASE)
            for match in matches:
                if (match in person_names or any(match in name for name in person_names)) and (not event_name or match not in event_name):
                    guest_mentions.append(match)
        # New code to add more guests if guest count is greater than zero
        if len(guest_mentions) > 0:
            for i, token in enumerate(doc):
                if token.text.lower() in ["and", ",", "&"]:
                    # Check the next token after the connector
                    if i + 1 < len(doc):
                        next_token = doc[i + 1]
                        if next_token.ent_type_ == "PERSON" or next_token.pos_ == "PROPN":
                            full_name = next((name for name in person_names if next_token.text in name), next_token.text)
                            if full_name not in guest_mentions:
                                guest_mentions.append(full_name)

        # Remove duplicates and return
        return list(set(guest_mentions)) if guest_mentions else None
    
    # Function to calculate days
    def convert_text_to_digit(self, text):
        """Convert number words to digits."""
        
        # Dictionary for converting number words to digits
        number_words = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17,
            'eighteen': 18, 'nineteen': 19, 'twenty': 20
        }
        
        for word, digit in number_words.items():
            text = re.sub(r'\b' + word + r'\b', str(digit), text, flags=re.IGNORECASE)
        return text

    def extract_event_duration(self, text, start_date=None, end_date=None):
        """
        Extracts the delay before the event and the duration of the event from the input text.
        If no start or end date is provided, they are calculated based on the event duration.

        Args:
            text (str): Input text describing the event.
            start_date (str): The start date of the event (in 'YYYY-MM-DD') or None.
            end_date (str): The end date of the event (in 'YYYY-MM-DD') or None.

        Returns:
            dict: A dictionary containing the calculated start and end dates, 
                and the duration of the event in days. If both dates are None or empty, returns empty dates.
        """

        # Convert number words to digits first
        text = self.convert_text_to_digit(text)
        
        # Patterns to capture both forms of event duration and delay
        delay_pattern = re.search(r'after (\d+) day[s]?', text)  # Handles "after X day(s)"
        duration_pattern = re.search(r'(for|a|an) (\d+) day[s]?', text)  # Handles "for X day(s)" or "a X day(s) event"
        
        # Extract delay before event starts (default to 0 if not found)
        delay_days = int(delay_pattern.group(1)) if delay_pattern else 0
        
        # Extract the duration of the event (default to 1 if not found)
        duration_days = int(duration_pattern.group(2)) if duration_pattern else 1

        # Return empty if both dates are missing
        if not start_date and not end_date:
            start_date = ''
            end_date = ''
            event_duration = duration_days
            print(start_date, end_date, event_duration)
            return start_date, end_date, event_duration
            # return {'start_date': '', 'end_date': '', 'event_duration': duration_days}

        # If start_date is None, calculate it from end_date
        elif not start_date and end_date:
            try:
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
                start_date_obj = end_date_obj - timedelta(days=duration_days - 1)
                start_date = start_date_obj.strftime('%Y-%m-%d')
            except ValueError:
                start_date = ''
                end_date = ''
                event_duration = duration_days
                return start_date, end_date, event_duration
                # return {'start_date': '', 'end_date': '', 'event_duration': ''}

        # If end_date is None, calculate it from start_date
        elif not end_date and start_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                end_date_obj = start_date_obj + timedelta(days=duration_days - 1)
                end_date = end_date_obj.strftime('%Y-%m-%d')
            except ValueError:
                start_date = ''
                end_date = ''
                event_duration = duration_days
                return start_date, end_date, event_duration
                # return {'start_date': '', 'end_date': '', 'event_duration': ''}
        
        # If both dates are provided, just calculate the event duration
        elif start_date and end_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
                duration_days = (end_date_obj - start_date_obj).days + 1
            except ValueError:
                start_date = ''
                end_date = ''
                event_duration = duration_days
                print(start_date, end_date, event_duration)
                return start_date, end_date, event_duration
                # return {'start_date': '', 'end_date': '', 'event_duration': ''}
        
        # Return the calculated values
        return start_date, end_date, duration_days
        # return {
        #     'start_date': start_date,
        #     'end_date': end_date,
        #     'event_duration': duration_days
        # }

    # def calculate_days(self, start_date, end_date):
    #     if start_date and end_date:
    #         try:
    #             start = datetime.strptime(start_date, '%Y-%m-%d')
    #             end = datetime.strptime(end_date, '%Y-%m-%d')
    #             days_difference = (end - start).days
    #             return days_difference+1
    #         except ValueError:
    #             return None
    #     else:
    #         return None
        
    # Function to calculate time period
    def calculate_time_period(self,sentence, start_date, end_date, start_time, end_time):
        # Dictionary to convert word numbers to integers
        word_to_number = {
            'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,
            'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17,
            'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60,
            'seventy': 70, 'eighty': 80, 'ninety': 90, 'hundred': 100
        }

        # Function to convert word number to integer
        def word_to_int(word):
            return word_to_number.get(word.lower(), word)

        # Check for multi-day events
        multi_day_patterns = [
            r'(\d+|[a-zA-Z]+)\s+days?',
            r'finish(?:es)?\s+after\s+(\d+|[a-zA-Z]+)\s+days?'
        ]

        for pattern in multi_day_patterns:
            match = re.search(pattern, sentence, re.IGNORECASE)
            if match:
                days = word_to_int(match.group(1))
                try:
                    days = int(days)
                    if start_time and end_time:
                        start_time_obj = datetime.strptime(start_time, "%I:%M %p")
                        end_time_obj = datetime.strptime(end_time, "%I:%M %p")
                        daily_duration = (end_time_obj - start_time_obj).total_seconds() / 3600  # in hours
                        total_hours = days * daily_duration
                        hours = int(total_hours)
                        minutes = int((total_hours - hours) * 60)
                        return f"{hours} hours and {minutes} minutes"
                except ValueError:
                    pass

        # First, try to extract time period from the sentence
        period_patterns = [
            r'(?:for|period\s+of)\s+(\w+|\d+)\s*(hour|day|week|month|year)s?',
            r'(?:take)\s+(\w+|\d+)\s*(hour|day|week|month|year)s?',
            r'(?:over)\s+(\w+|\d+)\s*(hour|day|week|month|year)s?',
            r'(\w+|\d+)\s*(hour|day|week|month|year)s?\s+period'
        ]

        for pattern in period_patterns:
            period_match = re.search(pattern, sentence, re.IGNORECASE)
            if period_match:
                number = word_to_int(period_match.group(1))
                unit = period_match.group(2).lower()
                try:
                    number = int(number)
                    if unit == 'hour':
                        return f"{number} hours and 0 minutes"
                    elif unit == 'day':
                        return f"{number * 24} hours and 0 minutes"
                    elif unit == 'week':
                        return f"{number * 7 * 24} hours and 0 minutes"
                    elif unit == 'month':
                        return f"{number * 30 * 24} hours and 0 minutes"  # Approximation
                    elif unit == 'year':
                        return f"{number * 365 * 24} hours and 0 minutes"  # Approximation
                except ValueError:
                    # If conversion to int fails, it might be a complex word number
                    return None

        # If we have a start_date but no times, and we found a duration in the sentence
        if start_date and not (start_time or end_time) and period_match:
            return f"{number} hours and 0 minutes"

        # Convert times to datetime.time objects if they're strings
        if isinstance(start_time, str):
            start_time = datetime.strptime(start_time, "%I:%M %p").time()
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, "%I:%M %p").time()

        # If we only have start and end times (no dates), calculate the time difference
        if start_time and end_time and not (start_date or end_date):
            start_datetime = datetime.combine(datetime.today(), start_time)
            end_datetime = datetime.combine(datetime.today(), end_time)

            # If end time is earlier than start time, assume it's the next day
            if end_datetime < start_datetime:
                end_datetime += timedelta(days=1)

            time_difference = end_datetime - start_datetime
            hours = int(time_difference.total_seconds() // 3600)
            minutes = int((time_difference.total_seconds() % 3600) // 60)
            return f"{hours} hours and {minutes} minutes"

        # Case 1: Both start and end dates and times are provided
        if start_date and end_date and start_time and end_time:
            start = datetime.combine(datetime.strptime(start_date, "%Y-%m-%d").date(), start_time)
            end = datetime.combine(datetime.strptime(end_date, "%Y-%m-%d").date(), end_time)

        # Case 2: Start time is not given
        elif start_date and end_date and end_time:
            start = datetime.combine(datetime.strptime(start_date, "%Y-%m-%d").date(), time.min)
            end = datetime.combine(datetime.strptime(end_date, "%Y-%m-%d").date(), end_time)

        # Case 3: End date is not given
        elif start_date and start_time and end_time:
            start = datetime.combine(datetime.strptime(start_date, "%Y-%m-%d").date(), start_time)
            end = datetime.combine(datetime.strptime(start_date, "%Y-%m-%d").date(), end_time)

        # Case 4: Only end date and time are given
        elif end_date and end_time:
            start = datetime.combine(datetime.now().date(), time.min)
            end = datetime.combine(datetime.strptime(end_date, "%Y-%m-%d").date(), end_time)

        # Case 5: Only start date and time are given
        elif start_date and start_time:
            start = datetime.combine(datetime.strptime(start_date, "%Y-%m-%d").date(), start_time)
            end = datetime.combine(datetime.strptime(start_date, "%Y-%m-%d").date(), time.max)

        # Case 6: No sufficient information
        else:
            return None

        # Calculate the time difference
        time_difference = end - start

        # Convert to hours and minutes
        total_seconds = time_difference.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)

        return f"{hours} hours and {minutes} minutes"
    

    def extract_booking_status(self, text):
        list1 = ["complete", "completed", "finished", "finish"]
        list2 = ["cancelled", "canceled", "cancelled", "canceled"]
        # Convert the sentence to lowercase to ensure case-insensitive matching
        sentence_lower = text.lower()
        
        # Check if any word from list1 is in the sentence
        if any(word in sentence_lower for word in list1):
            return "Completed"
        # Check if any word from list2 is in the sentence
        elif any(word in sentence_lower for word in list2):
            return "Cancelled"
        else:
            return "Upcoming"
        

    def landmarks(self, text):
        list1 = ["restaurants", "restaurant", "food", "lunch", "dinner", "brunch", "breakfast", "dhaba", "tea", ]
        list2 = ["hotel", "hotels", "stays", "stay", "aasharam", "aasharams", "dharamshala", "guest room", "pg", "resorts", "room", "rooms", "tents", "tent", "coffee"]
        list3 = ["hospital", "first aid", "emergency", "doctor", "nurse", "hospitals", "medical", "medicals", "ambulance"]
        list4 = ["shopping", "shops", "mall", "kirana", "clothes", "cloth", "dress"]

        # Convert the sentence to lowercase to ensure case-insensitive matching
        sentence_lower = text.lower()
        
        # Check if any word from list1 is in the sentence
        if any(word in sentence_lower for word in list1):
            return "Restaurants"
        # Check if any word from list2 is in the sentence
        elif any(word in sentence_lower for word in list2):
            return "Hotels"
        # Check if any word from list3 is in the sentence
        elif any(word in sentence_lower for word in list3):
            return "Hospital"
        # Check if any word from list4 is in the sentence
        elif any(word in sentence_lower for word in list4):
            return "Shopping"

    def sub_events(self, text):
        list1 = ["heritage"]
        list2 = ["spiritual"]
        list3 = ["pilgrimage"]
        list4 = ["kumbh events", "kumbh"]
        list5 = ["tourist", "foreigner", "foreign"]
        list6 = ["shahi snan", "snan", "snaan" ]

        # Convert the sentence to lowercase to ensure case-insensitive matching
        sentence_lower = text.lower()
        
        # Check if any word from list1 is in the sentence
        if any(word in sentence_lower for word in list1):
            return "Heritage"
        # Check if any word from list2 is in the sentence
        elif any(word in sentence_lower for word in list2):
            return "Spritual"
        # Check if any word from list3 is in the sentence
        elif any(word in sentence_lower for word in list3):
            return "Pilgrimage"
        
        # Check if any word from list4 is in the sentence
        elif any(word in sentence_lower for word in list4):
            return "Kumbh Events"
        
        # Check if any word from list5 is in the sentence
        elif any(word in sentence_lower for word in list5):
            return "Tourist"
        
        else:
            return "Shahi Snaan"
