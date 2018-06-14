# learnerBot
- make and use bots with personalities, using shared knowledge

# info
- currently, its very basic
- one of five personalities will be generated for the bot, if an existing id isn't supplied
- the chatbot folder is where the bot class file (chatbot.py) and database (knowledge.db) is stored
- chatbot can be imported to python files as normal (`from chatbot.chatbot import Bot`)
- chatbot_gui.py is an example of how the bot could be used in chat format with a GUI
- see https://github.com/ge0metrics/learnerBot/projects/2 for updates and progress tracking
- feel free to contribute, my coding style isn't perfect and this is my first complex project, so support is welcome :)

# current methods
- `myBot=Bot()` initialize the bot
  - `id=4` initialize a bot with an id
  - `debug=True` initializes bot in debug mode
- `myBot.speak()` returns the bot to saying something
  - `length="short"` or `length="medium"` random length sentence if not supplied
- `myBot.ask()` returns the bot asking something
- `myBot.greet()` returns the bot's greeting
  - `mode="respond"` returns answer to "what's up" style questions
- `myBot.reply(message)` analyses user messages to try and give a related reply
- `myBot.laugh()` returns the bot's laugh according to its personality
