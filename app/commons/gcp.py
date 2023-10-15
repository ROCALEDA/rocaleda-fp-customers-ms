import asyncio
import os
from google.cloud import pubsub_v1
from google.oauth2.service_account import Credentials
from google.pubsub_v1 import PullRequest
from typing import Callable

# opcional
creds = Credentials.from_service_account_info(
    {
        "type": os.environ["GOOGLE_CLOUD_TYPE"],
        "project_id": os.environ["GOOGLE_CLOUD_PROJECT"],
        "private_key_id": os.environ["GOOGLE_CLOUD_PRIVATE_KEY_ID"],
        "private_key": os.environ["GOOGLE_CLOUD_PRIVATE_KEY"],
        "client_email": os.environ["GOOGLE_CLOUD_CLIENT_EMAIL"],
        "client_id": os.environ["GOOGLE_CLOUD_CLIENT_ID"],
        "auth_uri": os.environ["GOOGLE_CLOUD_AUTH_URI"],
        "token_uri": os.environ["GOOGLE_CLOUD_TOKEN_URI"],
        "auth_provider_x509_cert_url": os.environ[
            "GOOGLE_CLOUD_AUTH_PROVIDER_X509_CERT_URL"
        ],
        "client_x509_cert_url": os.environ["GOOGLE_CLOUD_CLIENT_X509_CERT_URL"],
    }
)

# create_customer_sub = pubsub_v1.SubscriberClient(credentials=creds)
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
        pull_request = PullRequest(subscription=subscription_path, max_messages=10)
        response = subscriber.pull(request=pull_request)

        for received_message in response.received_messages:
            try:
                await handler(received_message.message.data)
                subscriber.acknowledge(
                    subscription=subscription_path, ack_ids=[received_message.ack_id]
                )
            except Exception as e:
                print(f"Error processing message: {e}")

        await asyncio.sleep(15)
