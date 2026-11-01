import os
from dotenv import load_dotenv

load_dotenv()
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")
NEPTUNE_ENDPOINT = os.getenv("NEPTUNE_ENDPOINT", "https://db-neptune-1.cluster-c5koq6icadhd.ap-south-1.neptune.amazonaws.com:8182").rstrip("/")
BEDROCK_CHAT_MODEL_ID = os.getenv("BEDROCK_CHAT_MODEL_ID", "apac.amazon.nova-micro-v1:0")
BEDROCK_EMBEDDING_MODEL_ID = os.getenv("BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0")
C360 = os.getenv("CUSTOMER360_NAMESPACE", "https://abhigyaailab.com/ontology/customer360#")
