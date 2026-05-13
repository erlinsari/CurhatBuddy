import os
from flask import Flask, request, jsonify, session, send_from_directory
from chatbot_psikologi import CurhatBot
import uuid

app = Flask(__name__)
app.secret_key = 'super-secret-key-12345'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

bots = {}

UI_DIST = os.path.join(os.path.dirname(__file__), 'CurhatBuddy Mobile App Design', 'dist')


def get_session_bot(theme_name: str = 'teman_curhat') -> CurhatBot:
    session_id = session.get('session_id')
    if session_id is None or session_id not in bots:
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        bots[session_id] = {
            'bot': CurhatBot(theme_name=theme_name),
            'theme': theme_name,
        }
    else:
        bot_data = bots.get(session_id)
        if bot_data is None or bot_data['theme'] != theme_name:
            bots[session_id] = {
                'bot': CurhatBot(theme_name=theme_name),
                'theme': theme_name,
            }
    return bots[session_id]['bot']


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path: str):
    if os.path.isdir(UI_DIST):
        if path != '' and os.path.exists(os.path.join(UI_DIST, path)):
            return send_from_directory(UI_DIST, path)
        return send_from_directory(UI_DIST, 'index.html')
    return jsonify({'error': 'Frontend belum dibuild. Jalankan npm install dan npm run build di folder CurhatBuddy Mobile App Design.'}), 404


@app.route('/api/start', methods=['POST'])
def api_start():
    data = request.get_json() or {}
    theme_name = data.get('theme', 'teman_curhat')
    bot = get_session_bot(theme_name)
    greeting = bot.get_greeting()
    return jsonify({'reply': greeting, 'analysis_available': bot.is_insight_available()})


@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json() or {}
    theme_name = data.get('theme', 'teman_curhat')
    message = data.get('message', '').strip()

    if not message:
        return jsonify({'error': 'Tulis pesan dulu ya.'}), 400

    bot = get_session_bot(theme_name)
    reply = bot.process_message(message)
    return jsonify({'reply': reply, 'analysis_available': bot.is_insight_available()})


@app.route('/api/insight', methods=['GET'])
def api_insight():
    theme_name = request.args.get('theme', 'teman_curhat')
    bot = get_session_bot(theme_name)
    insight = bot.get_insight_data()
    return jsonify(insight)


@app.route('/api/reset', methods=['POST'])
def api_reset():
    data = request.get_json() or {}
    theme_name = data.get('theme', 'teman_curhat')
    session_id = session.get('session_id')
    if session_id in bots:
        del bots[session_id]
    bot = get_session_bot(theme_name)
    greeting = bot.get_greeting()
    return jsonify({'reply': greeting, 'analysis_available': bot.is_insight_available()})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
