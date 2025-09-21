from flask import Flask, request, jsonify, render_template
import uuid
from chatbot import Chatbot
from database import init_db, log_interaction, get_chat_history


app = Flask(__name__)
chatbot = Chatbot()

# Initialize database
init_db()

@app.route('/')
def index():
    """Serve the chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chatbot interactions"""
    try:
        data = request.json
        user_input = data.get('message', '').strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400

        # Get response from chatbot
        bot_response = chatbot.get_response(user_input)
        
        # Log interaction
        log_interaction(user_input, bot_response, session_id)
        
        return jsonify({
            'response': bot_response,
            'session_id': session_id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def history():
    """Get chat history"""
    try:
        session_id = request.args.get('session_id')
        limit = int(request.args.get('limit', 10))
        
        history = get_chat_history(session_id, limit)
        
        return jsonify({
            'history': [{
                'user_input': row[0],
                'bot_response': row[1],
                'timestamp': row[2]
            } for row in history]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)