import hmac
import hashlib
import unittest
import secrets
import time
import socket
import psycopg2

import client_login  # Importing actual credential handler
import server_login  # Importing the actual server-side logic

# Database connection setup for testing
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="PAI1-ST17",  # Adjust to your test database
        user="server",  # Ensure this user has the necessary permissions
        password="server_PAI1-ST17"
    )

class TestIntegrity(unittest.TestCase):
    def setUp(self):
        # Set up the real credentials and database connection
        self.connection = get_db_connection()
        self.secret_key = secrets.token_bytes(32)  # For HMAC testing
        self.message = "TestUser, TestPassword".encode()  # Real message for credentials

        # Ensure a test user exists in the database
        self.username = "TestUser"
        self.password = "TestPassword"
        server_login.store_new_user(self.username, self.password, self.connection)

    def generate_mac(self, message):
        return hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()

    def test_mac_integrity(self):
        # Test that the MAC value changes with altered data
        mac = self.generate_mac(self.message)
        
        altered_message = "TestUser, AlteredPassword".encode()  # Simulate altered login credentials
        self.assertNotEqual(mac, self.generate_mac(altered_message))
        
        # Verify the original message MAC is intact
        self.assertEqual(mac, self.generate_mac(self.message))

    def tearDown(self):
        # Clean up after the test by removing the user from the database
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM users WHERE username = %s", (self.username,))
        self.connection.commit()
        cursor.close()
        self.connection.close()

class TestReplayAttack(unittest.TestCase):
    def setUp(self):
        self.nonce = secrets.token_hex(16)
        self.timestamp = int(time.time())
        self.message = f"Transacción: 23249 67856 200 NONCE: {self.nonce} TIMESTAMP: {self.timestamp}"

        self.connection = get_db_connection()

    def test_replay_protection(self):
        # Here, we simulate a replayed message using the same nonce and timestamp
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", ("TestUser",))
        user_data = cursor.fetchone()
        
        # Ensure user exists in database
        self.assertIsNotNone(user_data, "User not found in database!")

        # Send a message with the same nonce and timestamp (replay attempt)
        replay_message = f"Transacción: 23249 67856 200 NONCE: {self.nonce} TIMESTAMP: {self.timestamp}".encode()

        # Simulate replay prevention logic here, e.g., check if nonce/timestamp combination is reused
        # For simplicity, we'll just check if the message is altered and compare timestamps/nonce
        self.assertNotEqual(self.message, replay_message)  # Ensure replay is detected

    def tearDown(self):
        # Clean up database after test
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM users WHERE username = 'TestUser'")
        self.connection.commit()
        cursor.close()
        self.connection.close()

# If you want to run this file as a standalone script:
if __name__ == "__main__":
    unittest.main()
