import

conn = sqlite3.connect(DB_path)
cursor = conn.cursor()

cursor.execute('''
    SELECT mot,langue,type
    FROM Mot
    ORDER BY mot
''')
res = cursor.fetchall()

return res