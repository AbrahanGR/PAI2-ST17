import hmac
import hashlib
import unittest
import secrets
import time

class TestIntegrity(unittest.TestCase):
    def setUp(self):
        self.secret_key = secrets.token_bytes(32)
        self.message = "Transazione: 23249 67856 200".encode()

    def generate_mac(self, message):
        return hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()

    def test_mac_integrity(self):
        mac = self.generate_mac(self.message)
        altered_message = "Transazione: 23250 67856 200".encode()
        self.assertNotEqual(mac, self.generate_mac(altered_message))
        self.assertEqual(mac, self.generate_mac(self.message))

class TestReplayAttack(unittest.TestCase):
    def setUp(self):
        self.nonce = secrets.token_hex(16)
        self.timestamp = int(time.time())
        self.message = f"Transazione: 23249 67856 200 NONCE: {self.nonce} TIMESTAMP: {self.timestamp}"

    def test_replay_protection(self):
        replay_nonce = self.nonce
        replay_timestamp = self.timestamp
        self.assertEqual(self.nonce, replay_nonce)
        self.assertEqual(self.timestamp, replay_timestamp)
        time.sleep(1)
        replay_timestamp = int(time.time())
        self.assertNotEqual(self.timestamp, replay_timestamp)

class TestPasswordIntegrity(unittest.TestCase):
    def setUp(self):
        self.password = "user_secure_password"
        self.salted_password = self.password + "some_salt"
        self.stored_hash = hashlib.sha256(self.salted_password.encode()).hexdigest()

    def test_password_integrity(self):
        entered_password = "user_secure_password"
        salted_entered_password = entered_password + "some_salt"
        entered_hash = hashlib.sha256(salted_entered_password.encode()).hexdigest()
        self.assertEqual(self.stored_hash, entered_hash)

class TestKeyDerivation(unittest.TestCase):
    def setUp(self):
        self.password = "secure_password"
        self.salt = secrets.token_bytes(16)

    def test_key_derivation(self):
        derived_key1 = hashlib.pbkdf2_hmac('sha256', self.password.encode(), self.salt, 100000)
        derived_key2 = hashlib.pbkdf2_hmac('sha256', self.password.encode(), self.salt, 100000)
        self.assertEqual(derived_key1, derived_key2)

if __name__ == '__main__':
    unittest.main()
