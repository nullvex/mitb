import os
import sys
import time
import logging
import json
import configparser
import zlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

class encrypt:
    """ Encrypts file passed in path using the passphrase passed in """

    def __init__(self, plaintext, filename, key_path):

        public_key_path = key_path + "/public_key.pem"

        with open(public_key_path, "rb") as file:
            public_key = RSA.importKey(file.read())

        rsGa_cipher = PKCS1_OAEP.new(public_key)
        ciphertext = rsa_cipher.encrypt(plaintext.encode())

        return ciphertext

    def encrypt_file(self, plaintext, filename, key_path):

        public_key_path = key_path + "/public_key.pem"

        #compress the data first
        blob = zlib.compress(blob)

        #In determining the chunk size, determine the private key length used in bytes
        #and subtract 42 bytes (when using PKCS1_OAEP). The data will be in encrypted
        #in chunks
        chunk_size = 470
        offset = 0
        end_loop = False
        encrypted =  ""

        while not end_loop:
            #The chunk
            chunk = blob[offset:offset + chunk_size]

            #If the data chunk is less then the chunk size, then we need to add
            #padding with " ". This indicates the we reached the end of the file
            #so we end loop here
            if len(chunk) % chunk_size != 0:
                end_loop = True
                chunk += " " * (chunk_size - len(chunk))


        #Append the encrypted chunk to the overall encrypted file
        encrypted += rsa_key.encrypt(chunk)

        #Increase the offset by chunk size
        offset += chunk_size

        #Base 64 encode the encrypted file
        return base64.b64encode(encrypted)

        #Use the public key for encryption
        fd = open("public_key.pem", "rb")
        public_key = fd.read()
        fd.close()

        #Our candidate file to be encrypted
        fd = open("img.jpg", "rb")
        unencrypted_blob = fd.read()
        fd.close()

        encrypted_blob = encrypt_blob(unencrypted_blob, public_key)

        #Write the encrypted contents to a file
        fd = open(file_path + "/.jpg.enc.z", "wb")
        fd.write(encrypted_blob)
        fd.close()