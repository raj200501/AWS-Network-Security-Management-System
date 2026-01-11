import unittest

from aws_sim.ecs import EcsService, ContainerDefinition


class TestEcs(unittest.TestCase):
    def test_register_and_run_task(self):
        ecs = EcsService()
        cluster = ecs.create_cluster("default")
        task_def = ecs.register_task_definition(
            "nsms",
            [ContainerDefinition(name="app", image="nsms:latest", cpu=128, memory=256, port_mappings=[8080])],
        )
        task = ecs.run_task(cluster.cluster_arn, task_def.task_definition_arn)
        self.assertEqual(task.status, "RUNNING")


if __name__ == "__main__":
    unittest.main()
