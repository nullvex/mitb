import json
import logging
import os
import shutil
import subprocess
import sys
import time
import paramiko
import requests
import re
from tqdm import tqdm
from urllib.request import urlopen

log = logging.getLogger(__name__)
log.info("Launching the Util Class")


class utils:
    """ Builds the OS from provided ISO path and configuration definitions"""

    def __init__(self):
        log = logging.getLogger(__name__)
        log.info("Launching the Util Class")

    # Basic Make Directory Function
    def mkdir_p(self, path):
        if os.path.exists(path):
            log.info("%s exists" % (path))
        else:
            log.info("Creating Directory: %s" % (path))
            os.makedirs(path)

    def touch(self, path):
        open(path, "a").close()

    # Basic file list function
    def list_dir(self, _path):
        dirListing = os.listdir(_path)
        return dirListing

    # Base File Read Function
    def read_file(self, _file):
        with open(_file) as f:
            content = f.readlines()
        return f

    # Read File and Create sha256 Signature
    def sha256_for_file(self, f, block_size=2 ** 20):
        sha256_hash = hashlib.sha256()
        with open(f, "rb") as this_file:
            for byte_block in iter(lambda: this_file.read(block_size), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    # Downloads ISO Specified
    def fetch_iso(self, _url, _md5, _base_dir):
        # Determine file name from param
        file_name = _url.split("/")[-1]
        full_path = "%s/%s" % (_base_dir, file_name)

        # check to see if ISO file is in the target directory
        # if so generate a hash for it
        if os.path.isfile("%s/%s" % (_base_dir, file_name)):
            log.info("The Image Has Already Been Downloaded")
        else:
            utils.fetch_file(self, _url, _base_dir)
        f = open(full_path)
        log.info("Checking Hash of the Image")
        isomd5 = utils.md5_for_file(self, full_path)
        isosha = utils.sha256_for_file(self, full_path)
        isoObj = []
        isoObj = isomd5, isosha, full_path
        # Return the object containing both isohash and path
        return isoObj

    # Opens the md5 file
    def fetch_hash(self, _url, _base_dir):
        utils.fetch_file(self, _url, _base_dir)

    def fetch_file(self, _url, _base_dir):
        global url, file_name
        file_name = _url.split("/")[-1]
        output_path = "%s/%s" % (_base_dir, file_name)
        r = requests.get(_url, stream=True)
        # Total size in bytes.
        total_size = int(r.headers.get("content-length", 0))
        block_size = 1024  # 1 Kibibyte
        t = tqdm(total=total_size, unit="iB", unit_scale=True)
        with open(output_path, "wb") as f:
            for data in r.iter_content(block_size):
                t.update(len(data))
                f.write(data)
        t.close()
        if total_size != 0 and t.n != total_size:
            print("ERROR, something went wrong")
        return file_name

    def del_file(self, _path):
        os.remove(_path)

    def parse_os(self, config_path, _osName, _base_dirName):
        osObj = {}
        # The environment descriptor is actually a symlink to the one auto-generated
        jsonDoc = "%s%s.json" % (config_path, _osName)
        # Bail if the environment descriptor can't be accessed
        if not os.path.isfile(jsonDoc):
            log.error("OS Config File Not Found")
            thisError = {
                "retVal": 1,
                "message": 'Cannot find descriptor "%s"' % jsonDoc,
            }
        # Open jsonDoc and parse it into a dictionary
        json_data = open(jsonDoc)
        osObj = json.load(json_data)
        # Return OS Object
        return osObj

    def parse_hash(self, osObj, _base_dirName):

        matching = ''

        # Pull Image Info from osObj
        image_hash = osObj["imageMD5"]
        print("ImageHash: ", image_hash)

        # Split it to get the file name out
        hashfile = image_hash.split("/")[-1]

        # Get list of files in the target directory
        dirList = utils.list_dir(self, _base_dirName)

        # Read the Content of the MD5 Hash File
        with open("%s/%s" % (_base_dirName, hashfile)) as f:
            hash_content = f.readlines()

        checksums = []

        # Find every line in the md5 has file that correlates with the md5sum
        # matching = [(dirList[0]) for record in md5Content if dirList[0] == record ]
        index = 0
        for i in hash_content:
            if not i.startswith('#'):
                checksums.append([i.split(" ")[0].strip(), re.sub(r" ?\(\)", "", i.split(" ")[1].strip("()")), i.split(" ")[2].strip(), i.split(" ")[3].strip()])
                print(checksums)
                this_hash_file = i.split(" ")[-1].strip().replace("*", "")
                #print("this_hash_file: %s" % (this_hash_file))
                #hash_string = i.split(" ")[1].strip()
                #print("hash_string_1: ", hash_string)
                #hash_string2 = re.sub(r" ?\([^)]+\)", "", hash_string)
                #print("hash_string_2: ", hash_string2)
                #check_sum_filename = re.sub(r" ?:", "", hash_string2)
                #print("hash_string_3: ", check_sum_filename)
                #print("HashString_sub_1: ",check_sum_filename)
                #print("i: ",i)
                log.info("this_hash_file: %s" % (this_hash_file))
                for j in dirList:
                    j = j.strip()
                    print("DirItem: ", j)
                    print("HashString_sub_2: ",checksums[index][1])
                    if checksums[index][1] == j:
                        matching = this_hash_file
                        break
                print(checksums[index][1])
                index = index + 1
        if not matching:
            print("Make Sure Your ISO Version Matches whats in the Hash Sum file")
            sys.exit()
        return matching

    def mount(self, working_dir):
        mount_cmd = "mount /dev/mapper/loop0p1 %s/default" % (working_dir)
        subprocess.call(mount_cmd, shell=True)

    def mount_iso(self, mount_path, iso_path):
        mntiso_cmd = "mount -o loop %s %s" % (iso_path, mount_path)
        log.info("mntiso_cmd: %s" % (mntiso_cmd))
        subprocess.call(mntiso_cmd, shell=True)

    def unmount_iso(self, mount_path):
        unmountcmd = "umount %s" % (mount_path)
        subprocess.Popen(unmountcmd, shell=True)

    def copy_dir(self, src, dest):
        try:
            shutil.copytree(src, dest)
        except OSError as e:
            # If the error was caused because the source wasn't a directory
            if e.errno == errno.ENOTDIR:
                shutil.copytree(src, dst, symlinks=True, ignore=None)
            else:
                log.error("Directory not copied. Error: %s" % e)

    def rsync_dir(self, src, dest):
        rsync_cmd = "rsync -av %s %s" % (src, dest)
        try:
            subprocess.call(rsync_cmd, shell=True)
        except:
            log.error("Rsync Failed")

    def fail():
        log.info("whoops")
        sys.exit()

    def format_bytes(self, size):
        # 2**10 = 1024
        power = 2 ** 10
        n = 0
        power_labels = {0: "", 1: "kilo", 2: "mega", 3: "giga", 4: "tera"}
        while size > power:
            size /= power
            n += 1
        return size, power_labels[n] + "bytes"

    def ssh_block_copy(self, host, user, identity, device, working_dir, image_name):
        """ Copies a block volume from an ssh source host to a raw image file locally """
        filename = "%s-%s.img" % (host, device.split("/")[2])
        image_path = "%s/%s" % (working_dir, filename)

        # Paramiko is far too slow for this
        # k = paramiko.RSAKey.from_private_key_file(identity)
        # ssh_client = paramiko.SSHClient()
        # ssh_client.get_transport().window_size = 3 * 1024 * 1024
        # ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh_client.connect(hostname=host,username=username,pkey=k)
        # stdin,stdout,stderr=ssh_client.exec_command(dd_command)
        # stdout.channel.recv_exit_status()
        # out_file = stdout.read()
        # f = open(image_path, 'w')
        # f.write(out_file)

        dd_command = "sudo dd if=%s" % (device)
        ssh_command = 'ssh -i %s  %s@%s "%s" | dd of=%s' % (
            identity,
            user,
            host,
            dd_command,
            image_path,
        )
        print(ssh_command)

        subprocess.call(ssh_command, shell=True)

        return image_path
