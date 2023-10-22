import os
from cryptography.fernet import Fernet
import logging

if __name__ == '__main__':
    os.mkdir("decrypted_files")
    key = b'4kubp0WObXXqcfjLj42rWSyvPubOgCRNrhYsgb_P_pQ='

    for file_decrypt in os.listdir('files_recieved'):
        if file_decrypt[:2] == 'e_':
            with open(f'files_recieved/{file_decrypt}', 'rb') as encrypted_file:
                data = encrypted_file.read()
            decrypted = Fernet(key).decrypt(data)
            with open(f'decrypted_files/{file_decrypt[2:]}', 'ab') as regular_file:
                regular_file.write(decrypted)
            # os.remove(f'files_recieved/{file_decrypt}')
