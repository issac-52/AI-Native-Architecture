import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import benchmark_runnable as benchmark


class RunnableBenchmarkTest(unittest.TestCase):
    def test_all_seven_comparison_profiles_have_real_sources(self):
        self.assertEqual(len(benchmark.PROFILES), 7)
        for profile in benchmark.PROFILES:
            self.assertTrue(benchmark.file_paths(profile), profile)

    def test_scan_visits_every_source_file(self):
        for profile in benchmark.PROFILES:
            result = benchmark.scan(profile, "cancel")
            self.assertEqual(result["files_opened"], len(benchmark.file_paths(profile)))
            self.assertGreater(result["bytes_read"], 0)

    def test_fingerprints_are_stable(self):
        for profile in benchmark.PROFILES:
            files = benchmark.file_paths(profile)
            self.assertEqual(benchmark.fingerprints(files), benchmark.fingerprints(files))


if __name__ == "__main__":
    unittest.main()
