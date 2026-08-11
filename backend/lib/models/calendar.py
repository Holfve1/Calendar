class Calendar():

    def __init__(self, id, date, start_time, end_time, content, title):
        self.id = id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.content = content
        self.title = title

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Calendar({self.id}, {self.date}, {self.start_time}, {self.end_time}, {self.content}, {self.title})"