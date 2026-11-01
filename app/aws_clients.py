import json
import requests
import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from app.config import AWS_REGION, NEPTUNE_ENDPOINT, BEDROCK_CHAT_MODEL_ID, BEDROCK_EMBEDDING_MODEL_ID

_session = boto3.Session(region_name=AWS_REGION)
_bedrock = _session.client("bedrock-runtime", region_name=AWS_REGION)

def execute_sparql(query: str) -> dict:
    credentials = _session.get_credentials()
    if credentials is None:
        raise RuntimeError("No AWS credentials found in the active credential chain.")
    frozen = credentials.get_frozen_credentials()
    url = f"{NEPTUNE_ENDPOINT}/sparql"
    body = {"query": query}
    request = AWSRequest(method="POST", url=url, data=body,
                         headers={"Content-Type": "application/x-www-form-urlencoded"})
    SigV4Auth(frozen, "neptune-db", AWS_REGION).add_auth(request)
    response = requests.post(url, data=body, headers=dict(request.headers.items()), timeout=45)
    response.raise_for_status()
    return response.json()

def converse(system_prompt: str, user_prompt: str, max_tokens: int = 900) -> str:
    response = _bedrock.converse(
        modelId=BEDROCK_CHAT_MODEL_ID,
        system=[{"text": system_prompt}],
        messages=[{"role": "user", "content": [{"text": user_prompt}]}],
        inferenceConfig={"maxTokens": max_tokens, "temperature": 0.1},
    )
    return response["output"]["message"]["content"][0]["text"]

def embed_text(text: str) -> list[float]:
    response = _bedrock.invoke_model(
        modelId=BEDROCK_EMBEDDING_MODEL_ID,
        body=json.dumps({"inputText": text}),
        contentType="application/json",
        accept="application/json",
    )
    return json.loads(response["body"].read())["embedding"]
