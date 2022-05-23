from models.models import Career

all_career = Career.nodes.all()


def get_all_career():
    list_career = []
    for i in all_career:
        list_career.append(i.to_json_1())
    return list_career


def get_career_by_id(career_id):
    return Career.get_one(career_id).to_json_1()


