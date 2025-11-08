from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def crypto_encrypt_data(plaintext: str):
    # Generate a 256-bit (32-byte) secret key
    # This key must be kept secret and used for BOTH encryption and decryption
    key = get_random_bytes(32)
    cipher = AES.new(key, AES.MODE_GCM)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode("utf-8"))
    return key, nonce, ciphertext, tag

def crypto_decrypt_data(
    key: bytes, nonce: bytes | bytearray | memoryview,
    ciphertext: bytes, tag: bytes
):
    # Create the cipher object with the same key and mode
    cipher = AES.new(key, AES.MODE_GCM, nonce)

    try:
        # Decrypt the data, verifying the tag (integrity check)
        plaintext_bytes = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext_bytes.decode('utf-8')
    except ValueError:
        # This error is raised if the key is wrong OR the data/tag was tampered with
        return "Decryption failed: Key is incorrect or message was tampered with."
    

if __name__ == "__main__":
    original_message = "Hello, this is a secret message encrypted with AES-256!"
    secret_key, iv_nonce, encrypted_message, auth_tag = crypto_encrypt_data(original_message)
    
    print("--- ENCRYPTION RESULT ---")
    print(f"Original Message: {original_message}")
    print(f"Secret Key (32 bytes): {secret_key.hex()}")
    print(f"Nonce (must be public): {iv_nonce.hex()}")
    print(f"Ciphertext (encrypted): {encrypted_message.hex()}")
    print(f"Authentication Tag: {auth_tag.hex()}\n")
    
    decrypted_message = crypto_decrypt_data(secret_key, iv_nonce, encrypted_message, auth_tag)
    print("--- DECRYPTION RESULT ---")
    print(f"Decrypted Message: {decrypted_message}")