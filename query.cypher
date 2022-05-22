//- Create new node with label:
create (n:User {name:'Alexa'});
create (n:User {name:'Bob'});
create (n:User {name:'Michael'});
create (n:User {name:'Ashley'});
create (n:User {name:'Thomas'});

//- Create Career-User relationship:
MATCH (a:User), (b:Career) WHERE a.name = 'Alexa' AND b.creTitle = 'Tester' CREATE (a)-[r:HAS_OBJECTIVE]->(b);
MATCH (a:User), (b:Career) WHERE a.name = 'Bob' AND b.creTitle = 'Data Analysts' CREATE (a)-[r:HAS_OBJECTIVE]->(b);
MATCH (a:User), (b:Career) WHERE a.name = 'Michael' AND b.creTitle = 'Mobile Developer' CREATE (a)-[r:HAS_OBJECTIVE]->(b);
MATCH (a:User), (b:Career) WHERE a.name = 'Ashley' AND b.creTitle = 'Backend Developer' CREATE (a)-[r:HAS_OBJECTIVE]->(b);
MATCH (a:User), (b:Career) WHERE a.name = 'Thomas' AND b.creTitle = 'Frontend Developer' CREATE (a)-[r:HAS_OBJECTIVE]->(b);

//- Create User-LO relationship for User "Bob" that describe user has LOs:
MATCH (a:User), (b:Knowledge) WHERE a.name = 'Bob' AND (b.value = 'bi' or b.value='statistic' or b.value = 'machine learning' or b.value = 'reporting')
CREATE (a)-[r:HAS_KNOWLEDGE{Level:1}]->(b);
MATCH (a:User), (b:Tool) WHERE a.name = 'Bob' AND (b.value = 'SAS' or b.value = 'tableau')
CREATE (a)-[r:HAS_TOOL{Level:1}]->(b);
MATCH (a:User), (b:ProgramingLanguage) WHERE a.name = 'Bob' AND b.value = 'SQL'
CREATE (a)-[r:HAS_PROGRAMINGLANGUAGE{Level:1}]->(b);
MATCH (a:User), (b:Platform) WHERE a.name = 'Bob' AND b.value = 'aws'
CREATE (a)-[r:HAS_PLATFORM{Level:1}]->(b);
MATCH (a:User), (b:Framework) WHERE a.name = 'Bob' AND (b.value = 'spark' or b.value = 'pandas')
CREATE (a)-[r:HAS_FRAMEWORK{Level:1}]->(b);

//- Create relationship indicate from User-Career and Career-LO:
Match (u: User {name:'Bob'})
Match (c: Career{creTitle:'Data Analysts'})
Match (u)-[ru:HAS_TOOL]->(ku:Tool)<-[rcc:NEED_TOOL]-(c)
Where ((ru.Level < rcc.Level) )
merge (u)-[:NEED_TOOL{Level:rcc.Level}]->(ku);
Match (u: User {name:'Bob'})
Match (c: Career{creTitle:'Data Analysts'})
match (c)-[rc:NEED_TOOL]->(kc)
Where not (u)-[:HAS_TOOL]->(kc)
merge (u)-[:NEED_TOOL{Level:rc.Level}]->(kc);
Match (u: User {name:'Bob'})
Match (c: Career{creTitle:'Data Analysts'})
Match (u)-[ru:HAS_KNOWLEDGE]->(ku)<-[rcc:NEED_KNOWLEDGE]-(c)
Where ((ru.Level < rcc.Level) )
merge (u)-[:NEED_KNOWLEDGE{Level:rcc.Level}]->(ku);
Match (u: User {name:'Bob'})
Match (c: Career{creTitle:'Data Analysts'})
match (c)-[rc:NEED_KNOWLEDGE]->(kc)
Where not (u)-[:HAS_KNOWLEDGE]->(kc)
merge (u)-[:NEED_KNOWLEDGE{Level:rc.Level}]->(kc);
Match (u: User {name:'Bob'})
Match (c: Career{creTitle:'Data Analysts'})
Match (u)-[ru:HAS_PLATFORM]->(ku)<-[rcc:NEED_PLATFORM]-(c)
Where ((ru.Level < rcc.Level) )
merge (u)-[:NEED_PLATFORM{Level:rcc.Level}]->(ku);
Match (u: User {name:'Bob'})
Match (c: Career{creTitle:'Data Analysts'})
match (c)-[rc:NEED_PLATFORM]->(kc)
Where not (u)-[:HAS_PLATFORM]->(kc)
merge (u)-[:NEED_PLATFORM{Level:rc.Level}]->(kc);
Match (u: User {name:'Bob'})
Match (c: Career{creTitle:'Data Analysts'})
Match (u)-[ru:HAS_FRAMEWORK]->(ku)<-[rcc:NEED_FRAMEWORK]-(c)
Where ((ru.Level < rcc.Level) )
merge (u)-[:NEED_FRAMEWORK{Level:rcc.Level}]->(ku);
Match (u: User {name:'Bob'})
Match (c: Career{creTitle:'Data Analysts'})
match (c)-[rc:NEED_FRAMEWORK]->(kc)
Where not (u)-[:HAS_FRAMEWORK]->(kc)
merge (u)-[:NEED_FRAMEWORK{Level:rc.Level}]->(kc);
Match (u: User {name:'Bob'})
Match (c: Career{creTitle:'Data Analysts'})
Match (u)-[ru:HAS_PROGRAMINGLANGUAGE]->(ku)<-[rcc:NEED_PROGRAMINGLANGUAGE]-(c)
Where ((ru.Level < rcc.Level) )
merge (u)-[:NEED_PROGRAMINGLANGUAGE{Level:rcc.Level}]->(ku);
Match (u: User {name:'Bob'})
Match (c: Career{creTitle:'Data Analysts'})
match (c)-[rc:NEED_PROGRAMINGLANGUAGE]->(kc)
Where not (u)-[:HAS_PROGRAMINGLANGUAGE]->(kc)
merge (u)-[:NEED_PROGRAMINGLANGUAGE{Level:rc.Level}]->(kc);

//- Get all LOs that User need:
Match (u:User{name:'Bob'})-[r]->(k) Where type(r) =~ 'NEED_.*' Return u, r, k;

//- Get all User-LO contains need and has relationship of "Bob":
Match (u:User{name:'Bob'})-[r]->(lo1)
Match (u)-[r2]->(lo2)
Where type(r)=~'NE.*' and type(r2)=~'HA.*' and type(r2) <> 'HAS_OBJECTIVE'
Return u, r2, r, lo1, lo2;

//- Calculate similarity of User "Bob" and Courses by Jaccard algorithm:
MATCH (p1:User{name:'Bob'})-[ru]-(e1)
where type(ru) =~ 'NEED_.*'
WITH p1, collect(id(e1)) AS p1entity_type
MATCH (p2:Course)-[rc]-(e2) WHERE type(rc) =~ 'TEACH_.*'
WITH p1, p1entity_type, p2, collect(id(e2)) AS p2entity_type
where gds.similarity.jaccard(p1entity_type, p2entity_type) > 0
RETURN p1.name AS User,
p2.crsName AS Course, p2.crsLink AS link,
gds.similarity.jaccard(p1entity_type, p2entity_type) AS similarity
ORDER BY similarity DESC;