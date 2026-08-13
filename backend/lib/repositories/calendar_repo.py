from lib.models.calendar import Calendar

class CalendarRepository():

    def __init__(self, connection):
        self.connection = connection

    def all(self):
        rows = self.connection.execute('SELECT * FROM calendar ORDER BY id')
        entries = []
        for row in rows:
            item = Calendar(row['id'], row['date'], row['start_time'], row['end_time'], row['content'], row['title'], row['is_recurring'], row['recurrence_group_id'])
            entries.append(item)
        return entries

    def create(self, date, start_time, end_time, content, title, is_recurring=False, recurrence_group_id=None):
        self.connection.execute('INSERT INTO calendar (date, start_time, end_time, content, title, is_recurring, recurrence_group_id) VALUES (%s, %s, %s, %s, %s, %s, %s)', [date, start_time, end_time, content, title, is_recurring, recurrence_group_id])
        return None

    def delete(self, id):
        self.connection.execute('DELETE FROM calendar WHERE ID = %s', [id])
        return None

    def delete_series(self, recurrence_group_id):
        self.connection.execute('DELETE FROM calendar WHERE recurrence_group_id = %s', [recurrence_group_id])
        return None

    def update(self, id, date, start_time, end_time, content, title, is_recurring=False):
        self.connection.execute('UPDATE calendar SET date = %s, start_time = %s, end_time = %s, content = %s, title = %s, is_recurring = %s WHERE id = %s', [date, start_time, end_time, content, title, is_recurring, id])
        return None

    def update_series(self, recurrence_group_id, start_time, end_time, content, title):
        self.connection.execute('UPDATE calendar SET start_time = %s, end_time = %s, content = %s, title = %s WHERE recurrence_group_id = %s', [start_time, end_time, content, title, recurrence_group_id])
        return None
