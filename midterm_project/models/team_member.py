class TeamMember:
    def __init__(self, name, role, email):
        self.name = name.strip()
        self.role = role.strip()
        self.email = email.strip()
        