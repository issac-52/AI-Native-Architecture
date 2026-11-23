import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import agent_discovery_trial as agent


class AgentRecorderTests(unittest.TestCase):
    def test_gold_exists_and_paths_are_relative(self):
        for profile in agent.GOLD:
            for file in agent.GOLD[profile]:
                self.assertTrue((agent.ROOT / file).is_file(), (profile, file))
                self.assertEqual(agent.normalize_paths(["./" + file]), {file})

    def test_scoring_exact_and_partial(self):
        selected = agent.GOLD["layered"]
        self.assertEqual(agent.score(selected, selected)["f1"], 1)
        self.assertEqual(agent.score(selected[:1], selected)["recall"], 0.5)
        self.assertEqual(agent.score([], selected)["all_loci_found"], 0)

    def test_token_usage_and_unique_tool_calls(self):
        with tempfile.TemporaryDirectory() as folder:
            trace = Path(folder) / "trace.jsonl"
            events = [
                {"type": "turn.started"},
                {"type": "item.started", "item": {"id": "1", "type": "command_execution"}},
                {"type": "item.completed", "item": {"id": "1", "type": "command_execution"}},
                {"type": "turn.completed", "usage": {
                    "input_tokens": 100, "cached_input_tokens": 25, "output_tokens": 40
                }},
            ]
            trace.write_text("\n".join(json.dumps(e) for e in events), encoding="utf-8")
            parsed = agent.parse_codex_events(trace)
            self.assertTrue(parsed["turn_completed"])
            self.assertEqual(parsed["tool_calls"], 1)
            self.assertEqual(parsed["input_tokens"], 100)
            self.assertEqual(parsed["output_tokens"], 40)

    def test_dry_run_fixture(self):
        with tempfile.TemporaryDirectory() as folder:
            repo = agent.build_fixture("ai_native", folder)
            self.assertTrue((repo / agent.GOLD["ai_native"][0]).is_file())
            self.assertTrue((repo / agent.GOLD["ai_native"][1]).is_file())
            self.assertTrue((repo / ".git").is_dir())


if __name__ == "__main__":
    unittest.main()
