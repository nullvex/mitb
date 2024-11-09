import os
import sys
import time
import logging
import json
import configparser
import zlib
import base64
import rsa
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class encrypt:
    """ Encrypts file passed in path using the passphrase passed in """

    def __init__(self, plaintext, filename, public_key_path):

        print("Filename: ", filename)

        with open(filename, 'rb') as f:
            blob = f.read()

        #public_key_path = key_path.split("/")[0] + "/public_key.pem"

        print("public_key_path:", public_key_path)

        #compress the data first
        blob = zlib.compress(blob)

        with open(public_key_path, "r") as key_file:
            public_key = RSA.import_key(key_file.read())

        encrypted_blob = rsa.encrypt(blob, public_key)

        #Base 64 encode the encrypted file
        #return base64.b64encode(encrypted_blob)

        #Write the encrypted contents to a file
        fd = open(filename + ".enc.z", "wb")
        fd.write(encrypted_blob)
        fd.close()
