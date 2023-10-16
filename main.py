import asyncio
import uvicorn

from app.commons.gcp import (
    pull_messages,
    create_customer_sub,
    CUSTOMER_CREATION_SUB_PATH,
)
from fastapi import FastAPI
from initializer import Initializer
from app.customer.handlers.customer_handlers import create_customer_handler

app = FastAPI()

instances = Initializer(app)
instances.setup()


@app.on_event("startup")
async def on_startup() -> None:
    asyncio.create_task(
        pull_messages(
            create_customer_sub,
            CUSTOMER_CREATION_SUB_PATH,
            await create_customer_handler(instances.customer_service),
        )
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
