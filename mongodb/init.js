db = db.getSiblingDB('OCTA');
db.createUser(
  {
    user: 'octa',
    pwd: 'octa',
    roles: [{ role: 'readWrite', db: 'OCTA' }]
  }
);
let dbs = ["AI_DS", "IT", "CSE"];
for (let i = 0; i < dbs.length; i++){
    db.createCollection(dbs[i]);
};