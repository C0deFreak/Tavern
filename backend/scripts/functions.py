from flask_login import current_user
from flask import jsonify
import os

# OPTIMIZATION
# Variabla koja drži popis administratorovih email adresa
email_addresses = []
# Putanja do datoteke koja sadrži popis admin emailova
ADMIN_LIST = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'admin_list.txt')

# Funkcija koja provjerava privatnost predmeta i vraća odgovarajući odgovor
def check_private(item, safe, not_safe={"error": "Item is private"}):
    # Provjerava je li predmet privatni i ako korisnik nije autentificiran ili nije vlasnik predmeta
    if item.is_private and (not current_user.is_authenticated or item.user_id != current_user.id):
        if not_safe == {"error": "Item is private"}:
            return jsonify(not_safe), 400  # Vraća poruku o privatnosti ako je predmet privatni
        else:
            return not_safe  # Vraća custom not_safe odgovor
    else:
        return safe  # Ako predmet nije privatni, vraća siguran odgovor

# Funkcija za pretvaranje JavaScript bool vrijednosti u Python bool
def js_bool_to_py(translate):
    if translate == 'true':
        return True  # Ako je vrijednost 'true', vraća True
    else:
        return False  # Inače, vraća False
        
# Funkcija koja učitava admin emailove iz datoteke
def return_admin_emails():
    # Ako datoteka ne postoji, stvara je i dodaje početni admin email
    if not os.path.exists(ADMIN_LIST):
        with open(ADMIN_LIST, "w") as file:
            file.write('grgur@gm.com')

    # Učitava sve emailove iz datoteke u listu email_addresses
    with open(ADMIN_LIST, "r") as file:
        for line in file:
            email = line.strip()  # Uklanja suvišne razmake
            if email:  # Provjerava nije li linija prazna
                email_addresses.append(email)  # Dodaje email u listu
