import random,sqlite3,uuid

class Bot:
	"create a bot object"
	def __init__(self,botid=0):
		if botid==0:
			c.execute("SELECT word,category FROM knowledge WHERE category='personality'")
			ps=c.fetchall()
			personalities=[]
			for p in ps:
				personalities.append(p[0])
			self.personality=random.choice(personalities)
			self.name="bot"
			self.catchphrase="what's new?"
			self.quirk="chirp"
			tempkey=str(uuid.uuid4())
			print("i'm a new bot! want to save me to the database? y/n")
			ans=input()
			if ans.lower=="y":
				c.execute("INSERT INTO bot_info (name,personality,catchphrase,quirk,temp_key) VALUES (?,?,?,?,?)",(self.name,self.personality,self.catchphrase,self.quirk,tempkey))
				con.commit()
				c.execute("SELECT id FROM bot_info WHERE temp_key=(?)",(tempkey,))
				self.botid=c.fetchall()[0][0]
				print("ok! my id is {}, so use this to create me next time!".format(self.botid))
			else:
				print("ok, when this program ends, my personality will be gone.")
		else:
			c.execute("SELECT * FROM bot_info WHERE id=(?)",(botid,))
			info=c.fetchall()[0]
			self.name=info[1]
			self.personality=info[2]
			self.catchphrase=info[3]
			self.quirk=info[4]
			self.botid=botid
			
		print(self.greet())

	def greet(self):
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

	def speak(self,length=random.choice(["short"]),subject=random.choice(["animal","place","food"])):
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

		if length=="short":
			'''
			short sentences are simple, using no adjectives or adverbs
			they are things like "the dog is walking" or "she is eating"
			they dont go into any detail
			'''
			
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


con=sqlite3.connect("knowledge.db")
c=con.cursor()
