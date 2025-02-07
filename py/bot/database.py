import sqlite3

def create_tables():
    try:
        conn = sqlite3.connect('laboratori.db')  # Sostituisci con il nome del tuo database
        cursor = conn.cursor()

        # Creazione della tabella 'laboratori'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS laboratori (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL
            )
        ''')

        # Creazione della tabella 'orari'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                orario TEXT UNIQUE NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

        print("Tabelle 'laboratori' e 'orari' create correttamente!")
    except Exception as e:
        print(f"Errore durante la creazione delle tabelle: {e}")
# Connessione al database
def connect_db():
    return sqlite3.connect("bot_database.db", check_same_thread=False)

# Funzione per creare le tabelle principali
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # Crea la tabella professori
    cursor.execute('''CREATE TABLE IF NOT EXISTS professori (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT UNIQUE NOT NULL)''')

    # Crea la tabella classi
    cursor.execute('''CREATE TABLE IF NOT EXISTS classi (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT UNIQUE NOT NULL)''')

    # Crea la tabella laboratori
    cursor.execute('''CREATE TABLE IF NOT EXISTS laboratori (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT UNIQUE NOT NULL)''')

    # Crea la tabella orari
    cursor.execute('''CREATE TABLE IF NOT EXISTS orari (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        orario TEXT NOT NULL)''')

    # Crea la tabella prenotazioni
    cursor.execute('''CREATE TABLE IF NOT EXISTS prenotazioni (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        classe_id INTEGER,
                        laboratorio_id INTEGER,
                        professore_id INTEGER,
                        orario_id INTEGER,
                        FOREIGN KEY (classe_id) REFERENCES classi(id),
                        FOREIGN KEY (laboratorio_id) REFERENCES laboratori(id),
                        FOREIGN KEY (professore_id) REFERENCES professori(id),
                        FOREIGN KEY (orario_id) REFERENCES orari(id))''')

    conn.commit()
    conn.close()

# Funzioni per aggiungere dati nelle tabelle
def add_classe(nome):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO classi (nome) VALUES (?)", (nome,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def add_insegnante(nome):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO professori (nome) VALUES (?)", (nome,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def add_laboratorio(nome):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO laboratori (nome) VALUES (?)", (nome,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def add_orario(orario):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO orari (orario) VALUES (?)", (orario,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Funzioni per ottenere i dati dalle tabelle
def get_classi():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM classi")
    result = cursor.fetchall()
    conn.close()
    return result

def get_insegnanti():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professori")
    result = cursor.fetchall()
    conn.close()
    return result

def get_laboratori():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM laboratori")
    result = cursor.fetchall()
    conn.close()
    return result

def get_orari():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orari")
    result = cursor.fetchall()
    conn.close()
    return result

def add_laboratorio(laboratorio):
    try:
        conn = sqlite3.connect('laboratori.db')  # Usa il tuo database
        cursor = conn.cursor()
        cursor.execute("INSERT INTO laboratori (nome) VALUES (?)", (laboratorio,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Errore durante l'aggiunta del laboratorio: {e}")
        return False
    
def add_orario(orario):
    try:
        conn = sqlite3.connect('laboratori.db')  # Usa il tuo database
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orari (orario) VALUES (?)", (orario,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Errore durante l'aggiunta dell'orario: {e}")
        return False

def get_orari_disponibili():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''SELECT laboratori.nome, classi.nome, professori.nome, orari.orario
                      FROM prenotazioni
                      INNER JOIN laboratori ON prenotazioni.laboratorio_id = laboratori.id
                      INNER JOIN classi ON prenotazioni.classe_id = classi.id
                      INNER JOIN professori ON prenotazioni.professore_id = professori.id
                      INNER JOIN orari ON prenotazioni.orario_id = orari.id
                      ORDER BY orari.orario''')

    orari = cursor.fetchall()
    conn.close()

    if not orari:
        return "Nessuna prenotazione trovata."

    risultato = "📅 **Orari delle Prenotazioni:**\n\n"
    for laboratorio, classe, professore, orario in orari:
        risultato += f"🏫 *{laboratorio}* - 📚 {classe} con 👨‍🏫 {professore}\n🕒 {orario}\n\n"

    return risultato
