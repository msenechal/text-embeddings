from decouple import config
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase

uri = config('NEO4J_URI')
username = config('NEO4J_USERNAME')
password = config('NEO4J_PASSWORD')

driver = GraphDatabase.driver(uri, auth=(username, password))


query = "MATCH (p:Person) WHERE NOT EXISTS(p.embedding) RETURN p.email AS email, p.firstName as firstName, p.lastName as lastName"
with driver.session() as session:
    result = session.run(query)
    personNode = []
    for record in result:
        personNode.append(record["email"])
        personNode.append(record["firstName"])
        personNode.append(record["lastName"])

# check https://spacy.io/ for embeddings
model = SentenceTransformer('all-mpnet-base-v2')
embeddings = model.encode(personNode)
#print(embeddings)

#UNWIND BEFORE MATCH instead
query = "MATCH (p:Person) WHERE p.email = $email AND p.firstName = $firstName AND p.lastName = $lastName SET e.embedding = $embedding"
with driver.session() as session:
    for email, firstName, lastName, embedding in zip(personNode, embeddings):
        session.run(query, email=email, firstName=firstName, lastName=lastName, embedding=embedding.tolist())

driver.close()