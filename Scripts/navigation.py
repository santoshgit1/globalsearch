# navigation.py

import re

class Navigation:
    def __init__(self):
        # Define the features and their associated keywords
        self.features = {
            "Contact Us": ["contact", "call", "contact us", "phone", "connect", "contact us", "helpline", "dial"],
            "Dark Mode": ["change mode", "dark mode", "light mode"],
            "Edit profile": ["edit", "name", "my name", "address", "my address", "my aadhar", "aadhar", "my blood group", "blood group", "my date birth", "date birth", "my phone", "phone number", "contact number", "my contact number", "editing", "edited", "edits", "change", "editable", "editor", "profile", "profiles", "profiling", "profiler", "changed", "changing", "changes", "changeable", "changer", "updated", "updating", "updates", "updatable", "updater"],
            "Dashboard": ["dashboard", "dashboards", "main", "mainer", "mainly", "mainland", "mainsail", "mainstay", "overview", "overviews", "overviewed", "overviewing", "overviewer"],
            "Menu": ["menu", "menus", "section", "sections", "sectional", "sectionally", "sectioner"],
            "Itinerary": ["itineary", "plan", "plans", "planning", "schedule", "scheduled", "scheduling"],
            "Smart Snap": ["smart snap"],
            "Wallet": ["wallet", "cash", "payment", "payments"],
            "Settings": ["settings", "preferences", "preferences", "setting", "settings", "change", "configure", "configuration", "configured", "configurer"],
            "Log Out": ["log out", "sign out", "leave"],
            "QR Scanner": ["qr", "qr code", "scanner", "scan", "lost", "found", "return"],
            "Add family": ["add", "adding", "added", "adds", "addition", "additional", "additionally", "family", "group", "groups", "families", "familiar", "familiarity", "familiarize", "member", "members", "membership"],
            "Upload photo": ["upload", "uploads", "uploaded", "uploading", "uploader", "photo", "photos", "photographic", "photographer", "photograph", "image", "images", "imaginable", "imaginary", "imagination", "imaginative"],
            "Calendar": ["calendar", "calendars", "date", "dates", "dated", "dateless", "dateline", "dating", "schedule", "schedules", "scheduled", "scheduler"],
            "Kumbh Attractions": ["nearby attractions", "attractions", "attraction", "kumbh attractions", "kumbh attraction", "maha kumbh attractions", "maha kumbh attraction"],
            "Nearby Places": ["nearby places", "kumbh nearby places", "maha kumbh nearby places", "maha kumbh nearby place", "kumbh nearby place"],
            "Map": ["map", "maps", "mapping", "mapped", "visit nearby", "go nearby", "restaurant", "Diner", "Bistro", "Café", "cafe", "coffee", "tea", "food", "breakfast", "lunch", "dinner", "Eatery", "Grill", "Tavern", "hospital", "hospitals", "medical", "first aid", "medicine", "medicines", "doctor", "doctors", "clinic", "infirmary", "dispensary", "medical", "healthcare", "psychiatric", "physician", "rehabilitation center", "hospice", "navigate", "navigating", "navigated", "navigation", "navigational", "navigator", "location", "locations", "locate", "located", "locating", "locator", "route", "routes", "routed", "routing", "router", "path", "paths", "pathable", "pathless", "shortest", "shorten", "shortened", "shortening", "shortener", "nearby", "nearness", "nearest", "nearer"],
            "App Guide": ["guide", "guides", "guided", "guiding", "guider", "help", "helps", "helped", "helping", "helper", "instruction", "instructions", "instructed", "instructing", "instructor", "use", "uses", "used", "using", "user", "usage", "app", "apps", "application", "applications"],
            "My Booking": ["book", "books", "booked", "my booking", "booking mine", "upcoming bookings", "current booking", "upcoming bookings", "current bookings", "cancelled", "cancel", "complete", "completed", "booking", "booker", "my bus booking", "my buses booking", "my bus bookings", "my travel booking", "my travel bookings", "my train booking", "my train bookings", "my trains booking"],
            "Train booking": ["trip", "trips", "tripper", "tripping", "tripped", "triplicate", "go", "went", "gone", "goes", "going",  "booking", "bookings", "booked", "booker", "travel", "travels", "traveled", "traveling", "traveler", "book", "books", "ticket", "tickets", "ticketed", "ticketing", "ticketer", "trains", "train", "railwaays", "railway"],
            "Bus booking": ["trip", "trips", "tripper", "tripping", "tripped", "triplicate", "go", "went", "gone", "goes", "going",  "booking", "bookings", "booked", "booker", "travel", "travels", "traveled", "traveling", "traveler", "book", "books", "ticket", "tickets", "ticketed", "ticketing", "ticketer", "bus", "buses", "road", "roadways"],
            "Hotels booking": ["go", "went", "gone", "goes", "going",  "booking", "bookings", "booked", "booker", "book", "books", "hotels", "hotel", "restaurants", "restaurant", "resorts", "resort", "hotelier", "hotelry", "reservation", "reservations", "reserved", "reserving", "reserver", "room", "rooms", "roomed"],
            "Flight booking": ["airplane", "air", "airplanes", "over cloud", "flight", "flights", "flighted", "flighty", "trip", "trips", "tripper", "tripping", "tripped", "triplicate", "go", "went", "gone", "goes", "going",  "booking", "bookings", "booked", "booker", "travel", "travels", "traveled", "traveling", "traveler", "book", "books", "ticket", "tickets", "ticketed", "ticketing", "ticketer"],
            "Homestays": ["home", "homestays", "homestay"],
            "Tents": ["tent", "tents"],
            "Event": ["event", "events", "eventful", "evented", "eventide", "evenly", "evenness", "nearby", "upcoming", "upcomingness", "scheduled", "scheduling", "schedules", "scheduler"],
            "Created Events" : ["created", "planed", "existing", "event", "events", "eventful", "evented", "eventide", "evenly", "evenness", "upcoming", "upcomingness", "scheduled", "scheduling", "schedules", "scheduler"],
            "Invited Events" :  ["invited", "called", "event", "events", "eventful", "evented", "eventide", "evenly", "evenness", "upcoming", "upcomingness", "scheduled", "scheduling", "schedules", "scheduler"],
            "Create Event" : ["create", "plan", "invite", "make", "form", "event", "events", "eventful", "evented", "eventide", "evenly", "evenness", "upcoming", "upcomingness", "scheduled", "scheduling", "schedules", "scheduler"],
            "Change language": ["change", "changes", "changed", "changing", "changer", "language", "languages", "languaged", "language-related", "linguistic"],
            "My account": ["account", "accounts", "accounted", "accounting", "accountant", "details", "detailed", "detailing", "detailer"],
            "Notification": ["notification", "notifications", "notified", "notifying", "notifier", "alert", "alerts", "alerted", "alerting", "alerter", "message", "messages", "messaged", "messaging", "messenger"],
            "Join family": ["join", "joins", "joined", "joining", "joiner", "family", "families", "familiar", "familiarity", "familiarize", "group", "groups", "grouped", "grouping", "grouper"],
            "Term and condition": ["term", "terms", "termed", "terminable", "terminal", "condition", "conditions", "conditioned", "conditional", "conditioner"],
            "Privacy policy": ["privacy", "private", "privately", "privatize", "privatization", "policy", "policies", "policed", "policing", "policeman"]
        }
        self.stop_words = set(["a", "an", "the", "is", "show", "me", "tell", "or", "this", "these", "that", "was", "were", "of", "in", "on", "at", "to", "for", "with", "by", "as", "and", "but", "if", "or", "which", "from", "it", "its", "has", "have", "had", "be", "are", "were", "been", "being", "do", "does", "did", "doing", "will", "would", "can", "could", "should", "might", "must"])

    def preprocess_text(self, text):
        # Remove punctuation and convert to lowercase
        text = text.lower()
        text = text.replace(",", "")
        text = text.replace(".", "")
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove stop words
        words = text.split()
        words = [word for word in words if word not in self.stop_words]
        return ' '.join(words)
    

    def find_feature_with_max_match(self, utterance):
        # Preprocess the utterance to remove stop words and punctuation
        utterance = self.preprocess_text(utterance)
        
        # Tokenize the utterance
        utterance_words = set(utterance.split())
        
        # Initialize a dictionary to track match counts for each feature
        match_counts = {feature: 0 for feature in self.features}
        
        # Track the feature with the maximum match count
        max_feature = None
        max_count = 0
        
        for feature, keywords in self.features.items():
            # Initialize match count for the current feature
            match_count = 0
            
            # Check for multi-word phrases
            for keyword in keywords:
                if ' ' in keyword:
                    if keyword in utterance:
                        match_count += 1
                else:
                    if keyword in utterance_words:
                        match_count += 1
            
            # Update match counts and the feature with the maximum match
            if match_count > max_count:
                max_count = match_count
                max_feature = feature
            
            match_counts[feature] = match_count
        
        # Return the feature with the maximum match count
        # return max_feature if max_feature else "No matching feature found"
        return max_feature if max_feature else False
    # def find_feature_with_max_match(self, utterance):
    #     # Preprocess the utterance (convert to lowercase, remove stop words, etc.)
    #     utterance = self.preprocess_text(utterance)
    #     # Split the utterance into words
    #     utterance_words = set(utterance.split())

    #     match_counts = {feature: 0 for feature in self.features}
    #     max_feature = None
    #     max_count = 0

    #     for feature, keywords in self.features.items():
    #         match_count = 0

    #         for keyword in keywords:
    #             if ' ' in keyword:
    #                 # Check for phrases (multi-word keywords)
    #                 if keyword in utterance:
    #                     print(f"Matched Phrase: {keyword}")
    #                     match_count += 1
    #             else:
    #                 # Check for single-word keywords
    #                 if keyword in utterance_words:
    #                     print(f"Matched Word: {keyword}")
    #                     match_count += 1

    #         print(f"Feature: {feature}, Match Count: {match_count}")

    #         # Update max count and feature
    #         if match_count > max_count:
    #             max_count = match_count
    #             max_feature = feature
    #         match_counts[feature] = match_count

    #     return max_feature if max_feature else False


