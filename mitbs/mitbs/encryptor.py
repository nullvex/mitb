from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import os
import zlib


class encryptor:
    def __init__(self, key_dir="keys", key_size=2048):
        self.key_dir = key_dir
        self.key_size = key_size
        print("KeySize: %s" % (key_size))
        os.makedirs(self.key_dir, exist_ok=True)

    def generate_keys(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=self.key_size, backend=default_backend()
        )
        # Save private key
        private_key_path = os.path.join(self.key_dir, "private_key.pem")
        with open(private_key_path, "wb") as f:
            f.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
        # Save public key
        public_key = private_key.public_key()
        public_key_path = os.path.join(self.key_dir, "public_key.pem")
        with open(public_key_path, "wb") as f:
            f.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )

        print(f"Keys generated and saved: {private_key_path}, {public_key_path}")

    def load_public_key(self):
        public_key_path = os.path.join(self.key_dir, "public_key.pem")
        with open(public_key_path, "rb") as f:
            return serialization.load_pem_public_key(
                f.read(), backend=default_backend()
            )

    def encrypt_and_compress_file(self, input_file_path, output_file_path):
        # Load the public key
        public_key = self.load_public_key()

        # Read the contents of the file
        with open(input_file_path, "rb") as f:
            file_data = f.read()

        # Compress the data
        compressed_data = zlib.compress(file_data)

        # Encrypt the compressed data
        encrypted_data = public_key.encrypt(
            compressed_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        # Save the encrypted data
        with open(output_file_path, "wb") as f:
            f.write(encrypted_data)

        print(f"File encrypted and compressed: {output_file_path}")

    def load_private_key(self):
        private_key_path = os.path.join(self.key_dir, "private_key.pem")
        with open(private_key_path, "rb") as f:
            return serialization.load_pem_private_key(
                f.read(), password=None, backend=default_backend()
            )

    def decrypt_and_decompress_file(self, encrypted_file_path, output_file_path):
        # Load the private key
        private_key = self.load_private_key()

        # Read the encrypted data
        with open(encrypted_file_path, "rb") as f:
            encrypted_data = f.read()

        # Decrypt the data
        decrypted_data = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        # Decompress the data
        decompressed_data = zlib.decompress(decrypted_data)

        # Save the decrypted, decompressed data
        with open(output_file_path, "wb") as f:
            f.write(decompressed_data)

        print(f"File decrypted and decompressed: {output_file_path}")
