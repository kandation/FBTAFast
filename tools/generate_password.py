def printPassword(dir='./'):
    from fbta import encrypt
    pwd = encrypt.Encrypt()
    pwd.loadKey('./key.key')
    pwd.loadPassword('./password.enc')
    pwd = pwd.decrypt()
    return pwd


def generatePasswordFile(password: str):
    from fbta import encrypt
    pwd = encrypt.Encrypt()
    pwd.getPasswordKey()
    pwd.encrypt(password)
    pwd.saveKey()
    pwd.savePassword()
    return pwd


if __name__ == '__main__':
    # generatePasswordFile('YOUR-PASSWORD')
    print(printPassword())

