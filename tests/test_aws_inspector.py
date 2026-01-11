import unittest

from aws_sim.inspector import InspectorService


class TestInspector(unittest.TestCase):
    def test_assessment_run(self):
        inspector = InspectorService()
        template = inspector.create_template("baseline", ["cve"])
        run = inspector.start_run(template.template_id)
        inspector.create_finding(run.run_id, "MEDIUM", "Issue", "i-123")
        self.assertEqual(len(inspector.list_findings()), 1)


if __name__ == "__main__":
    unittest.main()
