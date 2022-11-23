# mysql_password_cracker
Crack MySQL 8.0 caching_sha2_password algorithm passwords using a wordlist

# Installation
```
git clone https://github.com/mortasoft/mysql_password_cracker
cd mysql_password_cracker
pip3 install -r requirements.txt
```

## Usage
```
usage: crack_mysql.py [-h] --password PASSWORD --salt SALT --wordlist WORDLIST [--mask MASK] [--verbose]

Crack MySQL 8.0 caching_sha2_password algorithm passwords

options:
  -h, --help           show this help message and exit
  --password PASSWORD  The sha256 password hash Example: "1248ed45984fd9b1e5ee7ff8dabde10d8c3bd768dbf47315feb48323e6c55222"
  --salt SALT          The salt. Must be 20bits hex string. Example: "3b7749756a2f69763d057d07292719484b394e2b"
  --wordlist WORDLIST  Text file with the wordlist to use
  --mask MASK          [Optional] The mask you want to use. The x is replaced with each password. Example: CiscoCTF{x}
  --verbose, -v        [Optional] Verbosity Levels, v=Low Shows a progress bar, vv=High Print each password tested
```

## Examples 
```bash
# Low Verbosity
crack_mysql.py --wordlist rock_you.txt --password 1248ed45984fd9b1e5ee7ff8dabde10d8c3bd768dbf47315feb48323e6c55222 --salt 5a1230123b2e68763d057d00005509484b394e1b --mask "CiscoCTF{x}" -v
```

```bash
# High Verbosity
crack_mysql.py --wordlist rock_you.txt --password 1248ed45984fd9b1e5ee7ff8dabde10d8c3bd768dbf47315feb48323e6c55222 --salt 5a1230123b2e68763d057d00005509484b394e1b --mask "CiscoCTF{x}" -vv
```
