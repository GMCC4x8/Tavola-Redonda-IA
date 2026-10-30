import unittest

from roundtable import AGENTS, run_roundtable, to_markdown


class TestRoundtable(unittest.TestCase):
    def test_seven_calls_and_report(self):
        calls = []

        def fake_ask(role, instructions, prompt, model):
            calls.append((role, model, prompt))
            return {"text": f"Análise de {role}", "prompt_tokens": 22, "generated_tokens": 12}

        result = run_roundtable(
            question="Devemos investir em automação?",
            data_context="Receita média: 100.",
            ask_fn=fake_ask,
            model="modelo-falso",
        )
        self.assertEqual(len(calls), 7)
        self.assertEqual(len(result["events"]), 7)
        self.assertEqual(result["model"], "modelo-falso")
        self.assertEqual(sum(e["generated_tokens"] for e in result["events"]), 84)
        self.assertIn("Moderator AI", result["events"][-1]["agent"])
        self.assertIn("Devemos investir", to_markdown(result))
        self.assertEqual(len(AGENTS), 3)

    def test_empty_question(self):
        with self.assertRaises(ValueError):
            run_roundtable(" ", ask_fn=lambda *args: {})


if __name__ == "__main__":
    unittest.main()
