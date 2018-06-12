# learnerBot
- make and use bots with personalities, using shared knowledge

# current info
- currently, its very basic
- one of four personalities will be generated for the bot, if an existing id isnt supplied
- its personality will determine how it greets you, what it asks
- it will have a quirk which will sometimes appear at the end of its sentences, and catchphrase that it will sometimes say instead of replying or random speech
- brain.py is where all the bot class code is
- learnerBot.py is an example of how the bot could be used in chat format
- knowledge.db is a database where the bots' personalities and shared knowledge is stored

# latest updates
- example now contains a GUI for "chatting" to a bot
- basic message analysis of user sent messages so the bot can reply in a sensical manner
- currently only understands hello greetings and greeting questions (whats up, how're you)
- it is currently in a debug state where it will repeat what you said in a raw analysis format instead of generating a sentence
- modified some word types, fish don't walk anymore
- reference personalities by id in the bot_info table
- added likes, dislikes and mood to bot_info
- added reply table for analysing user speech
- removed auto greet from bot
- added auto greet to example

# current methods
- myBot=Bot() or myBot=Bot(id=4) | initialize the bot
- myBot.speak() | get the bot to say something
  - length="short" or length="medium" or blank for random
- myBot.ask() | get the bot to ask something
- myBot.greet() | get the bot to greet you
  - mode="respond" for answer to "what's up" style questions
- myBot.reply() | analyses user messages to try and give a related reply

# future updates
- replies need to be coded more dynamically instead of checking every possible type of word separately
- emotions affecting speech
- the ability to teach the bot new words, phrases, grammar
- changing names, quirks and catchphrases bc currently all are the same for new bots, except example bot 1
