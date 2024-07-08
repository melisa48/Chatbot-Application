from flask import Flask, request, jsonify, render_template
import re
import spacy

app = Flask(__name__)

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Define intents and responses
intents = {
    'greeting': ['hello', 'hi', 'hey'],
    'order_status': ['order', 'status', 'track'],
    'provide_order_number': [r'\b\d{10}\b'],  # Matches a 10-digit number
    'return': ['return', 'refund', 'exchange'],
    'product_info': ['product', 'information', 'details'],
    'shipping_info': ['shipping', 'delivery', 'shipment', 'how long', 'take'],
    'return_policy_details': ['more information', 'tell me more', 'yes', 'please'],
    'goodbye': ['bye', 'goodbye', 'see you', 'no more questions'],
    'specific_product_info': ['laptops', 'phones', 'ipad', 'computers', 'cameras', 'speakers'],
    'specific_laptop_info': ['gaming laptops', 'ultrabooks', 'business laptops']
}

responses = {
    'greeting': "Hello! How can I assist you today?",
    'order_status': "To check your order status, please provide your order number.",
    'provide_order_number': "Thank you for providing your order number. Your order {order_number} is currently being processed and will be shipped within 2-3 business days.",
    'return': "Our return policy allows returns within 30 days of purchase. Would you like more information?",
    'product_info': "I'd be happy to provide product information. What specific product are you interested in? We offer laptops, phones, iPads, computers, cameras, and speakers.",
    'shipping_info': "Our standard shipping takes 5-7 business days. Express shipping is available within 2-3 business days.",
    'return_policy_details': "You can return items within 30 days of purchase for a full refund. Items must be in original condition with all tags and packaging intact. Please contact our support team to initiate a return.",
    'goodbye': "Thank you for chatting with us. Have a great day!",
    'default': "I'm sorry, I didn't understand that. Could you please rephrase your question?",
    'invalid_order_number': "I'm sorry, I couldn't find a valid order number. Please provide a 10-digit order number.",
    'specific_laptop_info': "We offer a variety of laptops including gaming laptops, ultrabooks, and business laptops. What specific laptop are you interested in?",
    'business_laptop_info': "Our business laptops are designed for productivity, with robust security features, powerful processors, and durable build quality."
}

# To store the current context and conversation memory
user_sessions = {}

def classify_intent(text, awaiting_return_info=False, awaiting_specific_product_info=False):
    text = text.lower()
    if any(word in text for word in intents['shipping_info']):
        return 'shipping_info'
    if any(word in text for word in intents['goodbye']):
        return 'goodbye'
    if awaiting_return_info and any(word in text for word in ['yes', 'more', 'please', 'tell']):
        return 'return_policy_details'
    if awaiting_specific_product_info:
        if 'laptop' in text:
            return 'specific_laptop_info'
        for product in intents['specific_product_info']:
            if product in text:
                return 'specific_product_info'
    for intent, patterns in intents.items():
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
            return intent
    return 'default'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST', 'GET'])
def chat():
    if request.method == 'POST':
        user_message = request.json['message']
        user_id = request.json['user_id']

        # Initialize session if it doesn't exist
        if user_id not in user_sessions:
            user_sessions[user_id] = {
                'awaiting_order_number': False,
                'order_number': None,
                'awaiting_return_info': False,
                'awaiting_specific_product_info': False,
                'product_type': None
            }

        session = user_sessions[user_id]
        intent = classify_intent(user_message, session['awaiting_return_info'], session['awaiting_specific_product_info'])

        if session['awaiting_order_number']:
            order_number = re.search(r'\b\d{10}\b', user_message)
            if order_number:
                session['awaiting_order_number'] = False
                session['order_number'] = order_number.group()
                response = responses['provide_order_number'].format(order_number=session['order_number'])
            else:
                response = responses['invalid_order_number']
        elif session['awaiting_specific_product_info']:
            if 'business laptop' in user_message.lower():
                session['awaiting_specific_product_info'] = False
                response = responses['business_laptop_info']
            else:
                response = responses['specific_laptop_info']
        elif intent == 'return':
            session['awaiting_return_info'] = True
            response = responses['return']
        elif intent == 'return_policy_details':
            session['awaiting_return_info'] = False
            response = responses['return_policy_details']
        elif intent == 'order_status':
            session['awaiting_order_number'] = True
            response = responses['order_status']
        elif intent == 'product_info' or intent == 'specific_product_info':
            session['awaiting_specific_product_info'] = True
            response = responses['product_info']
        elif intent == 'specific_laptop_info':
            session['awaiting_specific_product_info'] = True
            response = responses['specific_laptop_info']
        else:
            response = responses[intent]

        return jsonify({'response': response})
    return jsonify({'response': 'Please send a POST request with a message.'})

if __name__ == '__main__':
    app.run(debug=True)

