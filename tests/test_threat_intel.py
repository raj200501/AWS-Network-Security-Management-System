import unittest
from pathlib import Path

from nsms.threat_intel import ThreatIntelStore


class TestThreatIntel(unittest.TestCase):
    def test_threat_intel_lookup(self):
        store = ThreatIntelStore.load(Path("data/threat_intel.json"))
        indicator = store.check_ip("198.51.100.99")
        self.assertIsNotNone(indicator)
        self.assertEqual(indicator.severity, "high")


if __name__ == "__main__":
    unittest.main()
