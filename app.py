# # app.py

# from flask import Flask, request, jsonify, render_template
# from main import Main  # Import the Main class from main.py

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         input_text = request.form['text']
#         main_instance = Main(text_data=input_text)
#         result = main_instance.process_text_data()
#         return jsonify(result)
#     return render_template('index.html')

# if __name__ == '__main__':
#     # app.run(port=9090, debug=True)
#     app.run(debug=True) 










# from flask import Flask, request, jsonify, render_template
# from main import Main  # Import the Main class from main.py

# app = Flask(__name__)

# # Route for sending requests via Postman (or any API client)
# @app.route('/api/process', methods=['POST'])
# def process_text_api():
#     data = request.get_json()
#     input_text = data.get('text', '')  # Extract 'text' from JSON payload
#     main_instance = Main(text_data=input_text)
#     result = main_instance.process_text_data()
#     return jsonify(result)

# # Route for the web form
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         input_text = request.form['text']
#         main_instance = Main(text_data=input_text)
#         result = main_instance.process_text_data()
#         return jsonify(result)
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
#     # app.run(debug=True)







# # without async

# from flask import Flask, request, jsonify, render_template
# from main import Main  # Import the Main class from main.py
# import logging
# import os

# app = Flask(__name__)

# # Ensure the log directory exists
# if not os.path.exists('logs'):
#     os.makedirs('logs')

# # Set up logging
# # Set up logging for main.py
# logging.basicConfig(
#     filename='logs/main.log',  # Log file path
#     level=logging.INFO,        # Log level (INFO, DEBUG, ERROR, etc.)
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# # Route for sending requests via Postman (or any API client)
# @app.route('/api/process', methods=['POST'])
# def process_text_api():
#     data = request.get_json()
#     input_text = data.get('text', '')  # Extract 'text' from JSON payload

    
#     logging.info(f"API request received with text: {input_text}")

#     main_instance = Main(text_data=input_text)
#     result = main_instance.process_text_data()

#     logging.info(f"Processed result: {result}")

#     return jsonify(result)

# # Route for the web form
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         input_text = request.form['text']

#         logging.info(f"Form submission received with text: {input_text}")

#         main_instance = Main(text_data=input_text)
#         result = main_instance.process_text_data()

#         logging.info(f"Processed result: {result}")

#         return jsonify(result)

#     return render_template('index.html')

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)


















# with async

from flask import Flask, request, jsonify, render_template
from main import Main  # Import the Main class from main.py
import logging
import os
import asyncio

app = Flask(__name__)

# Ensure the log directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up logging for main.py
logging.basicConfig(
    filename='logs/main.log',  # Log file path
    level=logging.INFO,        # Log level (INFO, DEBUG, ERROR, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Route for sending requests via Postman (or any API client) asynchronously
@app.route('/api/process', methods=['POST'])
async def process_text_api():
    data = await request.get_json()  # Use 'await' to fetch JSON payload asynchronously
    input_text = data.get('text', '')  # Extract 'text' from JSON payload

    logging.info(f"API request received with text: {input_text}")

    # Use asyncio to run the text processing asynchronously
    result = await asyncio.to_thread(run_main_process, input_text)

    logging.info(f"Processed result: {result}")

    return jsonify(result)

# Route for the web form asynchronously
@app.route('/', methods=['GET', 'POST'])
async def index():
    if request.method == 'POST':
        input_text = request.form['text']

        logging.info(f"Form submission received with text: {input_text}")

        # Use asyncio to run the text processing asynchronously
        result = await asyncio.to_thread(run_main_process, input_text)

        logging.info(f"Processed result: {result}")

        return jsonify(result)

    return render_template('index.html')

def run_main_process(input_text):
    """Helper function to handle synchronous processing in an async manner."""
    main_instance = Main(text_data=input_text)
    return main_instance.process_text_data()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
