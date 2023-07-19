LOAD CSV FROM 'https://raw.githubusercontent.com/msenechal/text-embeddings/main/persons.csv' AS line
MERGE (:Person {firstName: line[1], lastName: line[2], email: line[3]})