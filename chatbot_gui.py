from chatbot.chatbot import Bot
from tkinter import *
from tkinter import scrolledtext as tkst

def send(message,name,e):
	chat.configure(state="normal") # allow message to be entered into chat widget
	chat.insert(END,"<{}> {}\n".format(name,message)) # insert message into chat widget
	chat.configure(state="disabled") # prevent text from being modified by the user
	chat.see("end") # auto scroll chat window to bottom
	if name=="User":
		entry.delete(0,END) # clear message entry widget
		send(bot.reply(message),bot.name,0) # bot speaks in relation to user's message

root=Tk() # create main window

chat=tkst.ScrolledText(root,state="disabled",width=50,height=20) # chat text will go here
chat.grid(row=0,column=0,columnspan=2)

entry=Entry(root) # user types message here
entry.grid(row=1,column=0,sticky="nesw")
entry.bind("<Return>",lambda e:send(entry.get(),"User",e)) # user can send message on return key press

submit=Button(root,text="Enter",command=lambda:send(entry.get(),bot.name,0)) # or click submit button to send message
submit.grid(row=1,column=1,sticky="nesw")

bot=Bot(botid=4,debug=False) # initialize bot
send(bot.greet(),bot.name,0) # get the bot to greet the user

root.mainloop()
