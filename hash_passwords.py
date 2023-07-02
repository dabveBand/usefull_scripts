#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi el3arbi_@email.com
# created       : 31-August-2022
#
# description   : how to hash and verify passwords from the Django framework
# ----------------------------------------------------------------------------


import base64
import hashlib
import secrets
ALGORITHM = 'pbkdf2_sha256'


def hash_password(pwd, salt=None, iterations=260000):
    if salt is None:
        salt = secrets.token_hex(16)
    assert salt and isinstance(salt, str) and "$" not in salt
    assert isinstance(pwd, str)
    pw_hash = hashlib.pbkdf2_hmac('sha256', pwd.encode('utf-8'), salt.encode('utf-8'), iterations)
    b64_hash = base64.b64encode(pw_hash).decode('ascii').strip()
    return '{}${}${}${}'.format(ALGORITHM, iterations, salt, b64_hash)


def verify_password(pwd, pwd_hash):
    if (pwd_hash or '').count("$") != 3:
        return False
    algorithm, iterations, salt, b64_hash = pwd_hash.split('$', 3)
    iterations = int(iterations)
    assert algorithm == ALGORITHM
    compare_hash = hash_password(pwd, salt, iterations)
    return secrets.compare_digest(pwd_hash, compare_hash)


if __name__ == '__main__':
    passwd = input('Enter Password to Hash: ')
    passwd = hash_password(passwd)
    while True:
        try:
            passwd_verify = input('Enter Password to verify [Ctrl+C to exit]: ')
            print(verify_password(passwd_verify, passwd))
            print()
        except KeyboardInterrupt:
            break
