import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import benchmark_discovery as bench


class DiscoveryBenchmarkTest(unittest.TestCase):
    def test_source_files_exist(self):
        self.assertEqual(len(bench.SOURCE), 7)
        self.assertTrue(all(path.is_file() for path in bench.SOURCE.values()))

    def test_all_profiles_are_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            bench.prepare(Path(tmp))
            profile_payloads = []
            for profile in bench.PROFILES:
                mappings = bench.PROFILES[profile]
                payloads = {key: (Path(tmp) / profile / path).read_bytes()
                            for key, path in mappings.items()}
                self.assertEqual(set(payloads), set(bench.SOURCE))
                profile_payloads.append(payloads)
            for payload in profile_payloads[1:]:
                self.assertEqual(payload, profile_payloads[0])

    def test_keyword_matches_equal_across_layouts(self):
        with tempfile.TemporaryDirectory() as tmp:
            bench.prepare(Path(tmp))
            for query in bench.QUERIES:
                rows = [bench.scan(Path(tmp) / profile, query)
                        for profile in bench.PROFILES]
                for field in ("files_opened", "bytes_read", "matching_files", "occurrences"):
                    self.assertEqual(len({row[field] for row in rows}), 1, (query, field))


if __name__ == "__main__":
    unittest.main()
