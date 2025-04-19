import os
from flask import Flask, request, jsonify

# Initialize Flask app for Render
app = Flask(__name__, static_folder='www')

# Define global variables used by the original app
ASSISTANT_NAME = os.environ.get('ASSISTANT_NAME', 'Y.U.Z.I')

# Import hugchat for chat functionality
try:
    from hugchat import hugchat
    
    def get_hugchat_response(query):
        try:
            # Try to use cookies.json if available
            cookies_path = os.path.join('engine', 'cookies.json')
            if os.path.exists(cookies_path):
                chatbot = hugchat.ChatBot(cookie_path=cookies_path)
                id = chatbot.new_conversation()
                chatbot.change_conversation(id)
                
                # Set up as a helpful assistant
                system_message = "You are a helpful assistant named Y.U.Z.I that provides concise answers in exactly 2-3 lines total."
                chatbot.chat(system_message)
                
                # Get response
                message_obj = chatbot.chat(query)
                message_obj.wait_until_done()
                return message_obj.get_final_text()
            else:
                return "HugChat cookies not available. Please configure the secret file in Render."
        except Exception as e:
            return f"Error with HugChat: {str(e)}"
except ImportError:
    def get_hugchat_response(query):
        return "HugChat module not available."

@app.route('/')
def index():
    return "Yuzi Backend API is running! Access web interface for full functionality."

@app.route('/static/<path:path>')
def serve_static(path):
    return app.send_static_file(path)

@app.route('/api/command', methods=['POST'])
def process_command():
    query = request.json.get('command', '')
    
    # Process based on command type
    response = "Command processed."
    
    # For opening applications - just return a message
    if query.lower().startswith('open'):
        app_name = query.lower().replace('open', '').strip()
        response = f"The command to open {app_name} was received, but cannot be executed in cloud environment."
    
    # For playing YouTube - return a message
    elif "on youtube" in query.lower():
        search_term = query.lower().replace('play', '').replace('on youtube', '').strip()
        response = f"The command to play '{search_term}' on YouTube was received."
    
    # For general questions - use HugChat
    else:
        response = get_hugchat_response(query)
    
    return jsonify({
        "status": "success", 
        "response": response,
        "environment": "cloud"
    })

@app.route('/healthcheck')
def healthcheck():
    """Health check endpoint for Render"""
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    # For local development
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port) 