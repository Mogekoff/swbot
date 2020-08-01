import time
import vk_api
import codecs
class bot:
	__login = ''
	__password = ''
	__convID = 0

	__membersInfo = []
	__messagesHistory = []

	__lastMessage = ''
	__lastMessageID = 0
	__lastMessageAction = ''
	__lastPersonName = ''
	__lastPersonID = 0
	__actionObjectID = 0
	__membersCount = 0
	__forwardPersonID = 0
	
	blackList = []
	wordsFilter = []

	with open('data','r') as f:                                
			try:
				i=0
				for Str in f:
					if i == 0:
						Str = Str[:-1]
						__login  = Str
					if i == 1:
						Str = Str[:-1]
						__password=Str 
					if i == 2:
						__convID = int(Str)
					i+=1
				vk_session = vk_api.VkApi(__login, __password)
				vk_session.auth()
				vk = vk_session.get_api()
				tools = vk_api.VkTools(vk_session)
				print("login\t\t= " + __login + "\npassword\t= " + __password + "\nconvID\t\t= ",end='')
				print(__convID)
			except:
				print("Account Access Denied")	#авторизация
	with open('blackList','r') as f:                                
		try:
			for Str in f:
				Str = Str.replace('\n','')
				blackList.append(int(Str))
			print("BlackList \t= ", end='')
			print(blackList)
		except:
			print("Blacklist Init Error")
	with codecs.open('filter','r', 'utf-8') as f:                   
				try:
					for Str in f:
						Str = Str[:-2]
						wordsFilter.append(Str)
					print("WordsFilter = ",end='')
					print(wordsFilter)
				except:
					print("Filter Init Error")

	__membersInfo=vk.messages.getConversationMembers(peer_id=__convID)
	__membersCount = __membersInfo['count']

	def bPrint(self, text):
		print('\n!***BOT***!: ' + text + "\n")
	def isAdmin(self, id):
		i=0
		while i<self.__membersCount:                               
			if self.__membersInfo['items'][i]['member_id']==id:           
				try:                                       
					return self.__membersInfo['items'][i]['is_admin']
				except:
					return False
			i+=1
		self.bPrint("def isAdmin(): This person is not in conversation, id = " + str(id))
		return False	
	def send(self, msg, forward=False):
		if msg=='':
			self.bPrint("def send(): Error, empty string")
			return False
		try:
			if forward:
				self.vk.messages.send(peer_id=self.__convID, forward_messages=self.__lastMessageID, message=str(msg))
			else:
				self.vk.messages.send(peer_id=self.__convID,  message=str(msg)) 
		except:
			self.bPrint("def send(): Error, msg = " + msg)
	def addUserToChat(self,id):
		if self.isFriend(self.getForwardPersonID()):
			if self.isUserInChat(id):
				self.bPrint("def addUserToChat(): The user is in chat already.")
				return False
			else:
				self.vk.messages.addChatUser(chat_id=self.__convID-2000000000, user_id=id)
				return True
		else:
			self.bPrint("def addUserToChat(): The user is not bot's friend.")
			return False
	def kick(self, id):
		if self.isAdmin(id):
			self.bPrint("def kick(): Try of kick admin")
			return False
		try:
			self.vk.messages.removeChatUser(chat_id=self.__convID-2000000000,user_id=id)
			return True
		except:
			self.bPrint("def kick(): Error, id = " + str(id))
			return False	
	def ban(self, id):
		if self.isAdmin(id):
			return False
		try:
			i=0
			while i<len(self.blackList):     
				if self.blackList[i] == id:
					return False
				i+=1
			self.blackList.append(id)
			self.vk.messages.removeChatUser(chat_id=self.__convID-2000000000, user_id=id)
			with open('blackList','a') as f:
				try:
					f.write('\n' + str(id))
					return True
				except UnicodeEncodeError:
					self.bPrint("def ban(): Error of adding to BlackList file")
					return False
		except:
			self.bPrint("def ban(): Can't remove user. id = " + str(id))
			return False
	def getName (self, id, case="nom"):
		if id <= 0:
			self.bPrint("def getName(): Error, 'id' can't be >=0, id = " + str(id))
			return False
		try:
			usr = self.vk.users.get(user_ids=id, name_case=case)
			return usr[0]["first_name"] + " " + usr[0]["last_name"]
		except:
			self.bPrint("def getName(): Error, id = " + str(id) + ", case = " + case)
			return False	
	def haveNewMessage(self):
		try:
			self.__messagesHistory = self.vk.messages.getHistory(count=1, peer_id=self.__convID)
			if self.__messagesHistory['items'][0]['id']!=self.__lastMessageID:
				self.__lastMessage = self.__messagesHistory['items'][0]['text']
				self.__lastPersonID = self.__messagesHistory['items'][0]['from_id']
				try:	
					self.__lastMessageAction = self.__messagesHistory['items'][0]['action']['type']
					self.__actionObjectID = self.__messagesHistory['items'][0]['action']['member_id']
				except:
					self.__lastMessageAction = 'None'
					self.__actionObjectID = self.__lastPersonID
				self.__lastMessageID = self.__messagesHistory['items'][0]['id']
				self.__lastPersonName = self.getName(self.__lastPersonID)
				try:	
					self.__forwardPersonID = self.__messagesHistory['items'][0]['fwd_messages'][0]['from_id']
				except:
					self.__forwardPersonID = 0
				if self.__lastMessage != '':
					print(self.__lastPersonName + ": " + self.__lastMessage)
				return True
			else:
				return False
		except:
			time.sleep(1)
			self.haveNewMessage()
	def checkMembersChanged(self):
		if self.__lastMessageAction=='None':
			return
		else:
			try:
				self.__membersInfo=self.vk.messages.getConversationMembers(peer_id=self.__convID)
				self.__membersCount = self.__membersInfo['count']
				if self.__lastMessageAction == 'chat_invite_user' and self.__actionObjectID<0:
					self.bPrint("There was added in conversation a conversation.")
					self.send("Зачем ты добавил сюда [club"+str(-(self.__actionObjectID))+"|этих сектантов]?")
					return True
				if self.__lastMessageAction == 'chat_kick_user' and self.__actionObjectID<0:
					self.bPrint("There was deleted a conversation from conversation.")
					self.send("Репрессировать [club"+str(-(self.__actionObjectID))+"|ублюдков]!")
					return True
				if self.__lastMessageAction == 'chat_invite_user' and self.__actionObjectID!=self.__lastPersonID:
					self.bPrint(self.getName(self.__lastPersonID)+" added in conversation " + self.getName(self.__actionObjectID))
					self.send("Наши ряды пополнил [id"+str(self.__actionObjectID)+"|"+self.getName(self.__actionObjectID)+"]!")
					return True
				if self.__lastMessageAction == 'chat_invite_user_by_link' and self.__actionObjectID != self.__lastPersonID:
					self.bPrint(self.getName(self.__actionObjectID)+" invited by link.")
					self.send("По тайному проходу наше племя было найдено [id"+str(self.__actionObjectID)+"|"+self.getName(self.__actionObjectID,'ins')+"]!")
					return True
				if self.__lastMessageAction == 'chat_kick_user' and self.__actionObjectID!=self.__lastPersonID:
					self.bPrint(self.getName(self.__lastPersonID)+" kicked from conversation " + self.getName(self.__actionObjectID))
					self.send("Сегодня утром был найден труп [id"+str(self.__actionObjectID)+"|"+self.getName(self.__actionObjectID,'gen')+"]!")
					return True
				if self.__lastMessageAction == 'chat_invite_user' and  self.__actionObjectID==self.__lastPersonID:
					self.bPrint(self.getName(self.__actionObjectID)+" came back to conversation.")
					self.send("Вернулся, не запылился [id"+str(self.__actionObjectID)+"|"+self.getName(self.__actionObjectID)+"]!")
					return True
				if self.__lastMessageAction == 'chat_kick_user' and  self.__actionObjectID==self.__lastPersonID:	
				 	self.bPrint(self.getName(self.__actionObjectID)+" leaved the conversation.")
				 	self.send("Скатертью дорога, [id"+str(self.__actionObjectID)+"|"+self.getName(self.__actionObjectID)+"]!")
				 	return True
			except:
				self.bPrint("def checkMembersChanged(): Error, __lastMessageAction = "+ self.__lastMessageAction + ", __actionObjectID = " + str(self.__actionObjectID) + ", __lastPersonID = " + str(self.__lastPersonID))
				return False
	def checkPhrase(self):
		with codecs.open('answers','r', 'utf-8') as f:          #ответочки             
			try:
				msg = self.__lastMessage
				msg = msg.lower() 
				for ask in f:
					ask = ask[:-2]
					ask = ask.replace('=',',')
					ask = ask.split(',')
					answer = ask[-1]
					ask = ask[:-1]
					for i in ask:
						if msg == i:
							self.vk.messages.send(peer_id=self.__convID,forward_messages=self.__lastMessageID, message=answer)
							break
			except:
				self.bPrint("def checkPhrase(): Phrases Check Error, __lastMessage = "+self.__lastMessage)
	def checkBannedMembers(self):
		i=0
		while(i<self.__membersCount):                                  #цикл проверки участников из черного списка
			j=0
			while(j<len(self.blackList)):
				if self.__membersInfo['items'][i]['member_id']==self.blackList[j]:
					self.kick(self.__membersInfo['items'][i]['member_id'])
					break
				j+=1
			i+=1
	def checkCommand(self, command, arg='all', admin=False):
		if admin:
			if not(self.isAdmin(self.__lastPersonID)):
				return False
		list = self.__lastMessage.split(' ')
		if list[0] == command and arg == 'exist':
			return True
		elif list[0] == command and arg == 'one':
			try:
				return list[1]
			except:
				return True
		elif list[0] == command and arg == 'all':
			string = self.__lastMessage.replace(command,'')
			return string[1:]
		else:
			return False
	def checkAskToAdd(self):
		try:
			askSearch = self.vk.messages.search(q="4r3g43reg34",count=1, extended=1)
			i=0

			if isUserInChat(askSearch['items'][0]['from_id']):
				return False
			else:
				self.vk.messages.addChatUser(chat_id=self.__convID-2000000000, user_id=askSearch['items'][0]['from_id'])
				return askSearch['items'][0]['from_id']
		except:
			return False
	def checkWordsFilter(self):
		if self.isAdmin(self.__lastPersonID):
			return
		i=0
		while(i<len(self.wordsFilter)):                                    #цикл проверки последнего сообщения по фильтру слов
			word = self.__lastMessage.lower()                               #приводит последнее сообщение-строку в нижний регистр для удобства
			if word.find(self.wordsFilter[i])!=-1:                         #ищет в последнем сообщение слова по фильтру
				if self.kick(self.__lastPersonID):
					self.vk.messages.send(peer_id=self.__convID,forward_messages=self.__lastMessageID, message="Помогите избавиться от [id" + str(self.__lastPersonID) + "|трупа], пожалуйста!")
					break
				else:
					self.bPrint("def checkWordsFilter(): Can't kick the person. __lastPersonID = "+str(self.__lastPersonID)+", wordsFilter["+str(i)+"] = "+self.wordsFilter[i]+", __lastMessage = "+ self.__lastMessage)
			i+=1
	def isFriend(self,id):
		if id<=0:
			return False
		friend = self.vk.friends.areFriends(user_ids=id)
		if friend[0]['friend_status']==3:
			return True
		else:
			return False
	def isUserInChat(self,id):
		i=0
		while i<self.__membersCount:                               
			if self.__membersInfo['items'][i]['member_id']==id:                                  
				return True
			i+=1
		return False
	def getLastMessage(self):
		return self.__lastMessage
	def getLastMessageID(self):
		return self.__lastMessageID
	def getLastPersonName(self):
		return self.__lastPersonName
	def getLastPersonID(self):
		return self.__lastPersonID
	def getMembersCount(self):
		return self.__membersCount
	def getForwardPersonID(self):
		return self.__forwardPersonID


#автоматизировать сообщения приветствия из cfg файла