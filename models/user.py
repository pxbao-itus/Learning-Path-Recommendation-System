class User:

    def __init__(self, user):
        self.email = user.get('email')
        self.name = user.get('name')
        self.id = user.get('id')
        self.cost = user.get('cost')
        self.time = user.get('time')
        self.career = user.get('career')

    def is_time(self):
        if self.time > 0:
            return True
        else:
            return False

    def is_cost(self):
        if self.cost > 0:
            return True
        else:
            return False

    def get_user(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "cost": self.cost,
            "time": self.time,
            "career": self.career
        }
