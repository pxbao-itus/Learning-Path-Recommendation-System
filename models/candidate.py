class Candidate:
    def __init__(self):
        self.size = 0
        self.content = []

    def __init__(self, content):
        self.content = content.copy()
        self.size = self.content.__len__()

    def get_value(self):
        return self.content

    def extend_value(self, value):
        self.content.extend(value)

    
def convert_list_object_to_list_course(objects):
    list_course = []
    for element in objects:
        list_course.extend(element.get_value())

    return list(set(list_course))
