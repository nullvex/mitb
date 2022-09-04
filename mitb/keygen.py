import os
import sys
import time
import logging
import json
import configparser

class create:
    """ Creates keys for encryption in a spcecific path """


    def __init__(self, path):

        print("Path:", path)

        from Crypto.PublicKey import RSA

        keypair = RSA.generate(2048)
        public_key = keypair.publickey()

        public_key_path = "%s/public_key.pem" % (path)
        print("public_key_path", public_key_path)
        private_key_path = "%s/private_key.pem" % (path)
        print("private_key_path", private_key_path)

        with open(public_key_path, "wb") as file:
            file.write(public_key.exportKey('PEM'))
            file.close()

        with open(private_key_path, "wb") as file:
            file.write(keypair.exportKey('PEM', 'MyPassphrase'))
            file.close()

