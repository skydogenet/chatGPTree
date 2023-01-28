import irc.bot
import openai
import textwrap

class GPT3Bot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server, api_key):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, 6667)], nickname, nickname)
        self.channel = channel
        openai.api_key = api_key
        print("Init")

    def on_welcome(self, c, e):
        c.join(self.channel)
        print("Channel joined")

    def on_privmsg(self, c, e):
        sender = e.source.nick
        print("Private message")
        self.do_commandpriv(e, e.arguments[0], sender)

    def on_pubmsg(self, c, e):
        print("Public message")
        a = e.arguments[0].split(":", 1)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip())
        return

    def do_commandpriv(self, e, cmd, sender):
        print("do")
        c = self.connection

        prompt = (f"{cmd}")
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        message = completions.choices[0].text
        messager = message.replace('\n', ' ')
        for line in textwrap.wrap(message, width=450):
            c.privmsg(sender, line)
        print(messager)


    def do_command(self, e, cmd):
        print("do")
        c = self.connection

        prompt = (f"{cmd}")
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        message = completions.choices[0].text
        print(message)
        messager = message.replace('\n', ' ')
        for line in textwrap.wrap(message.strip(), width=450):
            c.privmsg(self.channel, line)
        print(messager)

bot = GPT3Bot("#channel", "Bot name", "IRC server address", "YOUR API KEY HERE")
print("Starting chatGPTree")
bot.start()

