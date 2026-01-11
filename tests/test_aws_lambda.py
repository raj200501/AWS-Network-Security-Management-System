import unittest

from aws_sim.lambda_runtime import LambdaRuntime, LambdaFunction


def handler(event, context):
    return {"status": "ok", "payload": event.get("value")}


class TestLambdaRuntime(unittest.TestCase):
    def test_invoke_records_invocation(self):
        runtime = LambdaRuntime()
        runtime.register(LambdaFunction(name="handler", handler=handler))
        result = runtime.invoke("handler", {"value": 5})
        self.assertEqual(result["payload"], 5)
        invocations = runtime.invocations()
        self.assertEqual(len(invocations), 1)
        self.assertEqual(invocations[0].function_name, "handler")


if __name__ == "__main__":
    unittest.main()
