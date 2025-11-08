from enum import Enum


class CipherMode(Enum):
    ENCRYPT = "ceasar_cipher_encrypt"
    DECRYPT = "ceasar_cipher_decrypt"

def caesar_cipher(
    text: str, shift: int,
    mode: CipherMode = CipherMode.ENCRYPT
) -> str | None:
    """Encrypts or decrypts a message usiing the Caesar Cipher."""
    # Adjust shift for decryption
    if mode == CipherMode.DECRYPT:
        shift = -shift
    
    result = ""
    
    for char in text:
        # Only process alphabetic characters
        if 'A' <= char <= 'Z' or 'a' <= char <= 'z':
            start_point = ord('A') if 'A' <= char <= 'Z' else ord('a')
            char_pos = ord(char) - start_point
            new_pos = (char_pos + shift) % 26
            new_char = chr(new_pos + start_point)
            result += new_char
        else:
            # Keep non-alphabetic characters (like spaces, punctuation) as they are
            result += char
            
    return result
    

if __name__ == "__main__":
    message = "Cryptography is fun!"
    key = 3  # The shift value
    
    encrypted_text = caesar_cipher(message, key, CipherMode.ENCRYPT)
    print("--- ENCRYPTION ---")
    print(f"Original: {message}")
    print(f"Key (Shift): {key}")
    print(f"Encrypted: {encrypted_text}\n")
    
    decrypted_text = caesar_cipher(encrypted_text, key, CipherMode.DECRYPT)
    print("--- DECRYPTION ---")
    print(f"Encrypted: {encrypted_text}")
    print(f"Key (Shift): {key}")
    print(f"Decrypted: {decrypted_text}")