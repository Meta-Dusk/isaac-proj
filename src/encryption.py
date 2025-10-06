from cryptography.fernet import Fernet

def fernet_generate_key() -> str:
    """
    Generate a new random key for Fernet.
    Save this key somewhere safe (not in source code).
    """
    key = Fernet.generate_key()
    return key.decode("utf-8")


def fernet_encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt plaintext with a given Fernet key (base64 urlsafe key string).
    Returns a base64-encoded token (utf-8 string).
    """
    f = Fernet(key.encode("utf-8"))
    token = f.encrypt(plaintext.encode("utf-8"))
    return token.decode("utf-8")


def fernet_decrypt(token: str, key: str) -> str:
    """
    Decrypt a Fernet token and return the original plaintext string.
    Raises cryptography.fernet.InvalidToken if key/token invalid.
    """
    f = Fernet(key.encode("utf-8"))
    plaintext = f.decrypt(token.encode("utf-8"))
    return plaintext.decode("utf-8")


# Example
if __name__ == "__main__":
    key = fernet_generate_key()
    print("Key (store this):", key)
    secret = "this is reversible"
    token = fernet_encrypt(secret, key)
    print("Token:", token)
    recovered = fernet_decrypt(token, key)
    print("Recovered:", recovered)
