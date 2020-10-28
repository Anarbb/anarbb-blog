from passlib.hash import pbkdf2_sha256


class Crypt:
    # Encrypts the passwrod using pbkdf2
    def encrypt_password(password):
        return pbkdf2_sha256.hash(password)
    # Checks if the hash matches the provided password

    def verify_password(password, hashed):
        return pbkdf2_sha256.verify(password, hashed)
