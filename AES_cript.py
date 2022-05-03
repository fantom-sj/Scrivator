import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes


def encrypt(plain_text, password):
    salt = get_random_bytes(AES.block_size)

    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)

    cipher_config = AES.new(private_key, AES.MODE_GCM)

    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(plain_text, 'utf-8'))

    enc_str = salt.hex() + '.' + cipher_config.nonce.hex() + '.' + tag.hex() + '.' + cipher_text.hex()
    return enc_str


def decrypt(enc_str, password):
    salt, nonce, tag, cipher_text = enc_str.split('.')
    salt = bytes.fromhex(salt)
    cipher_text = bytes.fromhex(cipher_text)
    nonce = bytes.fromhex(nonce)
    tag = bytes.fromhex(tag)

    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2 ** 14, r=8, p=1, dklen=32)

    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return bytes.decode(decrypted)


if __name__ == '__main__':
    password = input("Password: ")

    # First let us encrypt secret message
    encrypted = encrypt("The secretest message here", password)
    print(encrypted)

    # Let us decrypt using our original password
    decrypted = decrypt(encrypted, password)
    print(decrypted)