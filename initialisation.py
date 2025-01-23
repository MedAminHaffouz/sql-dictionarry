import sqlite3

def initialise_database():
    conn = sqlite3.connect('dictionary.db')
    cursor = conn.cursor()

    # Create the Mot table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Mot (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mot TEXT NOT NULL,
            langue TEXT NOT NULL,
            type TEXT,
            premiere_lettre TEXT NOT NULL,
            genre TEXT,
            pluralité TEXT
        )
    ''')

    # Create the Sens table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texte TEXT NOT NULL,
            langue TEXT NOT NULL
        )
    ''')

    # Create the Posseder table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Posseder (
            mot_id INTEGER NOT NULL,
            sens_id INTEGER NOT NULL,
            FOREIGN KEY (mot_id) REFERENCES Mot (id),
            FOREIGN KEY (sens_id) REFERENCES Sens (id)
        )
    ''')

    # Create the Synonyme table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Synonyme (
            mot_id INTEGER NOT NULL,
            mot_syn_id INTEGER NOT NULL,
            FOREIGN KEY (mot_id) REFERENCES Mot (id),
            FOREIGN KEY (mot_syn_id) REFERENCES Mot (id)
        )
    ''')

    # Create the Antonyme table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Antonyme (
            mot_id INTEGER NOT NULL,
            mot_ant_id INTEGER NOT NULL,
            FOREIGN KEY (mot_id) REFERENCES Mot (id),
            FOREIGN KEY (mot_ant_id) REFERENCES Mot (id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialise_database()
    print("Database initialized successfully!")
