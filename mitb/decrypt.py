import rsa

def decrypt(encrypted_file_path, private_key_path, phrase):
    """Decrypts a file using an RSA private key."""

    with open(private_key_path, 'rb') as f:
        private_key = rsa.PrivateKey.load_pkcs1(f.read(), format='PEM')

    print(private_key)

    with open(encrypted_file_path, 'rb') as g:
        encrypted_data = g.read()

    decrypted_data = rsa.decrypt(encrypted_data, private_key)

    return decrypted_data
