from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
from typing import List, Dict, Optional
import threading
import os

app = Flask(__name__, static_folder='static')
CORS(app)

messages: List[Dict] = []
messages_lock = threading.Lock()
message_id_counter = 0

MAX_MESSAGES = 1000

def add_message(player_name: str, message_text: str, is_auto_reply: bool = False) -> Dict:
    global message_id_counter
    with messages_lock:
        message_id_counter += 1
        message = {
            'id': message_id_counter,
            'player_name': player_name,
            'message': message_text,
            'timestamp': datetime.utcnow().isoformat(),
            'is_auto_reply': is_auto_reply
        }
        messages.append(message)
        
        if len(messages) > MAX_MESSAGES:
            messages.pop(0)
        
        return message

@app.route('/')
def home():
    return send_from_directory('static', 'test.html')

@app.route('/api')
def api_info():
    return jsonify({
        'status': 'online',
        'server': 'Roblox Messaging Server',
        'endpoints': {
            'POST /api/send': 'Send a message',
            'GET /api/messages': 'Get all messages',
            'GET /api/messages/<player_name>': 'Get messages for a specific player',
            'POST /api/clear': 'Clear all messages'
        }
    })

@app.route('/api/send', methods=['POST'])
def send_message():
    data = request.get_json()
    
    if not data or 'player_name' not in data or 'message' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing required fields: player_name and message'
        }), 400
    
    player_name = data['player_name']
    message_text = data['message']
    
    user_message = add_message(player_name, message_text, is_auto_reply=False)
    
    auto_reply_text = f"Hello {player_name}!"
    auto_reply = add_message('Server', auto_reply_text, is_auto_reply=True)
    
    return jsonify({
        'success': True,
        'message': user_message,
        'auto_reply': auto_reply
    }), 201

@app.route('/api/messages', methods=['GET'])
def get_messages():
    limit = request.args.get('limit', type=int)
    since = request.args.get('since', type=str)
    
    with messages_lock:
        filtered_messages = messages.copy()
    
    if since:
        try:
            since_time = datetime.fromisoformat(since)
            filtered_messages = [
                msg for msg in filtered_messages
                if datetime.fromisoformat(msg['timestamp']) > since_time
            ]
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid timestamp format. Use ISO format (e.g., 2025-11-22T10:30:00)'
            }), 400
    
    if limit and limit > 0:
        filtered_messages = filtered_messages[-limit:]
    
    return jsonify({
        'success': True,
        'count': len(filtered_messages),
        'messages': filtered_messages
    })

@app.route('/api/messages/<player_name>', methods=['GET'])
def get_player_messages(player_name: str):
    limit = request.args.get('limit', type=int)
    
    with messages_lock:
        player_messages = [
            msg for msg in messages
            if msg['player_name'].lower() == player_name.lower()
        ]
    
    if limit and limit > 0:
        player_messages = player_messages[-limit:]
    
    return jsonify({
        'success': True,
        'player_name': player_name,
        'count': len(player_messages),
        'messages': player_messages
    })

@app.route('/api/clear', methods=['POST'])
def clear_messages():
    global message_id_counter
    with messages_lock:
        messages.clear()
        message_id_counter = 0
    
    return jsonify({
        'success': True,
        'message': 'All messages cleared'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
