db = db.getSiblingDB('ComputerVision');
db.createUser(
  {
    user: 'octa',
    pwd: 'octa',
    roles: [{ role: 'readWrite', db: 'OCTA' }],
  },
);
let dbs = ["Collection1", "collection2"];
for (let i = 0; i < dbs.length; i++){
    db.createCollection(dbs[i]);
};