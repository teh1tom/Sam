import sqlite3
# import discord

class Setup:
    def __init__(self):
        conn = sqlite3.connect('SAM.DB')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS CONFIG (DEBUG INTEGER, TOKEN TEXT, ADMIN INTEGER)')
        cursor.execute('SELECT DEBUG FROM CONFIG')
        if cursor.fetchone() == None:
            print('')
            cursor.execute('INSERT INTO CONFIG (DEBUG, TOKEN, ADMIN) VALUES (?, ?, ?)', (1, 'DEFAULT', 276276276))
        conn.commit()
        cursor.close()
    def get(self):
        conn = sqlite3.connect('SAM.DB')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM CONFIG')
        if cursor == None:
            return None
        else:
            data = cursor.fetchone()
            self.debug = data[0]
            self.token = data[1]
            self.admin = data[2]
            return self

class Command:
    def input(self, discord, name, command):
        log = command + "\n"
        return log

class DebugMain:
    def __init__(self):
        while True:
            command = input('AWAITING COMMAND\n\n>>')
            output = Command.input(276276276, 'LEROY', command.upper())
            print(output)

# class Main(discord.Client):
#     async def on_message(self, message):
#         return


Setup = Setup()

Command = Command()

config = Setup.get()
if config.debug == 1:
    #
    DebugMain = DebugMain()
# else:
    # Main = Main()
    # Main.run(config.token)
