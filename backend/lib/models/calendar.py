class Calendar():

    def __inti__(self, id, date, start_time, end_time, content):
        self.id = id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.content = content

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"Calendar{self.id = id}, {self.date = date}, {self.start_time = start_time}, {self.end_time = end_time}, {self.content = content}"