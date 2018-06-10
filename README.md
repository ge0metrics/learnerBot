# learnerBot
make and use bots with personalities, using shared knowledge

currently, its more basic than any robot should be
one of five personalities will be generated for the bot, if an existing id isnt supplied
its personality will determine how it greets you, what it asks and its catchphrase that will occasionally pop up in conversation

# current methods
myBot=Bot() or myBot=Bot(id=4)
myBot.speak() or myBot.speak(length="long")
myBot.ask()
myBot.greet() which it will do automatically upon initialization

# future updates
- add emotions that will affect speech
- an actual conversational interface
- the ability to teach the bot new words, phrases, grammar
