from abc import abstractmethod
from typing import override

from agpyutils.task.hub import TaskHub
import agpyutils.task.models as models
import agpyutils.task.hatchet.workflows.basic as workflows_basic
from hatchet_sdk import Hatchet
import asyncio

class TaskHub_Hatchet(TaskHub):
    def __init__(self):
        super().__init__()

    @override
    def request_unmanaged_labor(self, task: models.Task_UnmanagedLabor):
        workflows_basic.task_unmanaged_labor.run_no_wait(input=task)

