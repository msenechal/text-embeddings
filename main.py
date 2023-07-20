#OLD VERSION, USE generate-embeddings.ipynb INSTEAD
from decouple import config
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase

uri = config('NEO4J_URI')
username = config('NEO4J_USERNAME')
password = config('NEO4J_PASSWORD')

driver = GraphDatabase.driver(uri, auth=(username, password))


query = "MATCH (p:Person) WHERE p.embedding IS NULL RETURN p.email AS email, p.firstName as firstName, p.lastName as lastName LIMIT 500"
with driver.session() as session:
    result = session.run(query)
    personNode = []
    personNodeEmbeddings = []
    for record in result:
        personNode.append((record["email"], record["firstName"], record["lastName"]))

        # check https://spacy.io/ for embeddings
        model = SentenceTransformer('all-mpnet-base-v2')
        embeddings = model.encode(personNode)
        personNodeEmbeddings.extend(embeddings)
        # print(embeddings)

    with driver.session() as session:
        query = """
        UNWIND $data AS data
        MATCH (p:Person)
        WHERE p.email = data.email AND p.firstName = data.firstName AND p.lastName = data.lastName
        SET p.embedding = data.embedding
        """
        data_to_write = [{"email": email, "firstName": firstName, "lastName": lastName, "embedding": embedding.tolist()} for (email, firstName, lastName), embedding in zip(personNode, personNodeEmbeddings)]

        batch_size = 500
        for batch_start in range(0, len(data_to_write), batch_size):
            batch_end = batch_start + batch_size
            batch_data = data_to_write[batch_start:batch_end]
            session.run(query, data=batch_data)

driver.close()