from datetime import datetime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers.aead import AESCCM
from os import urandom
import luhn
import pytz, json, base64

class ClientSideEncryption():
    def __init__(self, key, card_data):
        self.adyen_public_key = key
        self.name = card_data["name"]
        self.pan = card_data["cc_num"]
        self.cvc = card_data["cvv"]
        self.expiry_month = card_data["month"]
        self.expiry_year = card_data["year"]
        #self.run()

    def generate_adyen_nonce(self):
        plain_card_data = self.generate_card_data_json()
        card_data_json_string = json.dumps(plain_card_data, sort_keys=True)

        # Encrypt the actual card data with symmetric encryption
        aes_key = self._generate_aes_key()
        nonce = self._generate_nonce()
        encrypted_card_data = self._encrypt_with_aes_key(aes_key, nonce, bytes(card_data_json_string))
        encrypted_card_component = nonce + encrypted_card_data

        # Encrypt the AES Key with asymmetric encryption
        public_key = self.decode_adyen_public_key(self.adyen_public_key)
        encrypted_aes_key = self._encrypt_with_public_key(public_key, aes_key)
        return "{}{}${}${}".format("adyenjs",
                                   "_0_1_12",
                                   base64.standard_b64encode(encrypted_aes_key).decode("utf-8"),
                                   base64.standard_b64encode(encrypted_card_component).decode("utf-8"))

    #@staticmethod
    def generate_card_data_json(self):
        generation_time = datetime.now(tz=pytz.timezone('UTC')).strftime('%Y-%m-%dT%H:%M:%S.000Z')
        return {
            "cvc": self.cvc,
            "dfValue": "",
            "expiryMonth": self.expiry_month,
            "expiryYear": self.expiry_year,
            "generationtime": generation_time,
            "holderName": self.name,
            "initializeCount": "1",
            "luhnCount": "1",
            "luhnOkCount": "1",
            "luhnSameLengthCount": "1",
            "number": self.pan,
            "sjclStrength": "10"
        }

    @staticmethod
    def decode_adyen_public_key(encoded_public_key):
        backend = default_backend()
        key_components = encoded_public_key.split("|")
        public_number = rsa.RSAPublicNumbers(int(key_components[0], 16), int(key_components[1], 16))
        return backend.load_rsa_public_numbers(public_number)

    @staticmethod
    def _encrypt_with_public_key(public_key, plaintext):
        ciphertext = public_key.encrypt(plaintext, padding.PKCS1v15())
        return ciphertext

    @staticmethod
    def _generate_aes_key():
        return AESCCM.generate_key(256)

    @staticmethod
    def _encrypt_with_aes_key(aes_key, nonce, plaintext):
        cipher = AESCCM(aes_key, tag_length=8)
        ciphertext = cipher.encrypt(nonce, plaintext, None)
        return ciphertext

    @staticmethod
    def _generate_nonce():
        return urandom(12)

    def run(self):
        valid = luhn.verify(self.pan)
        if valid is False:
            return False
        else:
            pass
        cse = self.generate_adyen_nonce()
        return cse