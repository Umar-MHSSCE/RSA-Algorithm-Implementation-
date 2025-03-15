import random
from sympy import isprime, mod_inverse

def generate_prime(bits):
    """Generate a random prime number with the given bit length."""
    while True:
        num = random.getrandbits(bits)
        if isprime(num):
            return num

def generate_keys():
    """Generate RSA public and private keys."""
    p = generate_prime(16)  # Generate a 16-bit prime number
    q = generate_prime(16)  # Generate another 16-bit prime number

    while p == q:  # Ensure p and q are different
        q = generate_prime(16)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 65537  # Commonly used public exponent
    if phi_n % e == 0:  # Ensure e is coprime to φ(n)
        e = 3

    d = mod_inverse(e, phi_n)  # Compute modular inverse of e mod φ(n)

    return {e, n}, [d, p, q]  # Public key: {e, n}, Private key: [d, p, q]

def encrypt(message, public_key):
    """Encrypt the message using the RSA formula: C = M^e mod n."""
    e, n = public_key
    cipher = []  # Create an empty list to store encrypted values

    for char in message:  # Loop through each character in the message
        ascii_value = ord(char)  # Convert character to ASCII number
        encrypted_value = pow(ascii_value, e, n)  # Apply RSA encryption formula
        cipher.append(encrypted_value)  # Store encrypted value in the list

    return cipher

def decrypt(cipher, private_key):
    """Decrypt the message using the RSA formula: M = C^d mod n."""
    d, p, q = private_key
    n = p * q  # Recalculate n
    decrypted_message = ""  # Initialize an empty string for the decrypted message

    for char in cipher:  # Loop through each encrypted number in the list
        decrypted_value = pow(char, d, n)  # Apply RSA decryption formula
        original_char = chr(decrypted_value)  # Convert back to a character
        decrypted_message += original_char  # Append character to decrypted message

    return decrypted_message

# RSA Algorithm Execution
public_key, private_key = generate_keys()

# Display Public and Private Keys
print("\nGenerated RSA Keys:")
print("Public Key (e, n): ", public_key)
print("Private Key (d, p, q): ", private_key)

while True:
    # Take message input from user
    message = input("\nEnter a message to encrypt: ")

    # Encryption
    ciphertext = encrypt(message, public_key)
    print("\nEncrypted Message:", ciphertext)

    # Decryption
    decrypted_message = decrypt(ciphertext, private_key)
    print("Decrypted Message:", decrypted_message)

    cont = input("Do you want to continue? (yes/no): ")
    if cont.lower() != 'yes':
        break
