import sqlite3
import discord
import datetime

class Setup:
    def __init__(self):
        conn = sqlite3.connect('SAM.DB')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS CONFIG (DEBUG INTEGER, TOKEN TEXT, ADMIN INTEGER)')
        cursor.execute('CREATE TABLE IF NOT EXISTS COMMANDS (NAME TEXT, ENABLED INTEGER)')
        cursor.execute('SELECT DEBUG FROM CONFIG')
        if cursor.fetchone() == None:
            print('CREATING DEFAULT CONFIG')
            cursor.execute('INSERT INTO CONFIG (DEBUG, TOKEN, ADMIN) VALUES (?, ?, ?)', (1, 'DEFAULT', 276276276))
        cursor.execute('SELECT ENABLED FROM COMMANDS WHERE NAME=?', ('PING',))
        if cursor.fetchone() == None:
            print('INSERTING COMMANDS')
            cursor.execute('INSERT INTO COMMANDS (NAME, ENABLED) VALUES (?, ?)', ('PING', 1))
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
    def input(self, user):
        log = user.name + ' | ' + str(user.discord) + ' | ' + str(user.timestamp) + ' | ' + user.command + '\n'
        if user.discord == config.admin:
            if 'ADMINDEBUG1' in user.command:
                log += str(Command.get())

        if 'PING' in user.command:
            print(datetime.datetime.now().microsecond, '-', user.timestamp.microsecond)
            log += 'PONG: ' + str(datetime.datetime.now().microsecond - user.timestamp.microsecond)
        return log

    def get(self):
        conn = sqlite3.connect('SAM.DB')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM COMMANDS')
        data = cursor.fetchall()
        return data
        #self.ping = True


class DebugMain:
    def __init__(self):
        while True:
            self.command = input('AWAITING COMMAND\n\n>>').upper()
            self.discord = 276276276
            self.name = 'LEROY'
            self.timestamp = datetime.datetime.now()
            output = Command.input(self)
            print(output)

class Main(discord.Client):
    async def on_message(self, message):
        if message.author != self.user:
            self.command = message.content.upper()
            self.discord = message.author.id
            self.name = message.author.name.upper()
            self.timestamp = datetime.datetime.now()
            output = Command.input(self)
            await message.channel.send(output)


Setup = Setup()

Command = Command()

config = Setup.get()
if config.debug == 1:
    #
    DebugMain = DebugMain()
else:
    Main = Main()
    Main.run(config.token)
