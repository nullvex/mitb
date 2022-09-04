import os
import sys
import time
import logging
import json
import configparser
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def decrypt(filename):
    with open(filename, "rb") as file:
        private_key = RSA.importKey(file.read(), 'MyPassphrase')

    rsa_cipher = PKCS1_OAEP.new(private_key)
    decrypted_text = rsa_cipher.decrypt(ciphertext)

    return decrypted_text
