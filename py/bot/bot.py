import telebot
from telebot import types
import database
database.create_tables()

TOKEN = '7668811545:AAFXAioiveIm-kaZvG9ybcZwWwzqXz9Z368'
bot = telebot.TeleBot(TOKEN)

# Funzione per il menu principale
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🗓️ Visualizza Orari Prenotazioni")
    btn2 = types.KeyboardButton("🔬 Prenota Laboratorio")
    btn3 = types.KeyboardButton("🔐 Admin")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, "Benvenuto nel bot! Scegli un'opzione:", reply_markup=markup)

# Funzione per gestire il comando /start
@bot.message_handler(commands=['start'])
def start(message):
    main_menu(message)

# Funzione per gestire la visualizzazione degli orari
@bot.message_handler(func=lambda message: message.text == "🗓️ Visualizza Orari Prenotazioni")
def visualizza_orari(message):
    orari_text = database.get_orari_disponibili()
    bot.send_message(message.chat.id, orari_text, parse_mode='Markdown')

# Funzione per la prenotazione del laboratorio
@bot.message_handler(func=lambda message: message.text == "🔬 Prenota Laboratorio")
def prenota_laboratorio(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    classi = database.get_classi()
    for classe in classi:
        btn = types.KeyboardButton(f"📚 {classe[1]}")
        markup.add(btn)
    bot.send_message(message.chat.id, "Seleziona una classe:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.startswith("📚"))
def scegli_laboratorio(message):
    classe_selezionata = message.text[2:]  # Rimuoviamo la parte emoji
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    laboratori = database.get_laboratori()
    for laboratorio in laboratori:
        btn = types.KeyboardButton(f"🖥️ {laboratorio[1]}")
        markup.add(btn)
    bot.send_message(message.chat.id, f"Seleziona un laboratorio per la classe {classe_selezionata}:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.startswith("🖥️"))
def scegli_professore(message):
    laboratorio_selezionato = message.text[2:]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    professori = database.get_insegnanti()
    for professore in professori:
        btn = types.KeyboardButton(f"👨‍🏫 {professore[1]}")
        markup.add(btn)
    bot.send_message(message.chat.id, f"Seleziona un professore per il laboratorio {laboratorio_selezionato}:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.startswith("👨‍🏫"))
def scegli_orario(message):
    professore_selezionato = message.text[3:]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    orari = database.get_orari()
    for orario in orari:
        btn = types.KeyboardButton(f"🕒 {orario[1]}")
        markup.add(btn)
    bot.send_message(message.chat.id, f"Seleziona un orario per il professore {professore_selezionato}:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.startswith("🕒"))
def conferma_prenotazione(message):
    orario_selezionato = message.text[2:]
    bot.send_message(message.chat.id, f"✅ Prenotazione confermata per l'orario {orario_selezionato}.", parse_mode='Markdown')

# Funzione per l'accesso admin
@bot.message_handler(func=lambda message: message.text == "🔐 Admin")
def admin_menu(message):
    if message.from_user.id ==  7184491435:  # ID admin
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("➕ Aggiungi Classe")
        btn2 = types.KeyboardButton("➕ Aggiungi Professore")
        btn3 = types.KeyboardButton("➕ Aggiungi Laboratorio")
        btn4 = types.KeyboardButton("➕ Aggiungi Orario")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, "Benvenuto Admin! Scegli un'opzione:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "🚫 Accesso negato. Non hai i permessi necessari.", parse_mode='Markdown')

# Funzioni per aggiungere dati come admin
@bot.message_handler(func=lambda message: message.text == "➕ Aggiungi Classe")
def aggiungi_classe(message):
    bot.send_message(message.chat.id, "✍️ Scrivi il nome della nuova classe:")
    bot.register_next_step_handler(message, process_add_classe)

def process_add_classe(message):
    classe = message.text
    if database.add_classe(classe):
        bot.send_message(message.chat.id, f"✅ La classe {classe} è stata aggiunta con successo.")
    else:
        bot.send_message(message.chat.id, "❌ Errore durante l'aggiunta della classe.")

# Aggiungere funzioni simili per aggiungere professori, laboratori e orari
# Esempio per aggiungere professore
@bot.message_handler(func=lambda message: message.text == "➕ Aggiungi Professore")
def aggiungi_professore(message):
    bot.send_message(message.chat.id, "✍️ Scrivi il nome del nuovo professore:")
    bot.register_next_step_handler(message, process_add_professore)

def process_add_professore(message):
    professore = message.text
    if database.add_insegnante(professore):
        bot.send_message(message.chat.id, f"✅ Il professore {professore} è stato aggiunto con successo.")
    else:
        bot.send_message(message.chat.id, "❌ Errore durante l'aggiunta del professore.")

# Aggiungere funzioni per "Aggiungi Laboratorio" e "Aggiungi Orario" simili
@bot.message_handler(func=lambda message: message.text == "➕ Aggiungi Laboratorio")
def aggiungi_laboratorio(message):
    bot.send_message(message.chat.id, "✍️ Scrivi il nome del nuovo laboratorio:")
    bot.register_next_step_handler(message, process_add_laboratorio)

def process_add_laboratorio(message):
    laboratorio = message.text
    if database.add_laboratorio(laboratorio):
        bot.send_message(message.chat.id, f"✅ Il laboratorio '{laboratorio}' è stato aggiunto con successo.")
    else:
        bot.send_message(message.chat.id, "❌ Errore durante l'aggiunta del laboratorio.")

@bot.message_handler(func=lambda message: message.text == "➕ Aggiungi Orario")
def aggiungi_orario(message):
    bot.send_message(message.chat.id, "✍️ Scrivi il nuovo orario (ad esempio '09:00 - 11:00'):")
    bot.register_next_step_handler(message, process_add_orario)

def process_add_orario(message):
    orario = message.text
    if database.add_orario(orario):
        bot.send_message(message.chat.id, f"✅ L'orario '{orario}' è stato aggiunto con successo.")
    else:
        bot.send_message(message.chat.id, "❌ Errore durante l'aggiunta dell'orario.")

#giuls
@bot.message_handler(commands=["giulia"])
def start(message):
    bot.send_message(message.chat.id, "la ragazza piu bella che c'è ❤️")

# Avvia il bot
bot.polling(none_stop=True)
