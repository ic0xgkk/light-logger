from Crypto.Cipher import AES as aes
import logging
from binascii import crc32 as CRC32
# import binascii
import time
import random
import sys
import operator


class SecService(object):
    def __init__(self, key):
        self.key = key
        self.timestamp = 0

    def run(self, data):
        decrypt_data = self.decrypt(data)
        timestamp, project_name, level, msg = self.decrypt_data_processing(decrypt_data)
        ra_status = self.timestamp_check(timestamp)
        if ra_status > 0:
            return timestamp, project_name, level, msg
        else:
            return -1

    def decrypt(self, data):
        decrypt = aes.new(self.key, aes.MODE_CBC, self.key)
        decrypt_data = decrypt.decrypt(data)  # bytearray()
        return decrypt_data

    def decrypt_data_processing(self,  data):
        data_len = len(data)
        crc32 = data[data_len-3:data_len]  # get last 4 bytes as crc32
        crc32_data = data[0:data_len-4]
        if CRC32(crc32_data) == crc32:
            logging.info("Data usability checking passed")
            timestamp = data[0:3]  # get 4 bytes as timestamp
            level = data[4]  # get 1 byte as log level
            tmp = data[5:data_len-4]  # copy message

            data = str(tmp)
            data_dict = data.split('\0')
            project_name = data_dict[0]
            msg = data_dict[1]
            return timestamp, project_name, level, msg
        else:
            logging.warning("Data destroyed")
            return -1

    def timestamp_check(self, timestamp):
        if timestamp > self.timestamp:
            logging.info("Timestamp checking passed")
            self.timestamp = timestamp
            return 1
        if timestamp == self.timestamp:
            logging.warning("Replay attack detected")
            return -1
        if timestamp < self.timestamp:
            logging.error("!!!Key is loss!!!")
            return -2


# (9980883231).to_bytes(6, "little")



'''
    def random_header_builder(self):
        random.seed(int(time.time()))
        self.random_int = random.randint(10000000, 50000000)
        aes_crypt = Crypto.Cipher.AES.new(self.base_key, Crypto.Cipher.AES.MODE_CBC, self.base_key)
        encrypted_text = aes_crypt.encrypt((str(self.random_int) + str(self.random_int)).encode('ascii'))  # Fill to 16 digits

        h = Crypto.Hash.SHA256.new()
        res = str(int((self.random_int + int(time.time() / 100) - 222011) * 1.14635))

        return encrypted_text

        # conn.send(encrypted_text)
        ra_header = conn.recv()
        res = str(int((random_int + int(time.time() / 100) - 222011) * 1.14635))
        h = SHA256.new()
        h.update(res.encode('utf-8'))
        if ra_header == h.hexdigest():
            return True
        else:
            return False


    # Authentication header builder is used to avoid replay attack
    def au_header_builder(self):
        sec = int(time.time() / 100)  # Time threshold value are 100 sec
        sal_tim = str(sec) + str(sec)
        ori_value = self.ah_key + sal_tim
        h = Crypto.Hash.MD5.new()
        h.update(ori_value.encode('ascii'))
        return h.hexdigest()
'''



