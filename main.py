#################################################Аутентификация#########################################################

import vk_api
import time
import codecs
import random


login, password = '',''            				#логин и пароль от аккаунта бота
con = 0                                      	#id беседы (2000000000 + id)
adminID = 0                                     #id админа (создателя беседы)
filter = []                                     #фильтр запрещенных слов (слова, строки)
blackList = []                                  #черный список (id)

with open('data','r') as f:                                 #получает логин и пароль из файла data
                try:
                	i=0
                	for string in f:
                		if i == 0:
                			string = string[:-1]
                			login=string
                		if i == 1:
                			string = string[:-1]
                			password=string 
                		if i == 2:
                			string = string[:-1]
                			con = int(string)
                		if i == 3:
                			adminID = int(string)
                		i+=1
                except:
                	print("Account Access Denied")

with open('blacklist','r') as f:                                #заполнение массива blacklist из файла
                try:
                    for string in f:
                        string = string.replace('\n','')
                        blackList.append(str(string))
                except:
                    print("Blacklist Init Error")

with codecs.open('filter','r', 'utf-8') as f:                   #заполнение массива с "плохими" словами
                try:
                    for string in f:
                        string = string[:-2]
                        filter.append(string)
                except:
                    print("Filter Init Error")



vk_session = vk_api.VkApi(login, password)              #передача логина и пароля для создания объекта сессии

vk_session.auth()                                       #аутентификация

vk = vk_session.get_api()                               #получение api

tools = vk_api.VkTools(vk_session)

random.seed(version=2)
#команды
commandsList = ["!изгнанные", "!изгнать", "!убить", "!воскресить", "!посвятить", "!ритуалы", "!айди", "!жертвоприношение", "!рулетка"]
#текст последнего сообщения в беседе
msgLast = ""
#Имя, фамилия, отправившего человека
name = ""
#id человека, отправившего посл. сообщение
id = 0
#id последнего сообщения
msgID = 0
###################################################Логика###############################################################

def main(msgLast, id, msgID, name):         #главная логика программы
    #vk.messages.send(peer_id=con, message="&#128035;")           #отправляет смайлик цыпленка (мол, скрипт стартовал)
    global mem 
    mem = vk.messages.getConversationMembers(peer_id=con)   #получение инф. об участниках беседы
    while(1):
        try:
            msg = vk.messages.getHistory(count=1, peer_id=con)      #получение истории сообщений
        except:
            time.sleep(1)
            msg = vk.messages.getHistory(count=1, peer_id=con)
        if(str(msg['items'][0]['text'])!=msgLast):
            msgLast = str(msg['items'][0]['text'])                  #получаем и записываем текст посл. сообщения
            id = msg['items'][0]['from_id']                         #получ. и запис. айди отправителя посл. сообщения
            msgID = msg['items'][0]['id']                                                   #записываем id самого посл. сообщения
           
            if msgLast =='':
                try:   
                    if (msg['items'][0]['action']['type']=="chat_invite_user" or msg['items'][0]['action']['type']=="chat_invite_user_by_link") and msg['items'][0]['action']['member_id']!=id:
                        mem = vk.messages.getConversationMembers(peer_id=con)
                        vk.messages.send(peer_id=con, message="Сегодня наши ряды пополнил [id"+str(msg['items'][0]['action']['member_id'])+"|"+getName(msg['items'][0]['action']['member_id'])+"]!")
                        msgLast=" добавил в беседу " + getName(msg['items'][0]['action']['member_id'],"gen")
                    
                    if msg['items'][0]['action']['type']=="chat_kick_user" and msg['items'][0]['action']['member_id']!=id:
                        mem = vk.messages.getConversationMembers(peer_id=con)
                        vk.messages.send(peer_id=con, message="Пару секунд назад был репрессирован [id"+str(msg['items'][0]['action']['member_id'])+"|"+getName(msg['items'][0]['action']['member_id'])+"]!")
                        msgLast=" исключил из беседы " + getName(msg['items'][0]['action']['member_id'],"gen")
                        
                    if msg['items'][0]['action']['type']=="chat_invite_user" and msg['items'][0]['action']['member_id']==id:
                        mem = vk.messages.getConversationMembers(peer_id=con)
                        vk.messages.send(peer_id=con, message="[id"+str(id)+"|"+getName(id)+"] вернулся. Не запылился.")
                        msgLast=" вернулся(лась) в беседу."
                            
                    if msg['items'][0]['action']['type']=="chat_kick_user" and msg['items'][0]['action']['member_id']==id:
                        mem = vk.messages.getConversationMembers(peer_id=con)
                        vk.messages.send(peer_id=con, message="Ну и проваливай, [id"+str(id)+"|козёл]!")
                        msgLast=" покинул(а) беседу."    
                except:
                    print("Picture or sticker or another action")
                name = getName(id)                                      #получаем имя фамилию и записываем в переменную name
                print("~ " + name + msgLast)
                with codecs.open('logs','a', 'utf-8') as f:                         #ведение логов
                    try:
                        f.write("~ " + name + msgLast + '\n')
                    except UnicodeEncodeError:
                        f.write(":emoji:" + '\n')
            else:
                name = getName(id)
                print(name + ": " + msgLast)
                with codecs.open('logs','a', 'utf-8') as f:                         #ведение логов
                    try:
                        f.write(name + ": " + msgLast + '\n')
                    except UnicodeEncodeError:
                        f.write(":emoji:" + '\n')

        
        else:
            time.sleep(1)
            continue
        ####
        reqMessage = vk.messages.search(q="Смерть - это скучно",count=1, extended=1)            #добавление в конфу по фразе

        i=0
        while(i<mem['count']):
            if mem['items'][i]['member_id'] == reqMessage['items'][0]['from_id']:
                break
            i+=1
            if i==mem['count']:
                vk.messages.addChatUser(chat_id=con-2000000000, user_id=reqMessage['items'][0]['from_id'])

        ####
        i=0
        while(i<len(filter)):                                    #цикл проверки последнего сообщения по фильтру слов
            word = msgLast.lower()                               #приводит последнее сообщение-строку в нижний регистр для удобства
            if word.find(filter[i])!=-1:                         #ищет в последнем сообщение слова по фильтру
                msgKick(id, msgID)
                break
            i+=1

        
        with codecs.open('answers','r', 'utf-8') as f:          #ответочки             
            try:
                msg = msgLast
                msg = msg.lower() 
                for ask in f:
                    ask = ask[:-2]
                    ask = ask.replace('=',',')
                    ask = ask.split(',')
                    answer = ask[-1]
                    ask = ask[:-1]
                    for i in ask:
                        if msg == i:
                            vk.messages.send(peer_id=con,forward_messages=msgID, message=answer)
                            break
            except:
                print("Answers Error")

        i = 0
        while (i < len(commandsList)):                                  # цикл проверки команд
            firstWord = msgLast.split(' ')
            if firstWord[0] == commandsList[i]:
                commandsControl(msgLast, msgID, id)
                break
            i+=1


        i=0
        while(i<mem['count']):                                  #цикл проверки участников из черного списка
            j=0
            while(j<len(blackList)):
                if(str(mem['items'][i]['member_id'])==blackList[j]):
                    memKick(mem['items'][i]['member_id'],mem['items'][i]['invited_by'])
                    break
                j+=1
            i+=1


        if(msgLast=="🐤"):                                       #выключает скрипт по кодовой фразе(можно добавить рандом)
            break

        time.sleep(1)                                           #период в секунду, чтобы не грузить сервер/получать капчу

    vk.messages.send(peer_id=con, message="🐥")           #отправляет смайл цыпленка, конец скрипта

###################################################Функции кика#########################################################

def justKick(id):           #просто кик
    if isAdmin(id):
        return False
    try:
        vk.messages.removeChatUser(chat_id=con-2000000000,user_id=id)
        vk.messages.send(peer_id=con, message="Сегодня утром нашли [id" + str(id) + "|труп] человека...")
        return True
    except:
        vk.messages.send(peer_id=con, message="То, что мертво, умереть не может...")
        print("Can't remove user. Is he yet removed?")
        return False
def msgKick(id, msgID):           #фильтр слов(функция)
    if isAdmin(id):
        return
    vk.messages.send(peer_id=con,forward_messages=msgID, message="Что за мерзкие вещи [id" + str(id) + "|ты] говоришь? А ну, пшёл вон!")
    vk.messages.removeChatUser(chat_id=con-2000000000,user_id=id)

def memKick(id, inv_id):    #черный список(функция)
    if isAdmin(id):                          #провека пригласившего/забаненного на админство
        resurrect(id)
        return
    else:
        vk.messages.removeChatUser(chat_id=con-2000000000, user_id=id)    #кикает человека из черного списка
        vk.messages.send(peer_id=con, message="Ходит легенда, что [id" + str(id) + "|этот человек] был изгнан из нашего племени...")
        vk.messages.send(peer_id=con, message="Мы нашли [id"+str(inv_id)+"|предателя]!")
        vk.messages.removeChatUser(chat_id=con-2000000000, user_id=inv_id)#кикает человека, пригласившего забаненного

def memAdd(id, msgID=''):          #добавляет человека в конфу
    try:
        vk.messages.addChatUser(chat_id=con-2000000000, user_id=id)
        vk.messages.send(peer_id=con, message="Сегодня наши ряды пополнил [id"+id+"|"+getName(id)+"]!")
    except:
        vk.messages.send(peer_id=con,forward_messages=msgID, message="Глаза разуй, ёпта, он уже тут.")
def resurrect(id):                  #убирает из черного списка
    try:
        blackList.remove(id)
        with open('blacklist','w') as f:                                
                try:
                    for string in blackList:
                        f.write('\n' + string)
                except:
                    print("Blacklist Rewriting Error. ")
    except:
        print("Resurrect Error. Was this man in blacklist?")
###########################################Внутренние функции получения###################################################
def isAdmin(id):            #проверяет на админство
    i=0
    while i<mem['count']:                               #проверяет админ ли отправитель сообщения
        if mem['items'][i]['member_id']==id:            #если айди участника конфы == айди отправителя
            try:                                        #tryExcept здесь потому что если отправитель не админ, то слот isAdmin отсутствует
                return mem['items'][i]['is_admin']   #и тогда это выдаст ошибку
            except:
                return False
        i+=1

def getName (id, case="nom"):       #получает имя\фамилию по айди
    usr = vk.users.get(user_ids=id, name_case=case)
    name = usr[0]["first_name"] + " " + usr[0]["last_name"]
    return name                                                     #получаем имя фамилию и записываем в переменную name


####################################################Команды#############################################################



def commandsControl(command, msgID, id):            #комадный контроль
    if command == "!изгнанные":
        commandBanned(msgID)
        return
    if command == "!ритуалы":
        rituals(msgID)
    
    #админские команды - обычные
    if isAdmin(id):
        if command == "!айди":
            showID(msgID)
        if command == "!жертвоприношение":
            sacrifice()

    #команды с параметрами - обычные
    command = command.split(' ')
    if command[0] == "!посвятить":
        memAdd(command[1], msgID)
        return
    if command[0] == "!рулетка":
        try:
            roulette(msgID, id, int(command[1]))
        except:
            roulette(msgID, id)
    
    #админские команды - проверка на id
    if isAdmin(id):
        if command[0] == "!изгнать":
            addToBlackList(command[1])
            return
        if command[0] == "!убить":
            justKick(command[1])
            return
        if command[0] == "!воскресить":
            resurrect(command[1])
            return
    return
def rituals(msgID):         #список команд
    message = " &#127773; Для холопов: \n!посвятить [id] - Добавляет человека в беседу \n!ритуалы - Выводит список команд\n!изгнанные - Выводит список забаненных без права возвращения\n!конституция - Свод законов нашего государства\n!карма - Твоя репутация\n!цитата [text] - Сохранить цитату\n!скрин - Скринит пересланные сообщения\n!рулетка [1-6] - Сыграть в русскую рулетку\n!дуэль - Приглашение на дуэль\n!масти - Кастовая система беседы \n\n &#127770; Для привилегированных: \n!жертвоприношение - Кикает случайного человека\n!изгнать [id] - Добавляет человека в черный список [id]\n!воскресить [id] - Убирает человека из черного списка\n!убить [id] - Кикает из беседы\n!айди - Выводит список айди участников"
    vk.messages.send(peer_id=con,forward_messages=msgID, message=message)

def commandBanned(msgID):       #!изгнанные
    i=0
    string = ""
    while (i < len(blackList)):  # цикл проверки последнего сообщения по фильтру слов
        string+="vk.com/id" + blackList[i] + '\n'
        i+=1
    vk.messages.send(peer_id=con, forward_messages=msgID, message=string)

def addToBlackList(parametr):           #добавляет в черный список
    if isAdmin(parametr):
        resurrect(parametr)
        return
    try:
        i=0
        while i<len(blackList):     
            if blackList[i] == parametr:
                return
            i+=1
        blackList.append(parametr)
        vk.messages.removeChatUser(chat_id=con-2000000000, user_id=int(parametr))
        with open('blacklist','a') as f:
            try:
                f.write('\n' + parametr)
            except UnicodeEncodeError:
                print("Error of adding to BlackList file")
    except:
        print("Error. Is banner admin? Is id exist?")
        return

def showID(msgID):      #выводит айди участников
    

def sacrifice():    #жертвоприношение
    try: 
        vk.messages.removeChatUser(chat_id=con-2000000000,user_id=mem['items'][random.randint(0, mem['count']-1)]['member_id'])
        vk.messages.send(peer_id=con, message="Жертва была принесена.")
    except:
        sacrifice()

def roulette(msgID, id, num=1):     #русская рулетка
    if num>6 or num<1:
        vk.messages.send(peer_id=con, forward_messages=msgID, message="Долбоеб ебанный, ты в русскую рулетку-то играть хотя бы умеешь?")
        return
    if random.randint(1, 6)>num:
        vk.messages.send(peer_id=con, forward_messages=msgID, message="Новичкам всегда везет.")
    else:
        vk.messages.send(peer_id=con, forward_messages=msgID, message="Без лоха и жизнь не та.")
        vk.messages.removeChatUser(chat_id=con-2000000000,user_id=id)


###################################################Старт################################################################

main(msgLast, id, msgID, name)                                                          #вызывает функцию бизнес-логики main()


#добавить логирование стикеров,картинок,видео
#добавить счетчик киков
#добавить голосования(в т.ч. вотекик)
#автозапуск скрипта при закрытии отдельным файлом .py и закрытие через него командой в конфе
#реализовать все задуманные команды