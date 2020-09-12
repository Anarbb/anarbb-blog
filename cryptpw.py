from passlib.hash import pbkdf2_sha256


class Crypt:
    def encrypt_password(password):
        return pbkdf2_sha256.hash(password)

    def verify_password(password, hashed):
        return pbkdf2_sha256.verify(password, hashed)
