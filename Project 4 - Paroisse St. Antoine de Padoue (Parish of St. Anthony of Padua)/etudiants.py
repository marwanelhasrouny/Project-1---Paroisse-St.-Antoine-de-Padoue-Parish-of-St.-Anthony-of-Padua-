import sqlite3

class Database:
    def __init__(self, db):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS etudiants(
            id INTEGER PRIMARY KEY,
            recu TEXT,
            prénom TEXT,
            nom TEXT,
            classe TEXT,
            année TEXT,
            cel_père TEXT,
            cel_mère TEXT,
            email TEXT
        )
        """
        self.cur.execute(sql)
        self.con.commit()

    def insert(self, recu, prénom, nom, classe, année, cel_père, cel_mère, email):
        self.cur.execute("INSERT INTO etudiants VALUES (NULL,?,?,?,?,?,?,?,?)",
                         (recu, prénom, nom, classe, année, cel_père, cel_mère, email))
        self.con.commit()

    def update(self, id, recu, prénom, nom, classe, année, cel_père, cel_mère, email):
        self.cur.execute("UPDATE etudiants SET recu=?, prénom=?, nom=?, classe=?, année=?, cel_père=?, cel_mère=?, email=? WHERE id=?",
                         (recu, prénom, nom, classe, année, cel_père, cel_mère, email, id))
        self.con.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM etudiants")
        rows = self.cur.fetchall()
        self.con.commit()
        return rows

    def remove(self, id):
        self.cur.execute("DELETE FROM etudiants WHERE id=?", (id,))
        self.con.commit()
