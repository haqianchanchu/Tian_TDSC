from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


# 如果text不足16位的倍数就用空格补足为16位
def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')

def handle_key(key):
    key = key[2:]
    key = hex(int(key,10))
    key = key+"f"*32
    key = key[2:34]
    key = a2b_hex(key)
    return key

# 加密函数
def encrypt(key,text):
    # key = add_to_16(key)
    key = handle_key(key)
    mode = AES.MODE_CBC
    iv = b'qqqqqqqqqqqqqqqq'
    text = add_to_16(text)
    cryptos = AES.new(key, mode, iv)
    cipher_text = cryptos.encrypt(text)
    # 因为AES加密后的字符串不一定是ascii字符集的，输出保存可能存在问题，所以这里转为16进制字符串
    return b2a_hex(cipher_text)


# 解密后，去掉补足的空格用strip() 去掉
def decrypt(key,text):
    key = handle_key(key)
    iv = b'qqqqqqqqqqqqqqqq'
    mode = AES.MODE_CBC
    cryptos = AES.new(key, mode, iv)
    plain_text = cryptos.decrypt(a2b_hex(text))
    return bytes.decode(plain_text).rstrip('\0')


if __name__ == '__main__':
    e = encrypt("111111","hello world")  # 加密
    d = decrypt("111111",e)  # 解密
    # with open("tem","w") as f:
    #     f.write(e)
    print("加密:", e.decode().encode())
    print("解密:", d)