import sqlite3
import discord
import datetime
import os
import sys
import requests
import random
import string

class Setup:
    def __init__(self):
        conn = sqlite3.connect('SAM.DB')
        cursor = conn.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS CONFIG (DEBUG INTEGER, TOKEN TEXT, ADMIN INTEGER)')
        cursor.execute('CREATE TABLE IF NOT EXISTS COMMANDS (NAME TEXT, ENABLED INTEGER)')

        cursor.execute('SELECT * FROM CONFIG')
        if cursor.fetchone() == None:
            print('CREATING DEFAULT CONFIG')
            cursor.execute('INSERT INTO CONFIG (DEBUG, TOKEN, ADMIN) VALUES (?, ?, ?)', (1, 'DEFAULT', 276276276))

        cursor.execute('SELECT * FROM COMMANDS')
        if cursor.fetchone() == None:
            print('CREATING DEFAULT COMMANDS')
            cursor.execute('INSERT INTO COMMANDS (NAME, ENABLED) VALUES (?, ?)', ('MATH', 1))
            cursor.execute('INSERT INTO COMMANDS (NAME, ENABLED) VALUES (?, ?)', ('RANDOM', 1))

        conn.commit()
        cursor.close()

    def get(self):
        conn = sqlite3.connect('SAM.DB')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM CONFIG')
        data = cursor.fetchall()
        if data == None:
            return None
        else:
            self.debug = data[0][0]
            self.token = data[0][1]
            self.admin = data[0][2]

        cursor.execute('SELECT * FROM COMMANDS')
        data = cursor.fetchall()
        if data == None:
            return None
        else:
            self.math = data[0][1]
            self.random = data[1][1]
        return self

    def update(self, config):
        conn = sqlite3.connect('SAM.DB')
        cursor = conn.cursor()
        cursor.execute('UPDATE CONFIG SET DEBUG=?,TOKEN=?,ADMIN=?', (config.debug, config.token, config.admin))
        cursor.execute('UPDATE COMMANDS SET ENABLED=? WHERE NAME=?', (config.math, 'MATH'))
        conn.commit()
        conn.close()

class Command:
    def input(self, user):
        config = Setup.get()
        #print('PRINT:', user.name, '|', str(user.discord), '|', str(user.timestamp), '|', user.command)
        if user.discord == config.admin:
            if 'ADMINDEBUG1' in user.command:
                log = 'ADMINCOMMANDS WORKING'
                return log
            if 'SHUTDOWN' in user.command:
                print('SAM IS SHUTINGDOWN!')
                sys.exit()
            if 'CONFIG' in user.command:
                if 'DEBUG' in user.command and len(user.command) == 3:
                    if int(user.command[2]) == 1 or int(user.command[2]) == 0:
                        config.debug = int(user.command[2])
                        Setup.update(config)
                        log = 'CONFIG UPDATED DEBUG MODE TO ' + user.command[2]
                        return log
                if 'TOKEN' in user.command and len(user.command) == 3:
                    if len(user.command[2]) > 50 and len(user.command[2]) < 70:
                        config.token = user.raw.split()[2]
                        Setup.update(config)
                        log = 'CONFIG UPDATED TOKEN TO ' + user.raw.split()[2]
                        return log
                if 'ADMIN' in user.command and len(user.command) == 3:
                    if len(user.command[2]) > 17 or int(user.command[2]) == 276276276:
                        config.admin = int(user.command[2])
                        Setup.update(config)
                        log = 'CONFIG UPDATED ADMIN TO ' + user.command[2]
                        return log

        if 'MATH' in user.command and config.math and len(user.command) == 4:
            if user.command[2].isdigit() and user.command[3].isdigit():
                if 'ADD' in user.command:
                    log = user.command[2] + ' + ' + user.command[3] + ' = ' + str(float(user.command[2]) + float(user.command[3]))
                    return log
                if 'SUB' in user.command:
                    log = user.command[2] + ' - ' + user.command[3] + ' = ' + str(float(user.command[2]) - float(user.command[3]))
                    return log
                if 'MUL' in user.command:
                    log = user.command[2] + ' * ' + user.command[3] + ' = ' + str(float(user.command[2]) * float(user.command[3]))
                    return log
                if 'DIV' in user.command:
                    if int(user.command[3]) != 0:
                        log = user.command[2] + ' / ' + user.command[3] + ' = ' + str(float(user.command[2]) / float(user.command[3]))
                        return log
                    else:
                        log = 'CANNOT DIVIDE BY 0!'
                        return log
                if 'MOD' in user.command:
                    log = user.command[2] + ' % ' + user.command[3] + ' = ' + str(float(user.command[2]) % float(user.command[3]))
                    return log
            else:
                log = 'MATH FUNCTION ONLY WORKS WITH NUMBERS.'
                return log

        if 'RAND' in user.command and config.random and len(user.command) > 1:
            if 'IMGUR' in user.command:
                characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                              's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                              'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1',
                              '2', '3', '4', '5', '6', '7', '8', '9']
                address = requests.get('https://i.imgur.com/removed.png')
                while address.url == 'https://i.imgur.com/removed.png' or '.jpg' not in address.url:
                    imgur = 'https://i.imgur.com/' + ''.join(random.choices(characters, weights=None, k=random.randint(5, 7))) + '.jpg'
                    address = requests.get(imgur)
                log = ['']
                log.append(address.url)
                log.append('')
                log.append('')
                return log
            if 'YOU' in user.command:
                characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                              's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                              'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1',
                              '2', '3', '4', '5', '6', '7', '8', '9']
                address = requests.get('https://i.imgur.com/removed.png')
                while address.url == 'https://i.imgur.com/removed.png' or '.jpg' not in address.url:
                    imgur = 'https://i.imgur.com/' + ''.join(
                        random.choices(characters, weights=None, k=random.randint(5, 7))) + '.jpg'
                    address = requests.get(imgur)
                log = ['']
                log.append(address.url)
                log.append('')
                log.append('')
                return log
            if 'PASS' in user.command and len(user.command) > 3:
                if 'NUM' in user.command:
                    characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                    password = ''.join(random.choices(characters, weights=None, k=int(user.command[3])))
                    if config.debug == 0:
                        log = 'PLEASE CHECK YOUR PRIVATE MESSAGES.'
                        return log
                    return password
                if 'LOW' in user.command:
                    characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                                  'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
                    password = ''.join(random.choices(characters, weights=None, k=int(user.command[3])))
                    if config.debug == 0:
                        log = 'PLEASE CHECK YOUR PRIVATE MESSAGES.'
                        return log
                    return password
                if 'UPP' in user.command:
                    characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                                  'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
                    password = ''.join(random.choices(characters, weights=None, k=int(user.command[3])))
                    if config.debug == 0:
                        log = 'PLEASE CHECK YOUR PRIVATE MESSAGES.'
                        return log
                    return password
                if 'LET' in user.command:
                    characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                                  'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                                  'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                                  'Z']
                    password = ''.join(random.choices(characters, weights=None, k=int(user.command[3])))
                    if config.debug == 0:
                        log = 'PLEASE CHECK YOUR PRIVATE MESSAGES.'
                        return log
                    return password
                if 'NOSYM' in user.command:
                    characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                                  'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                                  'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                                  'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                    password = ''.join(random.choices(characters, weights=None, k=int(user.command[3])))
                    if config.debug == 0:
                        log = 'PLEASE CHECK YOUR PRIVATE MESSAGES.'
                        return log
                    return password
                if 'ALL' in user.command:
                    characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                                  'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                                  'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                                  'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
                    randompassword = random.choices(characters, weights=None, k=int(user.command[3]))
                    symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', ']', '.', ',', '?', '<', '>', '/', ';', ':', '"', '`', '~']
                    for i in range(1, int(int(user.command[3])/3)):
                        x = random.randint(0, len(randompassword) - 1)
                        while randompassword[x] in symbols:
                            x = random.randint(0, len(randompassword) - 1)
                        randompassword[x] = random.choice(symbols)
                    password = ''.join(randompassword)
                    if config.debug == 0:
                        log = 'PLEASE CHECK YOUR PRIVATE MESSAGES.'
                        return log
                    return password
        log = "'" + ' '.join(user.command) + "' IS UNKNOWN, USE 'HELP' FOR A LIST OF COMMANDS."
        return log

class DebugMain:
    def __init__(self):
        while True:
            self.raw = input('\n>>')
            self.command = self.raw.upper().split()
            self.discord = 276276276
            self.name = 'LEROY'
            self.timestamp = datetime.datetime.now()
            output = Command.input(self)
            print(output)

class Main(discord.Client):
    async def on_message(self, message):
        if message.author != self.user:
            self.raw = message.content
            self.command = self.raw.upper().split()
            self.discord = message.author.id
            self.name = message.author.name.upper()
            self.timestamp = datetime.datetime.now()
            output = Command.input(self)
            if len(output[1]) > 1 or output[1] == None:
                embed = discord.Embed()
                if output[0] != None:
                    embed.set_thumbnail(url=output[0])
                if output[1] != None:
                    embed.set_image(url=output[1])
                if output[2] != None:
                    embed.set_author(name=output[2])
                if output[3] != None:
                    embed.set_footer(text=output[3])
                if len(output) > 4:
                    for i in output(0, len(output) - 4):
                        namevalue = output[i].split(', ')
                        embed.add_field(name=namevalue[0], value=namevalue[1], inline=True)
                await message.channel.send(embed=embed)
            else:
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
