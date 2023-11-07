import mysql.connector
import random
import tkinter as tk
from tkinter import messagebox, simpledialog

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="vocabulary"
)

def randomw(numwords):
    # Retrieve random words from the database
    cursor = connection.cursor()
    cursor.execute("SELECT word, translation FROM words ORDER BY RAND() LIMIT %s", (numwords,))
    words = cursor.fetchall()
    cursor.close()
    return words

def quser(words): # Quser = Quiz User
    missed_words = []  # Define missed_words list
    for word, translation in words:
        userinput = enterword(f"What is the translation of '{word}' in lowercase?")
        if userinput.lower() != translation.lower():
            messagebox.showinfo("Incorrect", f"Incorrect. The correct translation is '{translation}'.")
            missed_words.append((word, translation))  # Append missed word to missed_words list
        else:
            messagebox.showinfo("Correct", "Correct!")
    return missed_words

def create_missed_words_database(missed_words):
    # Create a new database to store missed words
    missed_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="MissedWords"
    )
    cursor = missed_connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS words (word VARCHAR(255), translation VARCHAR(255))")
    cursor.executemany("INSERT INTO words (word, translation) VALUES (%s, %s)", missed_words)
    missed_connection.commit()
    cursor.close()
    missed_connection.close()

def enterword(prompt):
    result = simpledialog.askstring("User Input", prompt)
    return result if result else ""

# Tkinter Initialization
window = tk.Tk()
window.title("Vocabulary Quiz")
window.geometry("800x600")

def stquiz():
    num_words = simpledialog.askinteger("Number of Words", "How many words would you like to be checked on?")
    if num_words is not None:
        words = randomw(num_words)
        missed_words = quser(words)
        if missed_words:
            create_missed_words_database(missed_words)

stbutton = tk.Button(window, text="Start Quiz", command=stquiz)
stbutton.pack()

window.mainloop()
