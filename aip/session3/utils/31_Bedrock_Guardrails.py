"""
Shows how to use a guardrail with the ConverseStream operation.
"""

import logging
import json
import boto3


from botocore.exceptions import ClientError


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def stream_conversation(bedrock_client,
                    model_id,
                    messages,
                    guardrail_config):
    """
    Sends messages to a model and streams the response.
    Args:
        bedrock_client: The Boto3 Bedrock runtime client.
        model_id (str): The model ID to use.
        messages (JSON) : The messages to send.
        guardrail_config : Configuration for the guardrail.


    Returns:
        Nothing.

    """

    logger.info("Streaming messages with model %s", model_id)

    response = bedrock_client.converse_stream(
        modelId=model_id,
        messages=messages,
        guardrailConfig=guardrail_config
    )

    stream = response.get('stream')
    if stream:
        for event in stream:

            if 'messageStart' in event:
                print(f"\nRole: {event['messageStart']['role']}")

            if 'contentBlockDelta' in event:
                print(event['contentBlockDelta']['delta']['text'], end="")

            if 'messageStop' in event:
                print(f"\nStop reason: {event['messageStop']['stopReason']}")

            if 'metadata' in event:
                metadata = event['metadata']
                if 'trace' in metadata:
                    print("\nAssessment")
                    print(json.dumps(metadata['trace'], indent=4))


def main():
    """
    Entrypoint for streaming message API response example.
    """

    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    # The model to use.
    model_id = "amazon.titan-text-express-v1"

    # The ID and version of the guardrail.
    guardrail_id = "efzsheyu2yvm"
    guardrail_version = "3"

    # Configuration for the guardrail.
    guardrail_config = {
        "guardrailIdentifier": guardrail_id,
        "guardrailVersion": guardrail_version,
        "trace": "enabled",
        "streamProcessingMode" : "sync"
    }

    text = "Create a playlist of heavy metal songs."
  
    # The message for the model and the content that you want the guardrail to assess.
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "text": text,
                },
                {
                    "guardContent": {
                        "text": {
                            "text": text
                        }
                    }
                }
            ]
        }
    ]

    try:
        bedrock_client = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')

        stream_conversation(bedrock_client, model_id, messages,
                        guardrail_config)

    except ClientError as err:
        message = err.response['Error']['Message']
        logger.error("A client error occurred: %s", message)
        print("A client error occured: " +
              format(message))

    else:
        print(
            f"Finished streaming messages with model {model_id}.")


if __name__ == "__main__":
    main()
