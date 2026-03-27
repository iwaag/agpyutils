from abc import abstractmethod
from typing import override

from agpy.task.hub import TaskHub
import agpy.task.models as models
import agpy.task.hatchet.workflows.basic as workflows_basic
from hatchet_sdk import Hatchet, TriggerWorkflowOptions
import asyncio

def unmanaged_labor(task: models.Task_UnmanagedLabor):
    workflows_basic.task_labor_auth.run_no_wait(
        input=task, options=TriggerWorkflowOptions(
            additional_metadata={"user_id": task.meta.user_id, "project_id": task.meta.project_id, "type_id": task.meta.type_id})
    )
class TaskHub_Hatchet(TaskHub):
    def __init__(self):
        super().__init__()

    @override
    def request_unmanaged_labor(self, task: models.Task_UnmanagedLabor):
        unmanaged_labor(task)

    @override
    def request_labor_auth(self, task: models.Task_UnmanagedLabor):
        unmanaged_labor(task)

