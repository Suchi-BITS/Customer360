import socket
import boto3
from urllib.parse import urlparse
from app.config import AWS_REGION, NEPTUNE_ENDPOINT, BEDROCK_CHAT_MODEL_ID

print("Region:", AWS_REGION)
# Avoid an STS call here: this VPC demo environment may not have an STS VPC endpoint.
session = boto3.Session(region_name=AWS_REGION)
print("AWS credentials available:", session.get_credentials() is not None)
host = urlparse(NEPTUNE_ENDPOINT).hostname
print("Neptune DNS:", socket.gethostbyname_ex(host))
client = session.client("bedrock-runtime", region_name=AWS_REGION)
result = client.converse(
    modelId=BEDROCK_CHAT_MODEL_ID,
    messages=[{"role": "user", "content": [{"text": "Reply exactly CONNECTIVITY_OK"}]}],
    inferenceConfig={"maxTokens": 30, "temperature": 0},
)
print("Bedrock:", result["output"]["message"]["content"][0]["text"])
