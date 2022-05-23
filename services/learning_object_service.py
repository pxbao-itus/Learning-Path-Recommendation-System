from neomodel import db

from models.models import ProgramingLanguage, Knowledge, Framework, Platform, Tool


def get_all_programing_language():
    all_language = ProgramingLanguage.nodes.all()
    list_language = []
    for language in all_language:
        list_language.append(language.to_json())
    return list_language


def get_all_knowledge():
    all_knowledge = Knowledge.nodes.all()
    list_knowledge = []
    for knowledge in all_knowledge:
        list_knowledge.append(knowledge.to_json())
    return list_knowledge


def get_all_tool():
    all_tools = Tool.nodes.all()
    list_tools = []
    for tool in all_tools:
        list_tools.append(tool.to_json())
    return list_tools


def get_all_platform():
    all_platforms = Platform.nodes.all()
    list_platforms = []
    for platform in all_platforms:
        list_platforms.append(platform.to_json())
    return list_platforms


def get_all_framework():
    all_frameworks = Framework.nodes.all()
    list_frameworks = []
    for framework in all_frameworks:
        list_frameworks.append(framework.to_json())
    return list_frameworks

def get_language_by_career(id):
    results, meta = db.cypher_query('Match (c:Career)-[r:NEED_PROGRAMINGLANGUAGE]->(p:ProgramingLanguage) where id(c) = {id} return p'.format(id=id))
    print(results)
    languages = [ProgramingLanguage.inflate(row[0]).to_json() for row in results]
    return languages


