import os
import uuid

from flask import (
    Flask,
    request,
    jsonify,
    session,
    send_from_directory,
)

from chatbot_psikologi import CurhatBot

app = Flask(__name__)

app.secret_key = 'super-secret-key-12345'

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# ======================================================
# In-memory bot storage
# ======================================================

bots = {}

# ======================================================
# Frontend dist folder
# ======================================================

UI_DIST = os.path.join(
    os.path.dirname(__file__),
    'CurhatBuddy Mobile App Design',
    'dist'
)

# ======================================================
# Helper
# ======================================================

def create_bot(theme_name='teman_curhat'):
    return {
        'bot': CurhatBot(theme_name=theme_name),
        'theme': theme_name,
    }


def get_session_bot(theme_name='teman_curhat') -> CurhatBot:

    session_id = session.get('session_id')

    # Kalau belum ada session
    if not session_id:

        session_id = str(uuid.uuid4())

        session['session_id'] = session_id

        bots[session_id] = create_bot(theme_name)

        return bots[session_id]['bot']

    # Kalau session hilang dari memory
    if session_id not in bots:

        bots[session_id] = create_bot(theme_name)

        return bots[session_id]['bot']

    bot_data = bots[session_id]

    # Kalau theme berubah
    if bot_data['theme'] != theme_name:

        bots[session_id] = create_bot(theme_name)

    return bots[session_id]['bot']


# ======================================================
# Frontend
# ======================================================

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):

    if not os.path.isdir(UI_DIST):
        return jsonify({
            'error': (
                'Frontend belum dibuild. '
                'Jalankan npm install dan npm run build.'
            )
        }), 404

    full_path = os.path.join(UI_DIST, path)

    if path and os.path.exists(full_path):
        return send_from_directory(UI_DIST, path)

    return send_from_directory(UI_DIST, 'index.html')


# ======================================================
# API START
# ======================================================

@app.route('/api/start', methods=['POST'])
def api_start():

    try:

        data = request.get_json(silent=True) or {}

        theme_name = data.get(
            'theme',
            'teman_curhat'
        )

        bot = get_session_bot(theme_name)

        greeting = bot.get_greeting()

        analysis_available = False

        # SAFE CHECK
        if hasattr(bot, 'is_insight_available'):
            analysis_available = bot.is_insight_available()

        return jsonify({
            'reply': greeting,
            'analysis_available': analysis_available,
        })

    except Exception as e:

        print('ERROR /api/start:', e)

        return jsonify({
            'error': str(e)
        }), 500


# ======================================================
# API CHAT
# ======================================================

@app.route('/api/chat', methods=['POST'])
def api_chat():

    try:

        data = request.get_json(silent=True) or {}

        theme_name = data.get(
            'theme',
            'teman_curhat'
        )

        message = data.get(
            'message',
            ''
        ).strip()

        if not message:
            return jsonify({
                'error': 'Tulis pesan dulu ya.'
            }), 400

        bot = get_session_bot(theme_name)

        reply = bot.process_message(message)

        analysis_available = False

        if hasattr(bot, 'is_insight_available'):
            analysis_available = bot.is_insight_available()

        return jsonify({
            'reply': reply,
            'analysis_available': analysis_available,
        })

    except Exception as e:

        print('ERROR /api/chat:', e)

        return jsonify({
            'error': str(e)
        }), 500


# ======================================================
# API INSIGHT
# ======================================================

@app.route('/api/insight', methods=['GET'])
def api_insight():

    try:

        theme_name = request.args.get(
            'theme',
            'teman_curhat'
        )

        bot = get_session_bot(theme_name)

        if not hasattr(bot, 'get_insight_data'):

            return jsonify({
                'error': (
                    'Bot belum punya method get_insight_data().'
                )
            }), 500

        insight = bot.get_insight_data()

        return jsonify(insight)

    except Exception as e:

        print('ERROR /api/insight:', e)

        return jsonify({
            'error': str(e)
        }), 500


# ======================================================
# API RESET
# ======================================================

@app.route('/api/reset', methods=['POST'])
def api_reset():

    try:

        data = request.get_json(silent=True) or {}

        theme_name = data.get(
            'theme',
            'teman_curhat'
        )

        session_id = session.get('session_id')

        if session_id in bots:
            del bots[session_id]

        bots[session_id] = create_bot(theme_name)

        bot = bots[session_id]['bot']

        greeting = bot.get_greeting()

        analysis_available = False

        if hasattr(bot, 'is_insight_available'):
            analysis_available = bot.is_insight_available()

        return jsonify({
            'reply': greeting,
            'analysis_available': analysis_available,
        })

    except Exception as e:

        print('ERROR /api/reset:', e)

        return jsonify({
            'error': str(e)
        }), 500


# ======================================================
# MAIN
# ======================================================

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )