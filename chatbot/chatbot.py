import random,sqlite3,uuid,string

class Bot:
	"create a bot object"
	def __init__(self,botid=None,debug=False):
		self.debug=debug # if True then replies will be raw repetitions of the message fed to it
		if botid==None: # if no bot id supplied, we generate a new bot

			### LIKES/DISLIKES ###
			c.execute("SELECT word FROM knowledge WHERE category='noun' AND type='object'") # fetch objects
			objects=c.fetchall()
			c.execute("SELECT word FROM knowledge WHERE category='verb' AND tense='pres cont'") # fetch verbs
			verbs=c.fetchall()
			self.likes=[]
			self.likes.append(random.choice(objects)[0]) # random object like
			self.likes.append(random.choice(verbs[0])) # random verb like
			self.dislikes.append(random.choice(objects[0])) # random object dislike
			self.dislikes.append(random.choice(verbs[0])) # random verb dislike

			### PERSONALITY ###
			c.execute("SELECT word,type,id FROM knowledge WHERE category='personality'") # get personalities from knowledge
			personalities=c.fetchall() # store in personalities variable
			ps=random.choice(personalities) # select random personality
			self.personality=ps[0] # this holds the name of the personality
			self.formality=ps[1] # holds the formality associated with the personality (FORMAL, RELAXED, RANDOM)
			self.pid=ps[2] # need personality id if saving the bot

			### MOOD ###
			c.execute("SELECT word,type,id FROM knowledge WHERE category='mood'") # get moods from knowledge
			moods=c.fetchall() # store in moods variable
			mo=random.choice(moods) # select random mood for now
			self.mood=mo[0] # this holds the name of the mood
			self.attitude=mo[1] # this holds how the mood affects their attitude (positive or negative)
			self.mid=mo[2] # need mood id if saving the bot

			### NAME ###
			c.execute("SELECT word,type,id FROM knowledge WHERE category='name'") # get names from knowledge
			names=c.fetchall() # store in names variable
			na=random.choice(names) # choose random name
			self.name=na[0] # store name
			self.style=na[1] # store MASC/FEM/NEU (gives the bot more personality)
			self.nid=na[2] # need name id if saving the bot

			### CATCHPHRASE ###
			c.execute("SELECT word,id FROM knowledge WHERE type='catchphrase' AND category=(?)",(self.personality,)) # get catchphrases from knowledge
			catchphrases=c.fetchall() # store in catchphrases variable
			ca=random.choice(catchphrases) # choose random catchphrase
			self.catchphrase=ca[0] # store catchphrase
			self.cid=ca[1] # need catchphrase id if saving the bot

			### QUIRK ###
			c.execute("SELECT word,id FROM knowledge WHERE type='quirk' AND category=(?)",(self.personality,)) # get quirks from knowledge
			quirks=c.fetchall() # store in quirks variable
			qu=random.choice(quirks) # choose random quirk
			self.quirk=qu[0] # store quirk
			self.qid=qu[1] # need quirk id if saving the bot

			### SAVE THE BOT? ###
			print("i'm a new bot! want to save me to the database? y/n") # ask user if they want to save the bot
			ans=input() # wait for input y/n
			if ans.lower=="y": # lowercase it if user puts Y
				tempkey=str(uuid.uuid4()) # use to grab botid once saved and give it to the user
				c.execute("INSERT INTO bot_info (name,personality,catchphrase,quirk,temp_key,mood,likes,dislikes) VALUES (?,?,?,?,?,?,?,?)",(self.nid,self.pid,self.cid,self.qid,tempkey,self.likes,self.dislikes))
				con.commit() # commit bot to database
				c.execute("SELECT id FROM bot_info WHERE temp_key=(?)",(tempkey,)) # get botid using tempkey
				self.botid=c.fetchall()[0][0] # store botid
				c.execute("UPDATE knowledge SET temp_key=('') WHERE id=(?)",(self.botid,)) # set temp_key to nothing to save space
				con.commit() # commit the update
				print("ok! my id is {}, so use this to create me next time!".format(self.botid))
			else:
				print("ok, when this program ends, my personality will be gone.")
		else: # botid has been specified
			c.execute("SELECT name,personality,catchphrase,quirk,likes,dislikes,mood FROM bot_info WHERE id=(?)",(botid,)) # get bot from database
			info=c.fetchall()[0] # fetch first result because there should only be one anyway
			self.nid=info[0] # name id
			self.pid=info[1] # personality id
			self.cid=info[2] # catchphrase id
			self.qid=info[3] # quirk id
			self.likes=info[4] # likes
			self.dislikes=info[5] # dislikes
			self.mid=info[6] #  mood id
			self.botid=botid # botid

			### NAME ###
			c.execute("SELECT word,type FROM knowledge WHERE id=(?)",(self.nid,)) # get name info
			na=c.fetchall()[0]
			self.name=na[0] # name as word
			self.style=na[1] # style (MASC,FEM,NEU)

			### PERSONALITY ###
			c.execute("SELECT word,type FROM knowledge WHERE id=(?)",(self.pid,)) # get personality info
			pe=c.fetchall()[0]
			self.personality=pe[0] # personality as word
			self.formality=pe[1] # formality (FORMAL,RELAXED,RANDOM)

			### CATCHPHRASE ###
			c.execute("SELECT word FROM knowledge WHERE id=(?)",(self.cid,)) # get catchphrase info
			ca=c.fetchall()[0]
			self.catchphrase=ca[0] # catchphrase as word(s)

			### QUIRK ###
			c.execute("SELECT word FROM knowledge WHERE id=(?)",(self.qid,)) # get quirk info
			qu=c.fetchall()[0]
			self.quirk=qu[0] # quirk as word(s)

			### MOOD ###
			c.execute("SELECT word,type FROM knowledge WHERE id=(?)",(self.mid,)) # get mood info
			mo=c.fetchall()[0]
			self.mood=mo[0] # mood as word
			self.attitude=mo[1] # attitude (POSITIVE or NEGATIVE)

	def greet(self,mode=0):
		if mode==0:
			c.execute("SELECT word FROM knowledge WHERE type=(?) AND category='greeting'",(self.personality,))
			greetings=c.fetchall()
			g=random.choice(greetings)[0]
			quirk_chance=random.randint(0,1)
			if quirk_chance==0:
				greeting=g
			else:
				greeting="{}, {}".format(g,self.quirk)
			if self.personality=="CUTE":
				greeting=greeting+"!!"
			return greeting

		elif mode=="response":
			form=self.formality
			forms=["RELAXED","FORMAL"]
			if form=="random":
				form=random.choice(forms)

			if form=="FORMAL":
				personal="i am"
			else:
				personal="i'm"

			response="{} {}".format(personal,self.mood)

			return response


	def ask(self):
		c.execute("SELECT word FROM knowledge WHERE type=(?) AND category='question'",(self.personality,))
		questions=c.fetchall()
		q=random.choice(questions)[0]
		phrase_chance=random.randint(0,1)
		if phrase_chance==0:
			question=q
		else:
			question="{} {}".format(self.catchphrase,q)
		return question

	def reply(self,message):

		raw=message # keeps the message in its original form if needed later

		for char in string.punctuation:
			raw=raw.replace(char,"") # remove all non letter/number characters
		words=raw.split(" ") # separate words into an array

		phrases={}
		c.execute("SELECT word,type FROM reply") # get all phrases
		for row in c.fetchall():
			phrases.update({row[0]:row[1]}) # store phrases in a dictionary

		command=None
		for phrase in phrases:
			p=phrase
			phrase=phrase.split(",")
			if phrase[0] in words:
				index=words.index(phrase[0])
				if len(phrase)==1:
					command=phrases[p]
				else:
					sequence=[]
					for word in phrase:
						if index<len(words):
							if words[index]==word:
								sequence.append(True)
							else:
								sequence=[]
						else:
							sequence=[]
						index+=1
					if len(sequence)==len(phrase):
						command=phrases[p]
			if phrases[p]=="laugh":
				for word in words:
					if phrase[0] in word:
						command=phrases[p]

		# decide how to reply
		if command=="greeting":
			return self.greet()
		elif command=="greetQ":
			return self.greet("response")
		elif command=="laugh":
			return self.laugh()

		if self.debug==True: # if debug mode is on
			return words # say raw user input
		else:
			return self.speak() # if not, say something random

	def laugh(self):
		if self.personality=="CUTE":
			return "hehe"
		elif self.personality=="COOL":
			return "ha"
		elif self.personality=="INTROVERTED":
			return "*giggles*"
		elif self.personality=="NORMAL":
			return "haha"
		elif self.personality=="EXOTIC":
			return "haw haw haw."

	def learn(self):
		pass

	def speak(self,mode=None,**kwargs):
		try:
			length=kwargs["length"] # if the user defined the length set it here
		except KeyError:
			length=random.choice(["short","medium"]) # if they didnt pick a random length

		try:
			subject=kwargs["subject"] # if the user defined a subject set it here
		except KeyError:
			c.execute("SELECT type FROM knowledge WHERE category='noun'") # if they didnt get subjects
			sjs=c.fetchall()
			subjects=[]
			for sj in sjs:
				sj=sj[0].split(",")
				for s in sj:
					if s not in subjects:
						subjects.append(s)
			subject=random.choice(subjects) # pick a random subject from all the subjects found in knowledge

		c.execute("SELECT id,word,vc FROM knowledge WHERE category='article'")
		articles=c.fetchall()
		c.execute("SELECT id,word,type,vc,adj_type FROM knowledge WHERE category='noun'")
		nouns=c.fetchall()
		c.execute("SELECT id,word,type,tense,conjunction,conj_type,adv_type FROM knowledge WHERE category='verb'")
		verbs=c.fetchall()
		c.execute("SELECT id,word,type FROM knowledge WHERE category='adverb'")
		adverbs=c.fetchall()
		c.execute("SELECT id,word,type FROM knowledge WHERE category='adjective'")
		adjectives=c.fetchall()
		c.execute("SELECT id,word,type FROM knowledge WHERE category='conjunction'")
		conjunctions=c.fetchall()

		if mode=="myself":
			return "hewwo"

		if length=="short":
			#short sentences are simple, using no adjectives or adverbs
			#they are things like "the dog is walking" or "she is eating"
			#they dont go into any detail

			### selecting article ###
			a=random.choice(articles)[0]

			### selecting noun ###
			possibleNouns=[]
			for noun in nouns:
				if subject.upper() in noun[2].split(","):
					possibleNouns.append(noun[0])
			n=random.choice(possibleNouns)

			### selecting verb ###
			c.execute("SELECT type FROM knowledge WHERE id=(?)",(n,))
			nTs=c.fetchall()[0][0].split(",")
			possibleVerbs=[]
			for verb in verbs:
				for nT in nTs:
					if nT in verb[2]:
						possibleVerbs.append(verb[0])
			v=random.choice(possibleVerbs)

			### setting tense ###
			c.execute("SELECT tense FROM knowledge WHERE id=(?)",(v,))
			tense=c.fetchall()[0][0]
			if tense=="pres cont":
				vt="is "
			elif tense=="past":
				vt=""
			elif tense=="past cont":
				vt="was "
			elif tense=="past perf":
				vt="had been "
			elif tense=="present":
				vt=""

			### setting a/an if chosen ###
			c.execute("SELECT vc FROM knowledge WHERE id=(?)",(n,))
			nVc=c.fetchall()[0][0]
			if a==2 or a==3:
				if nVc=="c":
					a="a"
				else:
					a="an"
			else:
				c.execute("SELECT word FROM knowledge WHERE id=(?)",(a,))
				a=c.fetchall()[0][0]

			### setting all other variables from ids ###
			c.execute("SELECT word FROM knowledge WHERE id=(?)",(n,))
			n=c.fetchall()[0][0]
			c.execute("SELECT word FROM knowledge WHERE id=(?)",(v,))
			v=c.fetchall()[0][0]

			### construct sentence ###
			sentence="{} {} {}{}".format(a,n,vt,v)

		elif length=="medium":
			'''
			medium sentences use two articles and two nouns
			e.g. my cat is walking with his dog
			'''

			### selecting first article ###
			a1=random.choice(articles)[0]

			### selecting first noun ###
			possibleNouns=[]
			for noun in nouns:
				if subject.upper() in noun[2].split(","):
					possibleNouns.append(noun[0])
			n1=random.choice(possibleNouns)

			### selecting verb ###
			c.execute("SELECT type FROM knowledge WHERE id=(?)",(n1,))
			nTs=c.fetchall()[0][0].split(",")
			possibleVerbs=[]
			for verb in verbs:
				for nT in nTs:
					if nT in verb[2]:
						possibleVerbs.append(verb[0])
			v=random.choice(possibleVerbs)

			### setting tense ###
			c.execute("SELECT tense FROM knowledge WHERE id=(?)",(v,))
			tense=c.fetchall()[0][0]
			if tense=="pres cont":
				vt="is "
			elif tense=="past":
				vt=""
			elif tense=="past cont":
				vt="was "
			elif tense=="past perf":
				vt="had been "
			elif tense=="present":
				vt=""

			### setting first a/an if chosen ###
			c.execute("SELECT vc FROM knowledge WHERE id=(?)",(n1,))
			nVc=c.fetchall()[0][0]
			if a1==2 or a1==3:
				if nVc=="c":
					a1="a"
				else:
					a1="an"
			else:
				c.execute("SELECT word FROM knowledge WHERE id=(?)",(a1,))
				a1=c.fetchall()[0][0]

			''' ### picking conjunction ###
			possible_conjunctions={}
			for conj in conjunctions:
				if conj in verbs_conjunctions[v][0]:
					index=verbs_conjunctions[v][0].index(conj)
					possible_conjunctions.update({conj:index})
			c=random.choice(list(possible_conjunctions))
			'''
			possible_conjunctions={}
			for verb in verbs:
				verbid=verb[0]
				if verbid==v:
					conjs=verb[4].split(",")
					conjs_n=verb[5].split(",")
					cj=random.choice(conjs)
					cj_n=conjs_n[conjs.index(cj)]

			### selecting second noun ###
			possibleNouns=[]
			for noun in nouns:
				if cj_n in noun[2].split(","):
					possibleNouns.append(noun[0])
			n2=random.choice(possibleNouns)

			### selecting second article ###
			a2=random.choice(articles)[0]

			### settings second a/an if chosen ###
			c.execute("SELECT vc FROM knowledge WHERE id=(?)",(n2,))
			nVc=c.fetchall()[0][0]
			if a2==2 or a2==3:
				if nVc=="c":
					a2="a"
				else:
					a2="an"
			else:
				c.execute("SELECT word FROM knowledge WHERE id=(?)",(a2,))
				a2=c.fetchall()[0][0]

			### setting all other variables from ids ###
			c.execute("SELECT word FROM knowledge WHERE id=(?)",(n1,))
			n1=c.fetchall()[0][0]
			c.execute("SELECT word FROM knowledge WHERE id=(?)",(n2,))
			n2=c.fetchall()[0][0]
			c.execute("SELECT word FROM knowledge WHERE id=(?)",(v,))
			v=c.fetchall()[0][0]

			sentence="{} {} {}{} {} {} {}".format(a1,n1,vt,v,cj,a2,n2)

		return sentence


con=sqlite3.connect("./chatbot/knowledge.db")
c=con.cursor()
