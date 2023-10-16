import asyncio
import os
from google.cloud import pubsub_v1
from google.pubsub_v1 import PullRequest
from typing import Callable

#variable entorno (docker) - agrega el archivo del service account en la misma ruta que el test
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_.json_credential_file"

create_customer_sub = pubsub_v1.SubscriberClient()

CUSTOMER_CREATION_SUBSCRIPTION_NAME = os.environ[
    "CUSTOMER_CREATION_SUBSCRIPTION_NAME"
]
CUSTOMER_CREATION_SUB_PATH = create_customer_sub.subscription_path(
    os.environ["GOOGLE_CLOUD_PROJECT"], CUSTOMER_CREATION_SUBSCRIPTION_NAME
)


async def pull_messages(
    subscriber: pubsub_v1.SubscriberClient, subscription_path: str, handler: Callable
) -> None:
    while True:
        try:
            pull_request = PullRequest(subscription=subscription_path, max_messages=10)
            response = subscriber.pull(request=pull_request, timeout=5)
        except Exception as e:
            await asyncio.sleep(15)
            continue

        for received_message in response.received_messages:
            try:
                await handler(received_message.message.data)
                subscriber.acknowledge(
                    subscription=subscription_path, ack_ids=[received_message.ack_id]
                )
            except Exception as e:
                print(f"Error processing message: {e}")

        await asyncio.sleep(15)
