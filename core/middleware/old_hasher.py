from django.contrib.auth.hashers import BasePasswordHasher, mask_hash
import hashlib
import binascii
import base64
from collections import OrderedDict
from django.utils.translation import gettext_noop as _


class OldHasher(BasePasswordHasher):
    algorithm = "old_hash"

    def verify(self, password, encoded):
        algorithm,  salt, hash = encoded.split('$', 3)
        assert algorithm == self.algorithm
        salt = base64.b64decode(salt.encode('ascii')).hex()
        salted_password = salt.encode() + password.encode()
        check = binascii.hexlify(hashlib.sha256(
            salted_password).digest()).decode('ascii')
        print(password)
        return (check == hash)

    def safe_summary(self, encoded):
        algorithm,  salt, hash = encoded.split('$', 3)
        assert algorithm == self.algorithm
        return OrderedDict([
            (_('algorithm'), algorithm),
            (_('salt'), mask_hash(salt)),
            (_('hash'), mask_hash(hash)),
        ])


# def new_password(encoded):
#     salt = encoded[:64]
#     hashed_password = encoded[64:]
#     base64_salt = base64.b64encode(bytes.fromhex(salt)).decode('ascii')
#     return "%s$%s$%s" % ('old_hash', base64_salt, hashed_password)


# # new = new_password(encoded)
# # print(new)


# def verify(password, encoded):
#     algorithm, salt, hash = encoded.split('$', 3)
#     salt = base64.b64decode(salt.encode('ascii')).hex()
#     salted_password = salt.encode() + password.encode()
#     print(hash)
#     check = binascii.hexlify(hashlib.sha256(
#         salted_password).digest()).decode('ascii')
#     print(check)


# encoded = 'old_hash$MiUsYnQuU2V4R15JSEVdQ0FtRiN0N0xfZFEodV9eSSI=$6f8b2f53b2cb8f8bc3336ba8ece78d436e90248b6c9de7c71bd8022eb86e5387'
# password = 'metro2o33'
# verify(password, encoded)

# salt = '181f56d2f85d789aadf11e3a71b997415d939786421cd8c8444760d46b2b51f8'
# # hex_str = salt
# # print(salt)
# # encoded_str = base64.b64encode(bytes.fromhex(hex_str)).decode('ascii')
# # print(encoded_str)
# # # decoded_str = base64.b64decode(encoded_str.encode('ascii')).hex()
# # print(decoded_str)
