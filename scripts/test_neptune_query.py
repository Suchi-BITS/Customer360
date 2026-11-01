from app.aws_clients import execute_sparql

query = "SELECT (COUNT(*) AS ?tripleCount) WHERE { ?s ?p ?o }"
print("Neptune SPARQL response:")
print(execute_sparql(query))
