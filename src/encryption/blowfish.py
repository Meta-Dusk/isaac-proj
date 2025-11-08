from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os

# Blowfish has an 8-byte block size
BLOCK_SIZE = Blowfish.block_size

def encrypt_blowfish(plaintext: str, key: bytes):
    """
    Encrypts data using Blowfish in CBC mode with PKCS7 padding.

    :param plaintext: The string to encrypt.
    :param key: The secret encryption key (between 4 and 56 bytes).
    :return: Tuple containing (initialization_vector, ciphertext)
    """
    # 1. Generate a unique Initialization Vector (IV)
    # CBC mode requires an IV equal to the block size (8 bytes for Blowfish)
    iv = os.urandom(BLOCK_SIZE)

    # 2. Create the cipher object
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)

    # 3. Apply padding to ensure plaintext length is a multiple of BLOCK_SIZE
    padded_data = pad(plaintext.encode('utf-8'), BLOCK_SIZE)

    # 4. Encrypt the padded data
    ciphertext = cipher.encrypt(padded_data)

    # Return the IV and the ciphertext (both needed for decryption)
    return iv, ciphertext

def decrypt_blowfish(iv: bytes, ciphertext: bytes, key: bytes):
    """
    Decrypts data using Blowfish in CBC mode.

    :param iv: The Initialization Vector used during encryption.
    :param ciphertext: The encrypted data.
    :param key: The secret encryption key.
    :return: The decrypted plaintext string.
    """
    # 1. Create the cipher object using the same key, mode, and IV
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)

    # 2. Decrypt the ciphertext
    decrypted_padded_data = cipher.decrypt(ciphertext)

    # 3. Unpad the decrypted data and decode back to a string
    try:
        plaintext_bytes = unpad(decrypted_padded_data, BLOCK_SIZE)
        return plaintext_bytes.decode('utf-8')
    except ValueError:
        # This occurs if the padding is invalid (e.g., wrong key used)
        return "Decryption Error: Invalid padding (likely wrong key or tampered data)."


# --- Demonstration ---
if __name__ == '__main__':

    # 1. Setup the key and message
    # Blowfish key length is variable; using 16 bytes (128 bits) here.
    SECRET_KEY = get_random_bytes(16)
    MESSAGE = "Blowfish is a fast and simple cipher developed by Bruce Schneier."

    print(f"Original Message: {MESSAGE}")
    print(f"Secret Key (16 bytes): {SECRET_KEY.hex()}\n")

    # ENCRYPTION
    iv_out, ciphertext_out = encrypt_blowfish(MESSAGE, SECRET_KEY)

    print("--- ENCRYPTION SUCCESSFUL ---")
    print(f"IV (8 bytes): {iv_out.hex()}")
    print(f"Ciphertext: {ciphertext_out.hex()}\n")

    # DECRYPTION
    decrypted_message = decrypt_blowfish(iv_out, ciphertext_out, SECRET_KEY)

    print("--- DECRYPTION SUCCESSFUL ---")
    print(f"Decrypted Message: {decrypted_message}")

    # Example of Failure (Wrong Key)
    print("\n--- FAILURE TEST (Wrong Key) ---")
    WRONG_KEY = get_random_bytes(16)
    failed_decryption = decrypt_blowfish(iv_out, ciphertext_out, WRONG_KEY)
    print(f"Decryption Attempt with Wrong Key: {failed_decryption}")