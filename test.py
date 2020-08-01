import bot
import random

Bot=bot.bot()
random.seed(version=2)

def cycle():
	#try:
		while(1):
			if Bot.haveNewMessage():
				Bot.checkMembersChanged()		#Изменилось ли кол-во участников
				Bot.checkPhrase()				#Проверяет фразы
				Bot.checkBannedMembers()		#Кикает забаненных
				Bot.checkWordsFilter()			#Кикает за запрещ. слова
				Bot.checkAskToAdd()				#Добавляет кикнутых
				if Bot.checkCommand("!рулетка", 'one'):
					arg = Bot.checkCommand("!рулетка", 'one')
					if arg == True:
						roulette()					
					else:
						try:
							roulette(int(arg))
						except:
							Bot.send("Пашол нахуй, не ломай бота.",True)				
				if Bot.checkCommand("!ритуалы", 'exist'):
					Bot.send(" &#127773; Для холопов: \n!посвятить [id] - Добавляет человека в беседу \n!ритуалы - Выводит список команд\n!изгнанные - Выводит список забаненных без права возвращения\n!конституция - Свод законов нашего государства\n!карма - Твоя репутация\n!цитата [text] - Сохранить цитату\n!скрин - Скринит пересланные сообщения\n!рулетка [1-6] - Сыграть в русскую рулетку\n!дуэль - Приглашение на дуэль\n!масти - Кастовая система беседы \n\n &#127770; Для привилегированных: \n!жертвоприношение - Кикает случайного человека\n!изгнать [id] - Добавляет человека в черный список [id]\n!воскресить [id] - Убирает человека из черного списка\n!убить [id] - Кикает из беседы\n!айди - Выводит список айди участников")				
				if Bot.checkCommand("!убить", 'one', True):
					arg=Bot.checkCommand("!убить", 'one', True)
					if arg==True:
						try:
							if Bot.getForwardPersonID() == 0:
								Bot.send("Ни айди, ни пересланного сообщения... тЫ еБаНуТыЙ???", True)
							else:
								Bot.kick(Bot.getForwardPersonID())
						except:
							Bot.bPrint("!убить: Error, arg = " + arg)
					else:
						try:
							
							Bot.kick(int(arg))
						except:
							Bot.bPrint("!убить: Error, arg = " + arg)
							Bot.send("То, что мертво, умереть не может", True)				
				if Bot.checkCommand("!айди", 'exist', True):
					if Bot.getForwardPersonID() == 0:
						Bot.send("Перешли сообщение, чтобы узнать айди этого человека, придурок.", True)
					else:
						Bot.send(Bot.getForwardPersonID(), True)
				if Bot.checkCommand("!посвятить", 'exist'):
					if Bot.getForwardPersonID() == Bot.getLastPersonID():
						Bot.send("Ты идиот?", True)
					elif Bot.isUserInChat(Bot.getForwardPersonID()):
						Bot.send("Глаза, ёпта, разуй. Он уже тут.",True)
					elif Bot.getForwardPersonID() == 0:
						Bot.send("Перешли сообщение того, кого хочешь добавить и допиши команду.", True)
					elif Bot.isFriend(Bot.getForwardPersonID()):
						Bot.addUserToChat(Bot.getForwardPersonID())
					else:
						Bot.send("Этот чудила тебе не друг. А недругов добавлять нельзя. Да.", True)
				if Bot.checkCommand("!изгнанные", 'one'):
					pass
				if Bot.checkCommand("!конституция", 'one'):
					pass
				if Bot.checkCommand("!карма", 'one'):
					pass
				if Bot.checkCommand("!цитата", 'one'):
					pass
				if Bot.checkCommand("!скрин", 'one'):
					pass
				if Bot.checkCommand("!дуэль", 'one'):
					pass
				if Bot.checkCommand("!масти", 'one'):
					pass
				if Bot.checkCommand("!жертвоприношение", 'one', True):
					pass
				if Bot.checkCommand("!изгнать", 'one', True):
					pass
				if Bot.checkCommand("!воскресить", 'one', True):
					pass
	#except:		
		#Bot.bPrint("Cycle Error")
		#cycle()
def roulette(num=1):
	try:
		if num>6 or num<1:
			Bot.send("Ты, долбоеб сука ебанный, в русскую рулетку-то играть умеешь?.", True)
			return False
		if random.randint(1, 6)>num:
			Bot.send("Ньюфагам всегда везёт.", True)
			return False
		else:
			Bot.kick(Bot.getLastPersonID())
			Bot.send("Без лоха и жизнь не та.", True)
			return True
	except:
		Bot.bPrint("def roulette(): Error, num = " + str(num))
cycle()