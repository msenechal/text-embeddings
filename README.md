# text-embeddings
text-embeddings

# generate emails csv
```shell
npm i @faker-js/faker fs
node generate-persons.js
```

# for loading + python
```shell
source .env
```

# load emails into AuraDS
```shell
cypher-shell -a $NEO4J_URI -u $NEO4J_USERNAME -p $NEO4J_PASSWORD -f load-persons.cypher
```

# run embeddings
```shell
pip install -U neo4j sentence_transformers python-decouple
python main.py
```

# todo
Move to colab or panda using dataframes