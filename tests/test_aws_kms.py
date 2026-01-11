import unittest

from aws_sim.kms import KmsKey


class TestKms(unittest.TestCase):
    def test_encrypt_decrypt_roundtrip(self):
        key = KmsKey("key-1", "alias/test")
        ciphertext = key.encrypt(b"secret", {"purpose": "test"})
        plaintext = key.decrypt(ciphertext, {"purpose": "test"})
        self.assertEqual(plaintext, b"secret")


if __name__ == "__main__":
    unittest.main()
