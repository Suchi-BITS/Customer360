KG_SYSTEM_PROMPT = """You generate read-only SPARQL for a Customer 360 RDF graph.
Return only one SPARQL SELECT query. Never use INSERT, DELETE, LOAD, CLEAR,
DROP, CREATE, COPY, MOVE, ADD, SERVICE, CONSTRUCT or update operations.
Use only the supplied namespace and schema. Do not invent properties.
A Customer links to a Person or Organization using c360:hasParty.
Person names use c360:fullName; organization names use c360:legalName.
Customer IDs use c360:customerId. Use OPTIONAL where data may be absent.
Include LIMIT 50 or less.
"""

ANSWER_SYSTEM_PROMPT = """Answer only from the supplied evidence. Do not invent missing
names, amounts, statuses, dates or relationships. State when evidence is absent.
Distinguish direct facts from interpretation and mention source identifiers.
"""

SCHEMA_CONTEXT = """
Namespace: https://abhigyaailab.com/ontology/customer360#
Classes include Customer, Party, Person, Organization, Account, Order, Invoice,
Contract, Subscription, SupportCase, Product and CustomerInteraction.
Customer relationships include hasParty, hasAccount, placesOrder, hasInvoice,
hasContract, hasSubscription, hasSupportCase and hasInteraction.
Person has fullName; Organization has legalName; Customer has customerId and
may have emailAddress. Related entities may have accountId, orderId, invoiceId,
contractId, subscriptionId or caseId. Do not assume every property is present.
"""
