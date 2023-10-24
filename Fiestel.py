import struct
import random

def feistel_network(text, keys, rounds):
    left, right = struct.unpack('!QQ', text)

    for i in range(rounds):
        key = struct.unpack('!Q', keys[i])[0]
        temp = right
        right = (right ^ key) ^ left
        left = temp

    return struct.pack('!QQ', right, left)

def keygen(rounds):
    keys = []
    for i in range(rounds):
        key = random.randint(0, 2**64 - 1)
        byte_sequence = key.to_bytes(8, byteorder='big')
        keys.append(byte_sequence)
    return keys

def encrypt(plain_text, keys, rounds, block_size):
    encrypted_text = b''
    for i in range(0, len(plain_text), block_size):
        block = plain_text[i:i + block_size]
        if len(block) < block_size:
            block += b'\x00' * (block_size - len(block))
        encrypted_block = feistel_network(block, keys, rounds)
        encrypted_text += encrypted_block
    return encrypted_text


def decrypt(cipher_text, keys, rounds, block_size):
    keys.reverse()
    decrypted_text = b''
    for i in range(0, len(cipher_text), block_size):
        block = cipher_text[i:i + block_size]
        decrypted_block = feistel_network(block, keys, rounds)
        decrypted_text += decrypted_block
    return decrypted_text


# 测试
if __name__ == '__main__':
    user_input = input("请输入字符串: ")
    plain_text = user_input.encode('utf-8')
    rounds = 16
    block_size = 16
    keys = keygen(rounds)

    encrypted_text = encrypt(plain_text, keys, rounds, block_size)
    print("加密后:", encrypted_text)

    decrypted_text = decrypt(encrypted_text, keys, rounds, block_size)
    print("解密后:", decrypted_text.decode('utf-8').rstrip('\x00'))
