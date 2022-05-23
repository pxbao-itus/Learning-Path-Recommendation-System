import os
from email.policy import default
from enum import unique
import json
from os import name
import math

# from io import BytesIO
# from PIL import Image
# from neo4j import GraphDatabase
from neomodel.properties import FloatProperty, EmailProperty, IntegerProperty, DateTimeProperty
import pandas as pd
# from neomodel import config
from neomodel import Q, db
# config.DATABASE_URL ='bolt://neo4j:1@localhost:7687'
# Create your neo4j_connection here.
from neomodel import StructuredNode, StringProperty, DateProperty, RelationshipTo, RelationshipFrom, FloatProperty
from neomodel import StructuredRel

# Tao connection


#########################################################################
# Khoi tao cac class
class User(StructuredNode):
    uid = IntegerProperty()
    name = StringProperty()
    education = StringProperty()
    level = RelationshipTo("Level", "HAS_LEVEL")
    current_career = RelationshipTo("Career", "HAS_CURRENT_CAREER")
    hope_career = RelationshipTo("Career", "HAS_HOPE_CAREER")
    enroll = RelationshipTo("Course", "ENROLL")
    complete = RelationshipTo("Course", "COMPLETE")
    knowledge = RelationshipTo("Knowledge", "HAS_KNOWLEDGE")
    tool = RelationshipTo("Tool", "HAS_TOOL")
    platform = RelationshipTo("Platform", "HAS_PLATFORM")
    framework = RelationshipTo("Framework", "HAS_FRAMEWORK")
    programinglanguage = RelationshipTo("ProgramingLanguage", "HAS_PROGRAMINGLANGUAGE")

    def get_name(self):
        return {
            "uid": self.uid,
            "name": self.name,
        }

    def to_json(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "level": list(map(lambda n: n.to_json(), self.level)),
            "current_career": list(map(lambda n: n.to_json(), self.current_career)),
            "hope_career": list(map(lambda n: n.to_json(), self.hope_career)),
            "knowledge": list(map(lambda n: n.to_json(), self.knowledge)),
            "platform": list(map(lambda n: n.to_json(), self.platform)),
            "programinglanguage": list(map(lambda n: n.to_json(), self.programinglanguage)),
            "tool": list(map(lambda n: n.to_json(), self.tool)),
            "framework": list(map(lambda n: n.to_json(), self.framework)),
        }

    def get_enroll(self):
        return {
            "enroll": list(map(lambda n: n.to_json(), self.enroll)),
        }

    def get_complete(self):
        return {
            "complete": list(map(lambda n: n.to_json(), self.complete)),
        }


class Subject(StructuredNode):
    Name = StringProperty()
    Create_Date = DateTimeProperty()
    Update_Date = DateTimeProperty()
    course = RelationshipFrom("Course", "BELONG")

    def to_json(self):
        return {
            "id": self.id,
            "value": self.Name
        }

    def export(self):
        return self.Name


# Relationship prop model
class Index(StructuredRel):
    Index = IntegerProperty()


class Need(StructuredRel):
    Level = IntegerProperty(default=1)
    Prob = FloatProperty(default=0.5)


class Require(StructuredRel):
    Level = IntegerProperty(default=1)


class Teach(StructuredRel):
    Level = IntegerProperty(default=1)


class Website(StructuredNode):
    webName = StringProperty()
    course = RelationshipFrom("Course", "IS_IN")

    def to_json(self):
        return {
            "id": self.id,
            "value": self.webName
        }

    def export(self):
        return self.webName


class Organization(StructuredNode):
    orgName = StringProperty()
    instructor = RelationshipFrom("Instructor", "WORK_AT")
    course = RelationshipFrom("Course", "COLLABORATE_WITH")

    def to_json(self):
        return {
            "id": self.id,
            "value": self.orgName
        }

    def export(self):
        return self.orgName


class Instructor(StructuredNode):
    insName = StringProperty()
    organization = RelationshipTo("Organization", "WORK_AT")
    course = RelationshipTo("Course", "INSTRUCT_BY")

    def to_json(self):
        return {
            "id": self.id,
            "value": self.insName
        }

    def export(self):
        return self.insName


class SubTitle(StructuredNode):
    subLanguage = StringProperty()
    course = RelationshipFrom("Course", "TEACH_IN")

    def to_json(self):
        return {
            "id": self.id,
            "value": self.subLanguage
        }

    def export(self):
        return self.subLanguage


class Level(StructuredNode):
    levName = StringProperty()
    course = RelationshipFrom("Course", "HAS_LEVEL")

    def to_json(self):
        return {
            "id": self.id,
            "value": self.levName
        }

    def export(self):
        return self.levName


class Course(StructuredNode):
    crsFee = FloatProperty()
    crsLink = StringProperty()
    crsRating = FloatProperty()
    crsEnroll = IntegerProperty()
    crsName = StringProperty()
    crsTime = StringProperty()
    subtitle = RelationshipTo("SubTitle", "TEACH_IN")
    organization = RelationshipTo("Organization", "COLLABORATE_WITH")
    instructor = RelationshipFrom("Instructor", "INSTRUCT_BY")
    level = RelationshipTo("Level", "HAS_LEVEL")
    website = RelationshipTo("Website", "IS_IN")
    subject = RelationshipTo("Subject", "BELONG")
    knowledge = RelationshipTo("Knowledge", "TEACH_KNOWLEDGE", model=Teach)
    platform = RelationshipTo("Platform", "TEACH_PLATFORM", model=Teach)
    tool = RelationshipTo("Tool", "TEACH_TOOL", model=Teach)
    programinglanguage = RelationshipTo("ProgramingLanguage", "TEACH_PROGRAMINGLANGUAGE", model=Teach)
    framework = RelationshipTo("Framework", "TEACH_FRAMEWORK", model=Teach)
    knowledge_p = RelationshipTo("Knowledge", "REQUIRE_KNOWLEDGE", model=Require)
    platform_p = RelationshipTo("Platform", "REQUIRE_PLATFORM", model=Require)
    tool_p = RelationshipTo("Tool", "REQUIRE_TOOL", model=Require)
    programinglanguage_p = RelationshipTo("ProgramingLanguage", "REQUIRE_PROGRAMINGLANGUAGE", model=Require)
    framework_p = RelationshipTo("Framework", "REQUIRE_FRAMEWORK", model=Require)
    enroll = RelationshipFrom("User", "ENROLL")
    complete = RelationshipFrom("User", "COMPLETE")
    program = RelationshipFrom("Program", "INCLUDE_COURSE", model=Index)

    def to_json(self):
        fee = self.crsFee
        rating = self.crsRating
        if math.isnan(self.crsFee):
            fee = -1
        crsName = self.crsName.replace("\x92", "'")
        return {
            "id": self.id,
            "crsEnroll": self.crsEnroll,
            "crsName": crsName,
            "crsTime": self.crsTime,
            "crsFee": fee,
            "crsLink": self.crsLink,
            "crsRating": rating,
            "crsEnroll": self.crsEnroll,
            "subtitle": list(map(lambda n: n.to_json(), self.subtitle)),
            "organization": list(map(lambda n: n.to_json(), self.organization)),
            "instructor": list(map(lambda n: n.to_json(), self.instructor)),
            "level": list(map(lambda n: n.to_json(), self.level)),
            "subject": list(map(lambda n: n.to_json(), self.subject)),
            "knowledge": list(map(lambda n: n.to_json(), self.knowledge)),
            "platform": list(map(lambda n: n.to_json(), self.platform)),
            "programinglanguage": list(map(lambda n: n.to_json(), self.programinglanguage)),
            "tool": list(map(lambda n: n.to_json(), self.tool)),
            "framework": list(map(lambda n: n.to_json(), self.framework)),
            "require_knowledge": list(map(lambda n: n.to_json(), self.knowledge_p)),
            "require_platform": list(map(lambda n: n.to_json(), self.platform_p)),
            "require_tool": list(map(lambda n: n.to_json(), self.tool_p)),
            "require_programinglanguage": list(map(lambda n: n.to_json(), self.programinglanguage_p)),
            "require_framework": list(map(lambda n: n.to_json(), self.framework_p)),
        }

    def export(self):
        fee = self.crsFee
        rating = self.crsRating
        if math.isnan(self.crsFee):
            fee = 0
        crsName = self.crsName.replace("\x92", "'")
        return {
            "id": self.id,
            "crsEnroll": self.crsEnroll,
            "crsName": crsName,
            "crsTime": self.crsTime,
            "crsFee": fee,
            "crsLink": self.crsLink,
            "crsRating": rating,
            "crsEnroll": self.crsEnroll,
            "subtitle": list(map(lambda n: n.export(), self.subtitle)),
            "organization": list(map(lambda n: n.export(), self.organization)),
            "website": list(map(lambda n: n.export(), self.website)),
            "instructor": list(map(lambda n: n.export(), self.instructor)),
            "level": list(map(lambda n: n.export(), self.level)),
            "subject": list(map(lambda n: n.export(), self.subject)),
            "knowledge": list(map(lambda n: n.export(), self.knowledge)),
            "platform": list(map(lambda n: n.export(), self.platform)),
            "programinglanguage": list(map(lambda n: n.export(), self.programinglanguage)),
            "tool": list(map(lambda n: n.export(), self.tool)),
            "framework": list(map(lambda n: n.export(), self.framework)),
            "require_knowledge": list(map(lambda n: n.to_json(), self.knowledge_p)),
            "require_platform": list(map(lambda n: n.to_json(), self.platform_p)),
            "require_tool": list(map(lambda n: n.to_json(), self.tool_p)),
            "require_programinglanguage": list(map(lambda n: n.to_json(), self.programinglanguage_p)),
            "require_framework": list(map(lambda n: n.to_json(), self.framework_p)),
            "program": list(map(lambda n: n.export(), self.program)),
        }

    def get_one(id):
        try:
            model = Course(id=id)
            model.refresh()
            return model
        except:
            return None


class Career(StructuredNode):
    creCreate_Date = DateTimeProperty()
    creUpdate_Date = DateTimeProperty()
    creTitle = StringProperty()
    creMedianSalary = StringProperty()
    creDescription = StringProperty()
    knowledge = RelationshipTo("Knowledge", "NEED_KNOWLEDGE", model=Need)
    platform = RelationshipTo("Platform", "NEED_PLATFORM", model=Need)
    tool = RelationshipTo("Tool", "NEED_TOOL", model=Need)
    programinglanguage = RelationshipTo("ProgramingLanguage", "NEED_PROGRAMINGLANGUAGE", model=Need)
    framework = RelationshipTo("Framework", "NEED_FRAMEWORK", model=Need)
    current = RelationshipFrom("User", "HAS_CURRENT_CAREER")
    hope = RelationshipTo("User", "HAS_HOPE_CAREER")
    program = RelationshipTo("Program", "HAS_PROGRAM")
    industry = RelationshipTo("Industry", "IN_INDUSTRY")

    def to_json(self):
        return {
            "id": self.id,
            "creTitle": self.creTitle,
            "knowledge": map(lambda n: n.to_json(), self.knowledge),
            "platform": map(lambda n: n.to_json(), self.platform),
            "programinglanguage": map(lambda n: n.to_json(), self.programinglanguage),
            "tool": map(lambda n: n.to_json(), self.tool),
            "framework": map(lambda n: n.to_json(), self.framework),
            "industry": map(lambda n: n.to_json(), self.industry),
        }

    def to_json_1(self):
        return {
            "id": self.id,
            "creTitle": self.creTitle,
        }

    def export(self):
        return {
            "id": self.id,
            "creTitle": self.creTitle,
            "knowledge": map(lambda n: n.export(), self.knowledge),
            "platform": map(lambda n: n.export(), self.platform),
            "programinglanguage": map(lambda n: n.export(), self.programinglanguage),
            "tool": map(lambda n: n.export(), self.tool),
            "framework": map(lambda n: n.export(), self.framework),
            "industry": map(lambda n: n.export(), self.industry),
        }

    def get_one(id):
        try:
            model = Career(id=id)
            model.refresh()
            return model
        except:
            return None


class Taxonomy(StructuredNode):
    TaxonomyName = StringProperty()
    industry = RelationshipFrom("Industry", "IN_TAXONOMY")

    def to_json(self):
        return {
            "TaxonomyName": self.TaxonomyName,
            "industry": map(lambda n: n.to_json(), self.industry),
        }


class Industry(StructuredNode):
    IndustryName = StringProperty()
    taxonomy = RelationshipTo("Taxonomy", "IN_TAXONOMY")
    career = RelationshipFrom("Career", "IN_INDUSTRY")

    def to_json(self):
        return {
            "IndustryName": self.IndustryName,
            "taxonomy": map(lambda n: n.to_json(), self.toxonomy),
            "career": map(lambda n: n.to_json(), self.career),
        }

    def export(self):
        return self.IndustryName


class Program(StructuredNode):
    Create_Date = DateTimeProperty()
    Update_Date = DateTimeProperty()
    proName = StringProperty()
    course = RelationshipTo("Course", "INCLUDE_COURSE", model=Index)
    career = RelationshipFrom("Career", "HAS_PROGRAM")
    knowledge = RelationshipTo("Knowledge", "HAS_KNOWLEDGE")
    platform = RelationshipTo("Platform", "HAS_PLATFORM")
    tool = RelationshipTo("Tool", "HAS_TOOL")
    programinglanguage = RelationshipTo("ProgramingLanguage", "HAS_PROGRAMINGLANGUAGE")
    framework = RelationshipTo("Framework", "HAS_FRAMEWORK")

    def to_json(self):
        return {
            "id": self.id,
            "proName": self.proName,
            "course": list(map(lambda n: n.to_json(), self.course)),
            "knowledge": list(map(lambda n: n.to_json(), self.knowledge)),
            "platform": list(map(lambda n: n.to_json(), self.platform)),
            "tool": list(map(lambda n: n.to_json(), self.tool)),
            "programinglanguage": list(map(lambda n: n.to_json(), self.programinglanguage)),
            "framework": list(map(lambda n: n.to_json(), self.framework)),
        }

    def to_json_1(self):
        return {
            "id": self.id,
            "proName": self.proName,
            "course": list(map(lambda n: n.to_json(), self.course)),
            "knowledge": list(map(lambda n: n.to_json(), self.knowledge)),
            "platform": list(map(lambda n: n.to_json(), self.platform)),
            "tool": list(map(lambda n: n.to_json(), self.tool)),
            "programinglanguage": list(map(lambda n: n.to_json(), self.programinglanguage)),
            "framework": list(map(lambda n: n.to_json(), self.framework)),
        }

    def export(self):
        return self.proName

    def get_one(id):
        try:
            model = Program(id=id)
            model.refresh()
            return model
        except:
            return None


class Knowledge(StructuredNode):
    Create_Date = DateTimeProperty()
    Update_Date = DateTimeProperty()
    value = StringProperty()
    course = RelationshipFrom("Course", "TEACH_KNOWLEDGE")
    require_course = RelationshipFrom("Course", "NEED_KNOWLEDGE")
    career = RelationshipFrom("Career", "NEED_KNOWLEDGE")
    user = RelationshipFrom("User", "HAS_KNOWLEDGE")
    tool = RelationshipTo("Tool", "USE_TOOL")
    platform = RelationshipTo("Platform", "USE_PLATFORM")
    framework = RelationshipTo("Framework", "USE_FRAMEWORK")
    programinglanguage = RelationshipTo("ProgramingLanguage", "USE_PROGRAMINGLANGUAGE")

    def to_json(self):
        value = self.value.replace("\x92", "'")
        return {
            "id": self.id,
            "value": value
        }

    def export(self):
        value = self.value.replace("\x92", "'")
        return value


class Tool(StructuredNode):
    Create_Date = DateTimeProperty()
    Update_Date = DateTimeProperty()
    value = StringProperty()
    course = RelationshipFrom("Course", "TEACH_TOOL")
    require_course = RelationshipFrom("Course", "NEED_TOOL")
    career = RelationshipFrom("Career", "NEED_TOOL")
    user = RelationshipFrom("User", "HAS_TOOL")

    knowledge = RelationshipFrom("Knowledge", "USE_TOOL")
    programinglanguage = RelationshipTo("ProgramingLanguage", "INTERACT_LANG")

    def to_json(self):
        value = self.value.replace("\x92", "'")
        return {
            "id": self.id,
            "value": value
        }

    def export(self):
        value = self.value.replace("\x92", "'")
        return value


class Platform(StructuredNode):
    Create_Date = DateTimeProperty()
    Update_Date = DateTimeProperty()
    value = StringProperty()
    course = RelationshipFrom("Course", "TEACH_PLATFORM")
    require_course = RelationshipFrom("Course", "NEED_COURSE")
    career = RelationshipFrom("Career", "NEED_PLATFORM")
    user = RelationshipFrom("User", "HAS_PLATFORM")
    knowledge = RelationshipFrom("Knowledge", "USE_PLATFORM")
    framework = RelationshipFrom("Framework", "DEPLOY_PLAT")

    def to_json(self):
        value = self.value.replace("\x92", "'")
        return {
            "id": self.id,
            "value": value
        }

    def export(self):
        value = self.value.replace("\x92", "'")
        return value


class Framework(StructuredNode):
    Create_Date = DateTimeProperty()
    Update_Date = DateTimeProperty()
    value = StringProperty()
    course = RelationshipFrom("Course", "TEACH_FRAMEWORK")
    require_course = RelationshipFrom("Course", "NEED_COURSE")
    career = RelationshipFrom("Career", "NEED_FRAMEWORK")
    user = RelationshipFrom("User", "HAS_FRAMEWORK")
    knowledge = RelationshipFrom("Knowledge", "USE_FRAMEWORK")
    platform = RelationshipTo("Platform", "DEPLOY_PLAT")
    programinglanguage = RelationshipTo("ProgramingLanguage", "NEED_LANG")

    def to_json(self):
        value = self.value.replace("\x92", "'")
        return {
            "id": self.id,
            "value": value
        }

    def export(self):
        value = self.value.replace("\x92", "'")
        return value


class ProgramingLanguage(StructuredNode):
    Create_Date = DateTimeProperty()
    Update_Date = DateTimeProperty()
    value = StringProperty()
    course = RelationshipFrom("Course", "TEACH_PROGRAMINGLANGUAGE")
    user = RelationshipFrom("User", "HAS_PROGRAMINGLANGUAGE")
    require_course = RelationshipFrom("Course", "NEED_PROGRAMINGLANGUAGE")
    career = RelationshipFrom("Career", "NEED_PROGRAMINGLANGUAGE")
    knowledge = RelationshipFrom("Knowledge", "USE_LANG")
    tool = RelationshipFrom("Tool", "INTERACT_LANG")
    framework = RelationshipFrom("Framework", "NEED_LANG")

    def to_json(self):
        value = self.value.replace("\x92", "'")
        return {
            "id": self.id,
            "value": value,
        }

    def export(self):
        value = self.value.replace("\x92", "'")
        return value


def SortCoursebyEnroll(list_Course):
    def key_Enroll(course):
        b = course.__properties__
        return b['Enroll']

    list_Course.sort(reverse=True, key=key_Enroll)


def SearchCourseByName(text):
    return Course.nodes.filter(Q(crsName__icontains=text))


def filterCourse(Courses, field, value):
    if (field == 'Duration'):
        print('khi nao co duration thì tính sau')
    return Courses.filter(field=value)


def Program_Skill():
    program = Program.nodes.all()
    for p in program:
        courses = p.course
        for i in courses:
            if (i.tool != None):
                for j in i.tool:
                    p.tool.connect(j)
            if (i.knowledge != None):
                for j in i.knowledge:
                    p.knowledge.connect(j)
            if (i.platform != None):
                for j in i.platform:
                    p.platform.connect(j)
            if (i.framework != None):
                for j in i.framework:
                    p.framework.connect(j)
            if (i.programinglanguage != None):
                for j in i.programinglanguage:
                    p.programinglanguage.connect(j)


def Create_Graph():
    querycareer = """CALL gds.graph.create('careergraph',['Career', 'Framework','ProgramingLanguage','Tool','Program','Knowledge'],
    {
        HAS_FRAMEWORK:{type:'HAS_FRAMEWORK'}
      ,HAS_PROGRAMINGLANGUAGE:{type:'HAS_PROGRAMINGLANGUAGE'}
        ,HAS_TOOL:{type:'HAS_TOOL'}
        ,HAS_PLATFORM:{type:'HAS_PLATFORM'}
        ,HAS_KNOWLEDGE:{type:'HAS_KNOWLEDGE'}
        ,NEED_FRAMEWORK:{type:'NEED_FRAMEWORK'}
        ,NEED_PROGRAMINGLANGUAGE:{type:'NEED_PROGRAMINGLANGUAGE'}
        ,NEED_TOOL:{type:'NEED_TOOL'}
        ,NEED_PLATFORM:{type:'NEED_PLATFORM'}
        ,NEED_KNOWLEDGE:{type:'NEED_KNOWLEDGE'}
    }
);
"""
    querycourse = """CALL gds.graph.create('coursegraph',['Course', 'Framework','ProgramingLanguage','Tool','Platform','Knowledge'],
    {

        ,TEACH_FRAMEWORK:{type:'TEACH_FRAMEWORK'}
        ,TEACH_PROGRAMINGLANGUAGE:{type:'TEACH_PROGRAMINGLANGUAGE'}
        ,TEACH_TOOL:{type:'TEACH_TOOL'}
        ,TEACH_PLATFORM:{type:'TEACH_PLATFORM'}
        ,TEACH_KNOWLEDGE:{type:'TEACH_KNOWLEDGE'}
    }
);
"""
    Career.nodes.first_or_none().cypher(querycareer)
    Course.nodes.first_or_none().cypher(querycourse)


def Career_Program(career):
    similar = career.cypher(
        "CALL gds.nodeSimilarity.stream('careergraph') YIELD node1, node2, similarity  where gds.util.asNode(node1).creTitle='" + career.creTitle + "' and gds.util.asNode(node2).creTitle is  null  RETURN gds.util.asNode(node1).creTitle AS Career, gds.util.asNode(node2).proName AS Program, similarity")
    return similar[0]


def SimilarCourse(course):
    similar = course.cypher(
        "CALL gds.nodeSimilarity.stream('coursegraph') YIELD node1, node2, similarity  where gds.util.asNode(node1).crsLink='" + course.crsLink + "'  RETURN gds.util.asNode(node1).crsLink AS Course1, gds.util.asNode(node2).crsLink AS Course2, similarity")
    return similar[0]


def Program_Skill():
    program = Program.nodes.all()
    for p in program:
        courses = p.course
        for i in courses:
            if (i.tool != None):
                for j in i.tool:
                    p.tool.connect(j)
            if (i.knowledge != None):
                for j in i.knowledge:
                    p.knowledge.connect(j)
            if (i.platform != None):
                for j in i.platform:
                    p.platform.connect(j)
            if (i.framework != None):
                for j in i.framework:
                    p.framework.connect(j)
            if (i.programinglanguage != None):
                for j in i.programinglanguage:
                    p.programinglanguage.connect(j)


def ReCareerProgramWithFitler(career, list_skill):
    subcareer = Career(creTitle='subcareer').save()
    for i in career.tool:
        if (i.value not in list_skill):
            subcareer.tool.connect(i)
    for i in career.programinglanguage:
        if (i.value not in list_skill):
            subcareer.programinglanguage.connect(i)
    for i in career.knowledge:
        if (i.value not in list_skill):
            subcareer.knowledge.connect(i)
    for i in career.platform:
        if (i.value not in list_skill):
            subcareer.platform.connect(i)
    for i in career.framework:
        if (i.value not in list_skill):
            subcareer.framework.connect(i)
    subcareer.save()
    query = """CALL gds.graph.create('subgraph',['Career', 'Framework','ProgramingLanguage','Tool','Program','Knowledge'],
    {
        HAS_FRAMEWORK:{type:'HAS_FRAMEWORK'}
        ,HAS_PROGRAMINGLANGUAGE:{type:'HAS_PROGAMINGLANGUAGE'}
        ,HAS_TOOL:{type:'HAS_TOOL'}
        ,HAS_PLATFORM:{type:'HAS_PLATFORM'}
        ,HAS_KNOWLEDGE:{type:'HAS_KNOWLEDGE'}
        ,NEED_FRAMEWORK:{type:'NEED_FRAMEWORK'}
        ,NEED_PROGRAMINGLANGUAGE:{type:'NEED_PROGRAMINGLANGUAGE'}
        ,NEED_TOOL:{type:'NEED_TOOL'}
        ,NEED_PLATFORM:{type:'NEED_PLATFORM'}
        ,NEED_KNOWLEDGE:{type:'NEED_KNOWLEDGE'}
    }
);
"""
    subcareer.cypher(query)
    similar = subcareer.cypher(
        "CALL gds.nodeSimilarity.stream('subgraph') YIELD node1, node2, similarity  where gds.util.asNode(node1).creTitle='" + subcareer.creTitle + "' and gds.util.asNode(node2).creTitle is  null  RETURN gds.util.asNode(node1).creTitle AS Career, gds.util.asNode(node2).proName AS Program, similarity")
    subcareer.cypher("CALL gds.graph.drop('subgraph')")
    subcareer.delete()
    return similar[0]


def Career_Course(career):
    similar = career.cypher(
        "CALL gds.nodeSimilarity.stream('graph') YIELD node1, node2, similarity  where gds.util.asNode(node1).creTitle='" + career.creTitle + "' and gds.util.asNode(node2).creTitle is  null  RETURN gds.util.asNode(node1).creTitle AS Career, gds.util.asNode(node2).crsLink as Course, similarity")
    return similar[0]


def add_Indus_Taxo():
    co = Taxonomy(TaxonomyName="Computer Occupations").save()
    mso = Taxonomy(TaxonomyName="Mathematical Science Occupations").save()
    i1 = Industry(IndustryName="Database, Network Administrators and Architects").save()
    i2 = Industry(IndustryName="Software and Web Developers, Programmers, and Tester").save()
    i3 = Industry(IndustryName="Data Scientist").save()
    co.industry.connect(i1)
    co.industry.connect(i2)
    mso.industry.connect(i3)
    i1.career.connect(Career.nodes.first_or_none(creTitle="Database Administrator"))
    i1.career.connect(Career.nodes.first_or_none(creTitle='Network Engineer'))
    i1.career.connect(Career.nodes.first_or_none(creTitle='Software Architect'))
    i2.career.connect(Career.nodes.first_or_none(creTitle='Frontend Developer'))
    i2.career.connect(Career.nodes.first_or_none(creTitle='Backend Developer'))
    i2.career.connect(Career.nodes.first_or_none(creTitle='Mobile Developer'))
    i2.career.connect(Career.nodes.first_or_none(creTitle='Game Development'))
    i2.career.connect(Career.nodes.first_or_none(creTitle='Devops Engineer'))
    i2.career.connect(Career.nodes.first_or_none(creTitle='UX/UI Designer'))
    i2.career.connect(Career.nodes.first_or_none(creTitle='Tester'))
    i3.career.connect(Career.nodes.first_or_none(creTitle='Data Scientist'))
    i3.career.connect(Career.nodes.first_or_none(creTitle='Data Analysts'))
    i3.career.connect(Career.nodes.first_or_none(creTitle='Data Engineer'))
    i3.career.connect(Career.nodes.first_or_none(creTitle='Business Analyst'))

# Program_Skill()
# Create_Graph()
# add_Indus_Taxo()
