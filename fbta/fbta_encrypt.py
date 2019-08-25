from cryptography.fernet import Fernet
import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class FBTAEncrypt:
    def __init__(self):
        self.password_hash = None
        self.key = None
        self.fernet = None

    def getPasswordKey(self) -> str:
        password_provided = "THIS_IS_FBTA_MAGIC_KEY"
        password = password_provided.encode()
        salt = bytes(os.urandom(512))
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512_256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        self.key = key
        return key

    def loadKey(self, file):
        with open(file, 'rb') as fo:
            data = fo.read()
        self.key = data

    def loadPassword(self, file):
        with open(file, 'rb') as fo:
            data = fo.read()
        self.password_hash = data
        return self.password_hash

    def saveKey(self, dir='./'):
        self.__checkKeyAndSetKey()
        with open(dir + 'key.key', mode='wb') as fo:
            fo.write(self.key)

    def savePassword(self, dir='./'):
        self.__checkKeyAndSetKey()
        self.__checkPasswordHashAndThrow()

        with open(dir + 'password.enc', mode='wb') as fo:
            fo.write(self.password_hash)

    def __checkKeyAndSetKey(self):
        if self.key is None:
            self.getPasswordKey()

    def __checkPasswordHashAndThrow(self):
        if self.password_hash is None:
            raise Exception("Not Have Password Hash")

    def __checkFernetAndSetFernet(self):
        if self.fernet is None:
            self.fernet = Fernet(self.key)

    def encrypt(self, pwd='') -> str:
        self.__checkKeyAndSetKey()
        self.__checkFernetAndSetFernet()

        self.password_hash = self.fernet.encrypt(bytes(pwd, encoding='utf8'))
        return self.password_hash

    def decrypt(self, encrypted=None) -> str:
        self.__checkKeyAndSetKey()
        self.__checkFernetAndSetFernet()

        decrypted = self.fernet.decrypt(encrypted if encrypted is not None else self.password_hash)

        return str(bytes(decrypted).decode('utf8'))
