from werkzeug.security import generate_password_hash

def _generate_password(password):
    return generate_password_hash(password)