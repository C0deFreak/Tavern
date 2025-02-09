from flask_login import current_user
from flask import jsonify
import os

# OPTIMIZATION
#Variables
email_addresses = []
ADMIN_LIST = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'admin_list.txt')

# Functions that shorten the repeated code
def check_private(item, safe, not_safe={"error": "Item is private"}):
    print(current_user)
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
        
def return_admin_emails():
    if not os.path.exists(ADMIN_LIST):
        with open(ADMIN_LIST, "w") as file:
            file.write('grgur@gm.com')

    with open(ADMIN_LIST, "r") as file:
        for line in file:
            email = line.strip()  # Remove any extra whitespace
            if email:  # Ensure it's not an empty line
                email_addresses.append(email)
    
