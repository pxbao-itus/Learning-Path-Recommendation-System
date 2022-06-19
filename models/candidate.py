class Candidate:
    def __init__(self):
        self.size = 0
        self.content = []

    def __init__(self, content, lo):
        self.content = content.copy()
        self.size = self.content.__len__()
        self.lo_reference = lo

    def get_value(self):
        return self.content

    def extend_value(self, value):
        self.content.extend(value)
        self.content = list(set(self.content))

    def get_lo_reference(self):
        return self.lo_reference


def convert_list_object_to_list_course(objects):
    list_course = []
    for element in objects:
        list_course.extend(element.get_value())

    return list(set(list_course))
