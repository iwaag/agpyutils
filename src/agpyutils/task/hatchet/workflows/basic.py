from hatchet_sdk import DurableContext, Hatchet, Context
from datetime import timedelta

import agpyutils.task.models as models

hatchet = Hatchet()

@hatchet.durable_task(name="labor", input_validator=models.Task_UnmanagedLabor)
async def task_unmanaged_labor(input: models.Task_UnmanagedLabor, context: DurableContext) -> dict[str, str]:
    print("dummy")

@hatchet.durable_task(name="labor_auth", input_validator=models.Task_UnmanagedLabor)
async def task_labor_oath(input: models.Task_UnmanagedLabor, context: DurableContext) -> dict[str, str]:
    print("dummy")