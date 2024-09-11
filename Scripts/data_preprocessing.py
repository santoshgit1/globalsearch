# # importing Libraries
# from googletrans import Translator

# class DataPreprocessing:
#     def __init__(self, text_data):
#         """
#         Initialize the DataPreprocessing with the text data.

#         Args:
#             text_data (str): The text data to be processed.
#         """
#         self.text_data = text_data

#     def translate_to_english(self, text):
#         translator = Translator()
#         # Translate text to English
#         translated = translator.translate(text, dest='en')
#         return translated.text

#     def pre_process(self):
#         """
#         Process the text data.

#         This is where you would add text preprocessing steps such as cleaning, tokenization, etc.
#         """

#         # Translate to English
#         translated_text = self.translate_to_english(self.text_data)

#         # Print results
#         print("Original Text:", self.text_data)
#         print("Translated Text:", translated_text)

#         return translated_text







# from deep_translator import GoogleTranslator

# class DataPreprocessing:
#     def __init__(self, text_data):
#         """
#         Initialize the DataPreprocessing with the text data.

#         Args:
#             text_data (str): The text data to be processed.
#         """
#         self.text_data = text_data

#     def translate_to_english(self, text):
#         # Translate text to English using deep_translator
#         translated = GoogleTranslator(source='auto', target='en').translate(text)
#         return translated

#     def pre_process(self):
#         """
#         Process the text data.

#         This is where you would add text preprocessing steps such as cleaning, tokenization, etc.
#         """
#         # Translate to English
#         translated_text = self.translate_to_english(self.text_data)

#         # Print results
#         # print("Original Text:", self.text_data)
#         # print("Translated Text:", translated_text)

#         return translated_text





















# data_preprocessing.py

try:
    from googletrans import Translator
    GOOGLE_TRANS_AVAILABLE = True
except ImportError:
    GOOGLE_TRANS_AVAILABLE = False

from deep_translator import GoogleTranslator

class DataPreprocessing:
    def __init__(self, text_data):
        """
        Initialize the DataPreprocessing with the text data.

        Args:
            text_data (str): The text data to be processed.
        """
        self.text_data = text_data

    def translate_to_english(self, text):
        if GOOGLE_TRANS_AVAILABLE:
            try:
                # Use googletrans for translation
                translator = Translator()
                translated = translator.translate(text, dest='en')
                return translated.text
            except Exception as e:
                print(f"Googletrans failed: {e}")
                # Fall back to deep_translator
                return self.fallback_translation(text)
        else:
            # If googletrans is not available, use deep_translator
            return self.fallback_translation(text)

    def fallback_translation(self, text):
        try:
            # Use deep_translator for translation
            translated = GoogleTranslator(source='auto', target='en').translate(text)
            return translated
        except Exception as e:
            print(f"Deep_translator failed: {e}")
            return text  # Return the original text if both translators fail

    def pre_process(self):
        """
        Process the text data.

        This is where you would add text preprocessing steps such as cleaning, tokenization, etc.
        """
        # Translate to English
        translated_text = self.translate_to_english(self.text_data)

        # Print results
        # print("Original Text:", self.text_data)
        # print("Translated Text:", translated_text)

        return translated_text
