import sqlite3

class FeedbackSystem:
    def __init__(self, db_name="feedback.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        # Cria a tabela de feedback se não existir
        query = '''CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_input TEXT,
                    response TEXT,
                    feedback INTEGER)'''
        self.conn.execute(query)
        self.conn.commit()

    def store_feedback(self, user_input, response, feedback):
        query = '''INSERT INTO feedback (user_input, response, feedback) VALUES (?, ?, ?)'''
        self.conn.execute(query, (user_input, response, feedback))
        self.conn.commit()

    def get_feedback(self, user_input):
        query = '''SELECT AVG(feedback) FROM feedback WHERE user_input = ?'''
        cursor = self.conn.execute(query, (user_input,))
        result = cursor.fetchone()[0]
        return result if result is not None else 0  # Retorna o feedback médio