from flask import jsonify
from flask_login import current_user


# OPTIMIZATION
# Functions that shorten the repeated code
def check_private(item, safe, not_safe={"error": "Item is private"}):
    if item.is_private and (not current_user.is_authenticated or item.user_id != current_user.id):
        if not_safe == {"error": "Item is private"}:
            return jsonify(not_safe), 400
        else:
            return not_safe
    else:
        return safe
    
def js_bool_to_py(translate):
    if translate == 'true':
            return True
    else:
        return False
        

