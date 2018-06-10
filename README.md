# learnerBot
- make and use bots with personalities, using shared knowledge

# current info
- currently, its more basic than any robot should be
- one of five personalities will be generated for the bot, if an existing id isnt supplied
- its personality will determine how it greets you, what it asks and its quirk and catchphrase that will occasionally pop up in conversation
- brain.py is where the bot class is
- learnerBot.py is an example of the code
- knowledge.db is a database where the bots' personalities and shared knowledge is stored

# current methods
- myBot=Bot() or myBot=Bot(id=4) | initialize the bot
- myBot.speak() or myBot.speak(length="medium") | get the bot to say something. length can either be short or medium (or blank for random)
- myBot.ask() | get the bot to ask something / currently not varied or intelligent at all
- myBot.greet() | get the bot to greet you, which it will do automatically upon initialization / also currently not varied 

# future updates
- add emotions that will affect speech
- an actual conversational interface
- the ability to teach the bot new words, phrases, grammar
- changing names, quirks and catchphrases bc currently all are the same for new bots, except example bot 1
