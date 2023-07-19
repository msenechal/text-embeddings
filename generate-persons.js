const { faker } = require('@faker-js/faker');
const fs = require('fs');

const NUM_PERSONS = 1000000;

// Generate persons
const persons = [];
for (let i = 0; i < NUM_PERSONS; i++) {
  const id = faker.datatype.number({ min: 1, max: 100000000 }); 
  const firstName = faker.name.firstName(); 
  const lastName = faker.name.lastName(); 
  const email = firstName + '.' + lastName + '@' + faker.internet.domainWord() + '.' + faker.internet.domainSuffix();
  const person = {
    id,
    firstName,
    lastName,
    email
  };
  persons.push(person);
}

let personsCsv = '';
persons.forEach(person => {
  personsCsv += `${person.id},${person.firstName},${person.lastName},${person.email}\n`;
});

fs.writeFileSync('persons.csv', personsCsv);