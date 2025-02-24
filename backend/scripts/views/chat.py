from ..libraries import *


#SETUP
chat_views = Blueprint('chat', __name__)

# PLAYLISTS
# Creates the playlists
@chat_views.route('/create', methods=['POST'])
@login_required
def make_playlist():
    private = js_bool_to_py(request.form.get('private'))

    new_chat = Chat(host=current_user, is_private=private)
    db.session.add(new_chat)
    db.session.commit()

    return jsonify({"success": "Chat made"}), 200

