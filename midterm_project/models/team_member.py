class TeamMember:
    def __init__(self, name, role, email):
        self.name = name
        self.role = role
        self.email = email

    def to_dict(self):
        return {
            "name": self.name,
            "role": self.role,
            "email": self.email
        }