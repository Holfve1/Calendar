from lib.models.calendar import Calendar

class CalendarRepository():

    def __init__(self, connection):
        self.connection = connection

    def all(self):
        rows = self.connection.execute('SELECT * FROM calendar ORDER BY id')
        entries = []
        for row in rows:
            item = Calendar(row['id'], row['date'], row['start_time'], row['end_time'], row['content'], row['title'])
            entries.append(item)
        return entries

    def create(self, date, start_time, end_time, content, title):
        self.connection.execute('INSERT INTO calendar (date, start_time, end_time, content, title) VALUES (%s, %s, %s, %s, %s)', [date, start_time, end_time, content, title])
        return None

    def delete(self, id):
        self.connection.execute('DELETE FROM calendar WHERE ID = %s', [id])
        return None

    def update(self, id, date, start_time, end_time, content, title):
        self.connection.execute('UPDATE calendar SET date = %s, start_time = %s, end_time = %s, content = %s, title = %s WHERE id = %s', [date, start_time, end_time, content, title, id])
        return None