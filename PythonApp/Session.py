class Session:
    """ 
    Session object to store user session data.
    """
    def __init__(self, user_id, username, role):
        self.user_id = user_id
        self.username = username
        self.role = role


    def __str__(self):
        return f"Session(user_id={self.user_id}, username={self.username}, role={self.role})"
