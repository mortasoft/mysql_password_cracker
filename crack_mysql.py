#!/usr/bin/env python
from binascii import hexlify
from datetime import datetime
import hashlib
import argparse
import datetime
import tqdm


def crack_passwords(password_hash,salt,wordlist,mask):
    if len(password_hash) != 64:
        print("You must provide a valid password hash. (64 bytes)")
        exit(0)
    
    if len(salt) != 40:
        print("You must provide a valid hex salt (40 Bytes)")
        exit(0)

    salt = bytes.fromhex(salt)
    password_hash = str.encode(password_hash)

    try:
        wordlist_file = open(wordlist, "r", encoding='latin-1')
    except FileNotFoundError as e:
        print("[File not found] You must provide a valid file")
        exit(0)

    total_passwords= sum(1 for line in open(wordlist, "r", encoding='latin-1'))
    print(f"Total wordlist passwords to force: {total_passwords:,}")

    if args.verbose== 1:    
        with open(wordlist, "r", encoding='latin-1') as wordlist_file:
            for password in tqdm.tqdm(wordlist_file, total=total_passwords):
                if _crack_password(password_hash,password,mask,salt):
                    return {"result": True, "password": password.strip()}

    elif args.verbose== 2:
        for password in wordlist_file:

            print(f"Testing password > [" + _mask_password(password,mask).decode().strip() + "]")
            if _crack_password(password_hash,password,mask,salt):
                return {"result": True, "password": password.strip()}
    else:
        for password in wordlist_file:
            if _crack_password(password_hash,password,mask,salt):
                
                return {"result": True, "password": password.strip()}

    return {"result": False, "password": None}


def _crack_password(password_hash,password,mask,salt):

    password = _mask_password(password,mask)
    result_hash = hexlify(scramble_caching_sha2(password,salt))

    if(result_hash == password_hash):
        return True
    else:
        return False


def scramble_caching_sha2(password, nonce):
    # https://github.com/PyMySQL/PyMySQL/blob/main/pymysql/_auth.py
    # (bytes, bytes) -> bytes
    """Scramble algorithm used in cached_sha2_password fast path.
    XOR(SHA256(password), SHA256(SHA256(SHA256(password)), nonce))
    """
    if not password:
        return b""

    p1 = hashlib.sha256(password).digest()
    p2 = hashlib.sha256(p1).digest()
    p3 = hashlib.sha256(p2 + nonce).digest()

    res = bytearray(p1)
    for i in range(len(p3)):
        res[i] ^= p3[i]

    return bytes(res)


def _mask_password(password,mask):
    if not mask:
        return str.encode(password.strip())
    else:
        return str.encode(mask.replace("x",password.strip()))
     

if __name__ == "__main__":

    start_time = datetime.datetime.now()
    parser = argparse.ArgumentParser(description='Crack MySQL 8.0 caching_sha2_password algorithm passwords')
    parser.add_argument('--password', action='store', required=True, help='The sha256 password hash')
    parser.add_argument('--salt', action='store', required=True, help='The salt. Must be 20bits hex string. Example: "3b7749756a2f69763d057d07292719484b394e2b"')
    parser.add_argument('--wordlist', action='store', required=True, help='Text file with the wordlist to use')
    parser.add_argument('--mask', action='store', default=None, help='[Optional] The mask you want to use. The x is replaced with each password. Example: CiscoCTF{x}')
    parser.add_argument('--verbose', '-v',  action='count', default=0, help='[Optional] Verbosity Levels, v=Low Shows a progress bar, vv=High Print each password tested')
    args = parser.parse_args()

    try:
        process = crack_passwords(password_hash=args.password, salt= args.salt, wordlist= args.wordlist, mask=args.mask)
        if not process["result"]:
            print(f"Password not found. Try another wordlist ")
        else:
            print(f"Password found: [" + process["password"].strip() + "] Congratulations!")

        finish_time = datetime.datetime.now()
        duration = finish_time-start_time
        print(f"Script Duration: {duration}")
    except KeyboardInterrupt:
        finish_time = datetime.datetime.now()
        duration = finish_time-start_time
        print(f"Script Duration: {duration}")
