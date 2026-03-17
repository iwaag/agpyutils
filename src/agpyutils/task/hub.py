from abc import ABC, abstractmethod

import agpyutils.task.models as models

class TaskHub(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def request_unmanaged_labor(self, task: models.Task_UnmanagedLabor):
        pass

    @abstractmethod
    def request_labor_auth(self, task: models.Task_UnmanagedLabor):
        pass