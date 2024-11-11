from ..libraries import *

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user, remember=True)
        return jsonify({'message': 'Logged in successfully', 'user': user.email})
    return jsonify({'error': 'Invalid credentials'}), 401

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    new_user = User(email=email, username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return jsonify({'message': 'User created successfully'})

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@auth.route('/user')
def user_info():
    if current_user.is_authenticated:
        return jsonify({'message': 'Logged in',
                        'username': current_user.username,
                        'id': current_user.id})
    else:
        return jsonify({'error': 'Not logged in'}), 400


@auth.route('/get_user/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    if user:
        return jsonify({'name': user.username,
                        'id': user.id,
                        "playlists": [playlist.id for playlist in user.playlists
                                      if (user == current_user) or (not playlist.is_private)],
                        "audios": [audio.id for audio in user.audios
                                    if (user == current_user) or (not audio.is_private)],
                        "listens": user.listens,            
                                    })  
    else:
        return jsonify({'error': 'Not logged in'}), 400