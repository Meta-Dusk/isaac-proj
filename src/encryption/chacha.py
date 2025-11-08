from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
import os

# --- Helper Function for Key Derivation ---
def derive_key(password: str, salt: bytes) -> bytes:
    """Derives a secure 32-byte (256-bit) key from a password and salt using HKDF."""
    # HKDF (HMAC-based Key Derivation Function) is used to safely derive a cryptographic key
    # from a user-provided password, ensuring the key is exactly 32 bytes long.
    kdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32, # ChaCha20 requires a 256-bit (32-byte) key
        salt=salt,
        info=b'chacha20-encryption-context',
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_chacha20(plaintext: str, password: str, associated_data: bytes = None):
    """
    Encrypts data using ChaCha20-Poly1305.

    :param plaintext: The string to encrypt.
    :param password: The secret password used to derive the encryption key.
    :param associated_data: Optional non-secret data to authenticate (e.g., file name).
    :return: Tuple containing (salt, nonce, ciphertext)
    """
    # 1. Generate unique salt and nonce
    salt = os.urandom(16)      # 16 bytes is standard for salt
    nonce = os.urandom(12)     # 12 bytes is required for ChaCha20-Poly1305

    # 2. Derive the key from the password and salt
    key = derive_key(password, salt)

    # 3. Create the AEAD cipher instance
    aead = ChaCha20Poly1305(key)

    # 4. Encrypt (Poly1305 tag is automatically appended to the ciphertext)
    # The associated_data is authenticated but not encrypted.
    ciphertext = aead.encrypt(
        nonce,
        plaintext.encode('utf-8'),
        associated_data if associated_data else b''
    )

    return salt, nonce, ciphertext

def decrypt_chacha20(salt: bytes, nonce: bytes, ciphertext: bytes, password: str, associated_data: bytes = None) -> str:
    """
    Decrypts data using ChaCha20-Poly1305 and verifies authenticity.

    :param salt: The salt used during encryption.
    :param nonce: The nonce used during encryption.
    :param ciphertext: The encrypted data (includes the Poly1305 tag).
    :param password: The secret password used to derive the key.
    :param associated_data: Optional non-secret data used during encryption.
    :return: The decrypted plaintext string.
    :raises cryptography.exceptions.InvalidTag: If the ciphertext or associated data was tampered with.
    """
    # 1. Re-derive the key using the same password and salt
    key = derive_key(password, salt)

    # 2. Create the AEAD cipher instance
    aead = ChaCha20Poly1305(key)

    try:
        # 3. Decrypt (authenticity is verified automatically via the Poly1305 tag)
        plaintext_bytes = aead.decrypt(
            nonce,
            ciphertext,
            associated_data if associated_data else b''
        )
        return plaintext_bytes.decode('utf-8')
    except Exception as e:
        # Catch InvalidTag or other potential decryption errors
        return f"Decryption Error (Invalid Key or Tampered Data): {e}"


# --- Demonstration ---
if __name__ == '__main__':

    SECRET_PASSWORD = "MySuperSecurePassword123"
    MESSAGE = "ChaCha20 is a powerful stream cipher, great for high-speed encryption."

    # Example of non-secret data that should be authenticated (like a file header)
    AUTH_DATA = b"metadata-for-file-transfer-v1.0"

    print(f"Original Message: {MESSAGE}\n")

    # ENCRYPTION
    salt_out, nonce_out, ciphertext_out = encrypt_chacha20(MESSAGE, SECRET_PASSWORD, associated_data=AUTH_DATA)

    print("--- ENCRYPTION SUCCESSFUL ---")
    print(f"Salt (to be stored): {salt_out.hex()}")
    print(f"Nonce (to be stored): {nonce_out.hex()}")
    print(f"Ciphertext (with Poly1305 Tag): {ciphertext_out.hex()}")
    print(f"Authenticated Data: {AUTH_DATA.decode()}\n")

    # DECRYPTION (Successful case)
    decrypted_message = decrypt_chacha20(salt_out, nonce_out, ciphertext_out, SECRET_PASSWORD, associated_data=AUTH_DATA)

    print("--- DECRYPTION SUCCESSFUL ---")
    print(f"Decrypted Message: {decrypted_message}\n")

    # DECRYPTION (Failure case: Tampered Ciphertext)
    print("--- TESTING INTEGRITY FAILURE ---")
    # Simulate a single byte flip in the ciphertext
    tampered_ciphertext = ciphertext_out[:-1] + b'\x00'

    failed_decryption = decrypt_chacha20(salt_out, nonce_out, tampered_ciphertext, SECRET_PASSWORD, associated_data=AUTH_DATA)

    print(f"Decryption Attempt with Tampered Ciphertext: {failed_decryption}")
    print("Expected: Decryption Error (Invalid Key or Tampered Data) - This shows Poly1305 integrity check worked.")