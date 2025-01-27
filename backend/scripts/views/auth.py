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
    name = data.get('name')
    password = data.get('password')

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    return_admin_emails()
    new_user = User(email=email, name=name, password=generate_password_hash(password), admin= True if email in email_addresses else False)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    return jsonify({'message': 'User created successfully'})

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@auth.route('/user_check')
def check_current_user():
    if current_user.is_authenticated:
        return jsonify({'message': 'Logged in',
                        'name': current_user.name,
                        'id': current_user.id,
                        'admin': current_user.admin})
    else:
        return jsonify({'error': 'Not logged in'}), 400


@auth.route('/info/<int:id>', methods=['GET'])
def get_any_user(id):
    user = User.query.get_or_404(id)
    if user:
        return jsonify({'name': user.name,
                        'id': user.id,
                        "playlists": [playlist.id for playlist in user.playlists
                                      if (user == current_user) or (not playlist.is_private)],
                        "audios": [audio.id for audio in user.audios
                                    if (user == current_user) or (not audio.is_private)],
                        "followed": [followed.id for followed in user.followed],
                        "listens": user.overall_listens, 
                        "followers": user.follower_count,
                        "is_following": current_user.is_authenticated and current_user in user.followers        
                                    })  

    else:
        return jsonify({'error': 'User not found'}), 404


@auth.route('/follow/<int:id>', methods=['POST'])
def follow_user(id):
    user = User.query.get_or_404(id)
    if user:
        if user not in current_user.followed:
            current_user.followed.append(user)
            user.followers.append(current_user)
            user.follower_count += 1
            user.notifications.append(Notification(context=f"{current_user.name} followed you!", link=f"{'-'.join((current_user.name).split())}_userid_{current_user.id}", date=datetime.now()))
            db.session.commit()
            return jsonify({'message': 'Followed successfully'})
        else:
            current_user.followed.remove(user)
            user.followers.remove(current_user)
            user.follower_count -= 1
            db.session.commit()
            return jsonify({'message': 'Unfollowed successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404
    

@auth.route('/notifications', methods=['GET'])
@login_required
def notifications():
    print(current_user.notifications)
    return jsonify({"context": [notify.context for notify in current_user.notifications],
                    "link": [notify.link for notify in current_user.notifications],
                    "date": [notify.date for notify in current_user.notifications]})