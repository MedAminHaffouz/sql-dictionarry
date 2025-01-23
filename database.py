import sqlite3

DB_path = "dictionary.db"

def add_word(mot,lang,t,genre=None,pl=None):
    first_let=mot[0].upper()
    conn=sqlite3.connect(DB_path)
    cursor=conn.cursor()

    cursor.execute('''
                   INSERT INTO Mot(mot,langue,type,premiere_lettre,genre,pluralité)
                   VALUES (?, ?, ?, ?, ?, ?)
                   ''',(mot,lang,t,first_let,genre,pl))
    conn.commit()

def add_meaning(lang,txt):
    conn=sqlite3.connect(DB_path)
    cursor=conn.cursor()

    cursor.execute('''
        INSERT INTO Meaning(langue,txt) VALUES (?, ?)''',(lang,txt))
    conn.commit()

def getword(mot,lang,t):
    conn=sqlite3.connect(DB_path)
    cursor=conn.cursor()

    cursor.execute('''
        SELECT id
        FROM Mot
        WHERE mot=? AND langue=? AND type=?
    ''',(mot,lang,t))
    resid=cursor.fetchone()
    if resid:
        return resid[0]
    else:
        return None

def getmeaning(lang,txt):
    conn=sqlite3.connect(DB_path)
    cursor=conn.cursor()

    cursor.execute('''
        SELECT id
        FROM Sens
        WHERE texte=? AND langue=?
    ''',(txt,lang))
    resid=cursor.fetchone()
    if resid:
        return resid[0]
    else:
        return None

def link_wm(langw,word,t,langm,txt):
    conn=sqlite3.connect(DB_path)
    cursor=conn.cursor()

    wordid=getword(word,langw,t)
    meaningid=getmeaning(langm,txt)
    if wordid and meaningid:
        cursor.execute('''
            INSERT INTO Posseder(mot_id,sens_id)
            VALUES (?, ?)
        ''',(wordid,meaningid))
        conn.commit()

def link_s(l1,l2,t,w1,w2):
    conn=sqlite3.connect(DB_path)
    cursor=conn.cursor()

    w1id=getword(w1,l1,t)
    w2id=getword(w2,l2,t)

    if w1id and w2id:
        cursor.execute('''
        INSERT INTO Synonyme(mot_id,mot_syn_id)
        VALUES (?, ?)
        ''',(w1id,w2id))
        conn.commit()


def link_a(l1,l2, t, w1, w2):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()

    w1id = getword(w1, l1, t)
    w2id = getword(w2, l2, t)

    if w1id and w2id:
        cursor.execute('''
        INSERT INTO Antonyme(mot_id,mot_ant_id)
        VALUES (?, ?)
        ''', (w1id, w2id))
        conn.commit()

def searchword(w):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT 
        m.mot,
        m.langue,
        m.type,
        COALESCE(m.genre, NULL) AS genre,
        COALESCE(m.pluralité, NULL) AS pluralité,
        GROUP_CONCAT(DISTINCT s.texte) AS meanings,
        GROUP_CONCAT(DISTINCT syn.mot) AS synonyms,
        GROUP_CONCAT(DISTINCT ant.mot) AS antonyms
    FROM 
        Mot m
    LEFT JOIN 
        Posseder p ON m.id = p.mot_id
    LEFT JOIN 
        Sens s ON p.sens_id = s.id
    LEFT JOIN 
        Synonyme syn ON m.id = syn.mot_id
    LEFT JOIN 
        Synonyme syn2 ON m.id = syn2.mot_syn_id  -- Pour récupérer les synonymes dans les deux sens
    LEFT JOIN 
        Antonyme ant ON m.id = ant.mot_id
    LEFT JOIN 
        Antonyme ant2 ON m.id = ant2.mot_ant_id  -- Pour récupérer les antonymes dans les deux sens
    WHERE 
        m.mot = ?  -- Ce paramètre vous permet de chercher pour tous les enregistrements du mot "chat"
    GROUP BY 
        m.id, m.langue, m.type 
    ''', (w,))  # Pass the parameter as a tuple

    results = cursor.fetchall()
    conn.close()

    return results

def showall(letter):
    conn = sqlite3.connect(DB_path)
    cursor = conn.cursor()

    cursor.execute('''
    SELECT 
        m.mot,
        m.langue,
        m.type,
        COALESCE(m.genre, NULL) AS genre,
        COALESCE(m.pluralité, NULL) AS pluralité
    FROM Mot m
    WHERE m.premiere_lettre = ?
    ''',(letter,))
    results = cursor.fetchall()
    conn.close()

    return results

