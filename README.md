# Chatbot Application
This project is a Flask-based chatbot application that leverages spaCy for natural language processing. The chatbot can handle various intents, including greeting users, checking order statuses, providing product information, explaining return policies, and more.

## Features
- Greeting: Responds to greetings.
- Order Status: Checks the status of an order using a provided order number.
- Return Policy: Provides details about the return policy.
- Product Information: Gives information about different products.
- Shipping Information: Provides shipping details.
- Goodbye: Ends the conversation politely.
- Contextual Understanding: Remembers context within a session to provide relevant responses.

## Dependencies
- Flask
- spaCy
- re (Regular Expressions)

## Intents and Responses
The chatbot can recognize and respond to the following intents:
- Greeting
- Order Status
- Provide Order Number
- Return
- Product Information
- Shipping Information
- Return Policy Details
- Goodbye
- Specific Product Information (e.g., laptops, phones)
- Specific Laptop Information (e.g., gaming laptops, business laptops)

## Installation
1. Clone the repository:
-  git clone<repository-url>
- cd repository-directory>

2. Install the dependencies:
- Download the spaCy model:
- python -m spacy download en_core_web_sm


## Usage
1. Run the Flask application:
- python chatbot.py
2. Access the application:
Open your web browser and go to http://127.0.0.1:5000/.
3. Interact with the chatbot:
Use the chat interface to send messages and receive responses.

## Contributing
- Contributions are welcome! Please fork the repository and submit pull requests with your enhancements.
