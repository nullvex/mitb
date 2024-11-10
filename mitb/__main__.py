import os
import sys
import configparser
import io
import argparse
import logging
import logging.config

#############################################################
# Setup Paths
#############################################################
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
this_path = os.path.dirname(os.path.realpath(__file__))
one_up = os.path.dirname(os.path.realpath(__file__)) + "/../"
# app_path = os.path.join(this_path, one_up)

#############################################################
# Import Local Classes
#############################################################
from mitb import keygen
from mitb import encrypt
from mitb import decrypt
from mitb import utils
from mitb import encryptor
from mitb import rbmq_producer
from mitb import rbmq_consumer

###### Logging ######
log_path = "logs/mitb.log"
log_dir = "logs/"
utils = utils.utils()

if not os.path.isdir(log_dir):
    utils.mkdir_p(log_dir)
if not os.path.isfile(log_path):
    utils.touch(log_path)

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p %Z - ",
)

#############################################################
####################### Main Program ########################
#############################################################


class mitb_init(object):
    def __init__(self):
        log = logging.getLogger(__name__)
        log.info("-Starting Message in the Bottle-")

        # Multi-Command Parser Setup
        parent_parser = argparse.ArgumentParser(
            description="Encrypt and Decrypt Files using atypical key sources",
            usage=""" mitb <command> [<args>]
        Commands:

        keygen - Creates Keys and target key formats

        encrypt - Uses Keys to encrypt files

        decrypt - Uses Keys to decrypt files

        """,
        )

        # create subcommand parser
        parent_parser.add_argument("command", help="Subcommand to run")
        args = parent_parser.parse_args(sys.argv[1:2])
        # If argument doesn't match defined commands complain
        if not hasattr(self, args.command):
            print("Unrecognized Command")
            parent_parser.print_help()
            exit(1)
        # Collect sub command args
        getattr(self, args.command)()

    def keygen(self):
        """Creates default keys necessary to encrypt and decrypt"""
        encryptor = encryptor.encryptor()
        parser = argparse.ArgumentParser(description="Creates Key")
        #parser.add_argument("path", help="Add local path to the keys directory")
        args = parser.parse_args(sys.argv[2:])

        # rawobj = keygen.create(args.path)
        encryptor.generate_keys()

    def encrypt(self):
        """Encrypts files"""
        encryptor = encryptor.encryptor()
        parser = argparse.ArgumentParser(description="Encrypts File")
        #parser.add_argument("passphrase", help="passphrase for private key encryption")
        parser.add_argument("file_path", help="local path to file to be encrypted")
        parser.add_argument("output_path", help="local path to file to be written")
        #parser.add_argument("key_path", help="path to the public and private key")
        args = parser.parse_args(sys.argv[2:])

        # rawobj = encrypt.encrypt(args.passphrase, args.file_path, args.key_path)
        rawobj = encryptor.encrypt_and_compress_file(
            args.file_path, args.output_path
        )

    def decrypt(self):
        encryptor = encryptor.encryptor()
        """Decrypts files"""
        parser = argparse.ArgumentParser(description="Decrypts File")
        #parser.add_argument(
        #    "private_key_path", help="the path to the private key used to sign the file"
        #)
        parser.add_argument("file_path", help="the file youre trying to decrypt")
        parser.add_argument("out_path", help="the file youre trying to decrypt")
        #parser.add_argument("passphrase", help="the passphrase you used to encrypt")

        args = parser.parse_args(sys.argv[2:])

        # rawobj = decrypt.decrypt(args.file_path, args.private_key_path, args.passphrase)
        rawobj = encryptor.decrypt_and_decompress_file(
            args.file_path, args.out_path
        )

        print(rawobj)


if __name__ == "__main__":
    mitb_init()
