from hatchet_sdk import DurableContext, Hatchet, Context
from datetime import timedelta

import agpyutils.task.models as models

hatchet = Hatchet()

@hatchet.durable_task(name="labor", input_validator=models.Task_UnmanagedLabor)
async def task_unmanaged_labor(input: models.Task_UnmanagedLabor, context: DurableContext) -> dict[str, str]:
    pass
    # try:
    #     revent = context.aio_sleep_for(input.wait_for)
    #     return {"status": "success",}
    # except Exception as e:
    #     print(e)
    #     return {"status": "failed",}