import os
import rsa

class RSACipher:
    def __init__(self):
        self.keys_dir = os.path.join(os.path.dirname(__file__), 'keys')
        self.pub_path = os.path.join(self.keys_dir, 'publicKey.pem')
        self.pri_path = os.path.join(self.keys_dir, 'privateKey.pem')

    def generate_keys(self):
        if not os.path.exists(self.keys_dir):
            os.makedirs(self.keys_dir)
        (public_key, private_key) = rsa.newkeys(1024)
        with open(self.pub_path, 'wb') as p:
            p.write(public_key.save_pkcs1('PEM'))
        with open(self.pri_path, 'wb') as p:
            p.write(private_key.save_pkcs1('PEM'))

    def load_keys(self):
        with open(self.pub_path, 'rb') as p:
            public_key = rsa.PublicKey.load_pkcs1(p.read())
        with open(self.pri_path, 'rb') as p:
            private_key = rsa.PrivateKey.load_pkcs1(p.read())
        return private_key, public_key

    def encrypt(self, message, key):
        message_bytes = message.encode('utf8')
        return rsa.encrypt(message_bytes, key)

    def decrypt(self, ciphertext, key):
        return rsa.decrypt(ciphertext, key).decode('utf8')

    def sign(self, message, private_key):
        message_bytes = message.encode('utf8')
        return rsa.sign(message_bytes, private_key, 'SHA-256')

    def verify(self, message, signature, public_key):
        message_bytes = message.encode('utf8')
        try:
            rsa.verify(message_bytes, signature, public_key)
            return True
        except rsa.VerificationError:
            return False