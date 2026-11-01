# Customer 360 RAG Demonstration

Training project for three patterns using Amazon Neptune, Amazon Bedrock and Python:
1. Knowledge Graph RAG: natural language -> SPARQL -> Neptune -> grounded answer.
2. GraphRAG: start from a customer and traverse connected graph entities.
3. Hybrid Graph + Vector RAG: combine Neptune facts with semantically retrieved document chunks.

## Environment

This project is configured for the AWS environment prepared for this demo:
- Region: `ap-south-1`
- Neptune: private writer endpoint in the `.env.example`
- Bedrock chat profile: `apac.amazon.nova-micro-v1:0`
- Bedrock embeddings: `amazon.titan-embed-text-v2:0`

Run it in the **VPC-connected CloudShell** environment that can reach Neptune and Bedrock. Your ordinary Windows machine may not be able to reach the private Neptune endpoint directly.

The two text files in `data/documents/` are fictional training documents, not real customer contracts or support records. Hybrid RAG requires access to the configured Titan embedding model in Bedrock.

## Setup

Create `.env` from `.env.example` and adjust only if needed.

Windows PowerShell:
```powershell
Copy-Item .env.example .env
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

VPC CloudShell:
```bash
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run in VPC-connected CloudShell

```bash
python scripts/check_connectivity.py
python scripts/test_neptune_query.py
```

Knowledge Graph RAG:
```bash
python -m app.main kg --question "Show customers with their IDs, names and email addresses."
```

GraphRAG:
```bash
python -m app.main graph --customer-id C1001
```

Hybrid Graph + Vector RAG:
```bash
python -m app.main hybrid --customer-id C1001 --question "What contractual terms and support issues are relevant to this customer?"
```

## VS Code -> GitHub -> CloudShell workflow

1. Download and unzip this folder.
2. In VS Code choose **File -> Open Folder** and select `customer360-rag-demo`.
3. Create an empty GitHub repository named `customer360-rag-demo` (do not initialize it with a README).
4. In the VS Code terminal:

```powershell
git init
git add .
git commit -m "Initial Customer 360 RAG demonstration"
git branch -M main
git remote add origin https://github.com/YOUR-GITHUB-USERNAME/customer360-rag-demo.git
git push -u origin main
```

Replace `YOUR-GITHUB-USERNAME`. Complete GitHub authentication if prompted. Never commit `.env` or AWS credentials.

5. Open the VPC-connected CloudShell and clone the repository:

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/customer360-rag-demo.git
cd customer360-rag-demo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

6. Run the connectivity checks and demos above.

For later code updates, commit and push from VS Code:
```powershell
git add .
git commit -m "Update GraphRAG demo"
git push
```

Then in CloudShell:
```bash
cd customer360-rag-demo
git pull origin main
```
Run the updated command again.

## What the code does

- `app/aws_clients.py`: signs Neptune requests with AWS SigV4 (`neptune-db`); calls Bedrock Converse and Titan embeddings.
- `app/retrieval/kg_rag.py`: asks Bedrock for a read-only SELECT query, executes it, and asks Bedrock to answer from returned rows.
- `app/retrieval/graph_rag.py`: retrieves literal facts from a customer and its directly connected entities.
- `app/retrieval/hybrid_rag.py`: embeds the question and document chunks, ranks chunks by cosine similarity, retrieves graph facts, and combines both sources.
- `scripts/`: connectivity and SPARQL smoke tests.

## Important limitations

This is a teaching scaffold, not a production system. The NL-to-SPARQL guard is a basic safeguard, not a complete query-security layer. Inspect generated SPARQL during the demo. Production use needs IAM least privilege, authorization, query governance, monitoring, privacy controls, evaluation and automated tests.

In this data model, a Customer links to a Person or Organization through `c360:hasParty`. Person names are stored as `c360:fullName`; organization names are stored as `c360:legalName`. Do not assume names are direct Customer properties.

If Neptune times out, verify that you are in the VPC-connected CloudShell, not ordinary CloudShell. If Bedrock returns access/model errors, verify IAM permissions and model availability in `ap-south-1`. If Titan embedding invocation fails, enable `amazon.titan-embed-text-v2:0` or change `BEDROCK_EMBEDDING_MODEL_ID` to an embedding model enabled in your account.
