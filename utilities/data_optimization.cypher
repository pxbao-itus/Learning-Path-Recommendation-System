// Remove redundant LO that was not teached by any courses
match(lo)<-[r]-(c:Course) where type(r) =~'TEACH_.*'
with collect(id(lo)) as lo_list, ['Tool','Knowledge','Platform','ProgramingLanguage','Framework'] as skill
match(lo) where labels(lo)[0] in skill and not id(lo) in lo_list detach delete lo;

// Remove relationship REQUIRE if exist both relationship TEACH and REQUIRE between Course and LO
//match (c:Course)-[r]->(lo)<-[r1]-(c)
//where type(r)=~"TEACH.*" and type(r1)=~"REQUIRE.*"
//delete r1;

// Remove label, relationship unnecessary
match (c:Course)-[r]->(x)
where type(r)="COLLABORATE_WITH" or type(r)="TEACH_IN" or type(r)="IS_IN" or type(r)="HAS_LEVEL" or type(r)="BELONG"
detach delete r, x;
match (n)-[r]->(c:Course) where type(r) = 'INCLUDE_COURSE' or type(r) = 'INSTRUCT_BY' detach delete r, n;
// Upgrate property level of TEACH Relationship to 5
match(c:Course)-[r]->(lo) where type(r) =~'TEACH_.*' and type(r) <> 'TEACH_IN'
set r.Level = 5
return c,r,lo;
// Set course fee from NaN to 0.0
match (c:Course)
where TOSTRING(c.crsFee) = 'NaN'
set c.crsFee = 0.0;

