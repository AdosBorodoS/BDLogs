from ast import Try
from datetime import datetime
from datetime import timedelta
from http import client
import telebot as tb
import os
import sys
import colorama as cg
from numpy import percentile

# mom's friend's son's logs



class ClientFileLogs:
    
    def __init__(self,log_way='logs.log',*args,**kwargs):
        '''    
        :param log_way: Принимает на вход путь и имя файла с логами, (Может принимать как существующий так и еще не созданный путь) =>(String)
        :return: Создает клиент с помощью которого можно управлять логами                                                           =>(No return)
        '''
        self.datetoday=datetime.now()
        self.log_way=log_way

    def __call__(self,log="Step log",*args,**kwargs):
        today = datetime.now()
        with open(self.log_way, 'a') as l:
            l.write(f'Log: {log},  Date: {today} \n')
            print(f'Log: {log},  Date: {today} \n')

    # ---------------------------------------------------------------------------------
    # Пример применения метода __call__
    # client=LogControler(log_way='logs.log')
    # client(log="Test")
    # ----------------------------------result of working------------------------------
    # Log result: 
    # >>>Log: Test,  Date: 2022-06-07 17:20:31.986959 

    # print result:
    # >>>Log: Test,  Date: 2022-06-07 17:20:31.986959  
    # ---------------------------------------------------------------------------------





    def create_log_file(self,*args,**kwargs2):
        '''

        :param Nene: Создает файл для ведения логов операясь на параметры вызванного клиента.                                       =>(No input)
        :return: Создает файл в который в дальнейшем будут с которым в дальнейшем будут весть все манимуляции данного клиента       =>(No return)

        '''
        with open (self.log_way,'w',encoding='UTF-8') as l:
            pass

    def custom_w_logs(self,log="Step log",*args,**kwargs):
        '''
        :param log: Логируемая строка                                                                                               =>(String)
        :return: принтует и записывает в лог принимаемую строку, + дата время                                                       =>(No return)
        '''
        today = datetime.now()
        with open(self.log_way, 'a') as l:
            l.write(f'Log: {log},  Date: {today} \n')
            print(f'Log: {log},  Date: {today} \n')


    def delete_old_logs(self,days_del=30,*args,**kwargs):
        '''
        :param days_del: Принимает количество дней (в int формате), от которого будет расчитывать свежесь логов и перезаписывать их =>(int)
        :return: Перезаписывает логи с данными которые подходыт под условия свежести                                                =>(No return)

        '''
        with open(self.log_way, 'r') as l:
            reselt=l.readlines()
        reselt = [line.rstrip() for line in reselt]    
        with open(self.log_way, 'w') as l:
            for log in reselt:
                sp_log=log[-26:]
                sp_log=datetime.strptime(sp_log,'%Y-%m-%d %H:%M:%S.%f')
                if sp_log>=self.datetoday-timedelta(days=days_del):
                    l.write(log)
                    l.write('\n')

    def get_log_result(self,tail=-1,date_from='1990-01-01 00:00:00',date_to='2077-01-01 00:00:00',*args,**kwargs):
        '''
        :param tail: Принимает количество последних логов относительно заданным параметрам                                          =>(int)
        :param date_from: принимает строку с датой от которого будет отталкиватся стрез (может принимать точность среза до секунд)  =>(string)
        :param date_to: принимает строку с датой до которой будет готовиться стрез (может принимать точность среза до секунд)       =>(string)
        :return: Выводит данные по срезу логов и возвращает список логов подходящих по условию                                      =>(list)

        '''

        date_lits_fom=date_from.split(' ')
        date_lits_to=date_to.split(' ')
        try:
            if len(date_lits_fom)==len(date_lits_to):
                if len(date_lits_fom)==2:
                    if len(date_lits_fom[1])==8:
                        date_to=datetime.strptime(date_to,'%Y-%m-%d %H:%M:%S')
                        date_from=datetime.strptime(date_from,'%Y-%m-%d %H:%M:%S')
                    elif len(date_lits_fom[1])==5:
                        date_to=datetime.strptime(date_to,'%Y-%m-%d %H:%M')
                        date_from=datetime.strptime(date_from,'%Y-%m-%d %H:%M')
                    elif len(date_lits_fom[1])==2:
                        date_to=datetime.strptime(date_to,'%Y-%m-%d %H')
                        date_from=datetime.strptime(date_from,'%Y-%m-%d %H')
                else:
                    date_to=datetime.strptime(date_to,'%Y-%m-%d')
                    date_from=datetime.strptime(date_from,'%Y-%m-%d')
        except Exception as err:
            date_from='1990-01-01 00:00:00'
            date_to='2077-01-01 00:00:00'
            date_to=datetime.strptime(date_to,'%Y-%m-%d %H:%M:%S')
            date_from=datetime.strptime(date_from,'%Y-%m-%d %H:%M:%S')
            print("date format isn't support, try again, \nExample: '2077-01-01 00:00:00' or similar\n Err: "+str(err))
        with open(self.log_way, 'r') as l:
            reselt=l.readlines()
        reselt = [line.rstrip() for line in reselt]
        log_req=[]
        for log in reselt:
            sp_log=log[-26:]
            sp_log=datetime.strptime(sp_log,'%Y-%m-%d %H:%M:%S.%f')
            if sp_log>=date_from and sp_log<=date_to:
                log_req.append(log)
                
        if tail==0:
            pass
        elif tail>0:
            tail=tail*(-1)
            log_req=log_req[tail+1:]
        elif tail<0:
            log_req=log_req[tail+1:]
        print(log_req)
        return log_req

    def get_func_work_time(self,function_to_decorate):
        '''
        :Декоратор использующий *args,**kwargs для выведения и логирования время работы функции 
        :param  funcname_name:  принимает строку (Имя функции) для логирования результата                                           =>(String)
        :param printing:  принимает булево значение для вывода Начала и конца работы функции                                        =>(bool)
        :param loging: принимает булево значение для логирования Начала и конца работы функции                                      =>(bool)
        :return: выводит Началo и конeц работы функции и логирует Началo и конeц работы функции                                     =>(No return)

        '''
        def a_wrapper_accepting_arguments(*args,**kwargs):
            time_from=datetime.now()
            printing=True
            loging=False
            function_name='func1'
            result=function_to_decorate(*args,**kwargs)
            
            for i in kwargs.keys():
                if i=="printing":
                    printing=kwargs['printing']
                if i=="loging":
                    loging=kwargs['loging']
                if i=="Loging":
                    function_name=kwargs['funcname_name']
            work_time=(datetime.now()-time_from)
            if printing==True:
                print(work_time)
            if loging==True:
                self.custom_w_logs("function: "+str(function_name)+" work time: "+str(work_time))
            return result
        return a_wrapper_accepting_arguments

    # ---------------------------------------------------------------------------------
    # Пример применения метода get_func_work_time
        
        # client=LogControler(log_way='logs.log')
        # work_time_preset=client.get_func_work_time

        # @work_time_preset
        # def one(n,*args,**kwargs):
        #     l=[x for x in range(n)]
        #     return l

        # l1=one(1000000,funcname_name="fun",printing=False,loging=True)
        # print(l1[:10])

        # ----------------------------------result of working------------------------------
        # Log result: 
            # >>>Log: function: func1 work time: 0:00:00.081781,  Date: 2022-05-30 16:05:02.624069 

        # print result:
            # >>>Log: function: func1 work time: 0:00:00.081781,  Date: 2022-05-30 16:05:02.624069 
        # ---------------------------------------------------------------------------------


    def Start_end_log(self,function_to_decorate):
        '''
        :Декоратор использующий *args,**kwargs для отметки старта и окончания работы функции
        :param  funcname_name:  принимает строку (Имя функции) для логирования результата                                           =>(String)
        :param printing:  принимает булево значение для вывода времени работы функции                                               =>(bool)
        :param loging: принимает булево значение для логирования времени работы функции                                             =>(bool)
        :return: выводит время работы функции и логирует время работы функции                                                       =>(No return)

        '''
        def a_wrapper_accepting_arguments(*args,**kwargs):
            printing=False
            loging=True
            function_name='func1'

            for i in kwargs.keys():
                if i=="printing":
                    printing=kwargs['printing']
                if i=="loging":
                    loging=kwargs['loging']
                if i=="Loging":
                    function_name=kwargs['funcname_name']
            if printing==True:
                print("Start work function: "+function_name)
            if loging==True:
                self.custom_w_logs("Start work function: "+str(function_name))
            
            result=function_to_decorate(*args,**kwargs)

            if printing==True:
                print("End work of function: "+function_name)
            if loging==True:
                self.custom_w_logs("End work of function: "+str(function_name))
            
            return result
        return a_wrapper_accepting_arguments
        # ---------------------------------------------------------------------------------
        # Пример применения метода Start_end_log
        
        # client=LogControler(log_way='logs.log')
        # work_time_preset=client.Start_end_log
        # work_time_preset1=client.get_func_work_time

        # @work_time_preset
        # @work_time_preset1
        
        # def one(n,*args,**kwargs):
        #     l=[x for x in range(n)]
        #     print(l[0:10])
        #     return l

        # l1=one(1000000,funcname_name="fun",printing=False,loging=True)


        # ----------------------------------result of working------------------------------
        # Log result:
            # >>>Log: Start work function: func1,  Date: 2022-05-30 16:05:02.541288 
            # >>>Log: function: func1 work time: 0:00:00.081781,  Date: 2022-05-30 16:05:02.624069 
            # >>>Log: End work of function: func1,  Date: 2022-05-30 16:05:02.626064 

        # print result:
            # >>>Log: Start work function: func1,  Date: 2022-05-30 16:05:02.541288 
            # >>>Log: function: func1 work time: 0:00:00.081781,  Date: 2022-05-30 16:05:02.624069 
            # >>>Log: End work of function: func1,  Date: 2022-05-30 16:05:02.626064 
        # ---------------------------------------------------------------------------------


    def Loadbar(self,iteration, total, prefix='',suffix='',decimals=1,length=100,fill='█',color=cg.Fore.YELLOW):
        '''
        :строка прогресса
        :param  iteration:  принимает номер итерации цикла +1                                                                       =>(Int)
        :param total :  принимает количество итераций                                                                               =>(Int)
        :param prefix: Принимает строку которая будет выводится перед строкой прогресса                                             =>(String)
        :param suffix: Принимает строку которая будет выводится после строки прогресса                                              =>(String)
        :param decimals: целое число которое определяет точность строки прогресса                                                   =>(Int)
        :param length:  Принимает целое число которое определяет длину строки прогресса                                             =>(Int)
        :param fill: Принимает строку которая будет заполнять строку прогресса процессе                                             =>(String)
        :param color: значение параметра которая определяет начальный цвет строки прогресса                                         =>(Colorama.Fore.)
        :return:  Выводит в консоль строку прогресса с результатом общего выполнения цикла или функции                              =>(No return)

        '''
        persent=('{0:.'+str(decimals)+'f}').format(100*(iteration/float(total)))
        filledlenth=int(length*iteration//total)
        bar=fill*filledlenth+'-'*(length-filledlenth)
        print(color+f'\r{prefix} |{bar}| {persent}% {suffix}',end='\r')
        if iteration==total:
            color=cg.Fore.GREEN
            print(color+f'\r{prefix} |{bar}| {persent}% {suffix}',end='\r')
            print(cg.Fore.RESET)

        # ---------------------------------------------------------------------------------
        # Пример применения метода Loadbar

        # client=LogControler(log_way='logs.log')
        # item=list(range(0,50))
        # l=len(item)

        # client.Loadbar
        # import time as t
        # for i, items in enumerate(item,1):
        #     t.sleep(0.3)
        #     client.Loadbar(i+1,l,prefix='Progress',suffix='Complete',length=l)

        # ----------------------------------result of working------------------------------
        # print result:
            # Progress |██████████████████████████████████████████████████| 100.0% Complete
        # ---------------------------------------------------------------------------------



class ClientTGLogs():
    def __init__(self,Bot_token='5197006502:AAFrog4iHOh_4qZSexvCxTYhLYnNCqOIsMM',
                Chat_id=405023882,
                parse_mode='HTML',
                Project_name="Project1",
                File_name="",
                *args,**kwargs):
        
        '''    
        :param Bot_token: Принимает строку с API токеном бота, при игнорировании принимает стандартный токен бота от библиотеки =>(String)
        :param Chat_id: Принимает целое число означающее ID чата                                                                =>(Int)
        :param parse_mode: Принимает строку с типом парсинг мода сообщений бота                                                 =>(String)
        :param Project_name: Принимает строку с названием проекта                                                               =>(String)
        :param File_name: Принимает строку с названием файла, при игнорировании принимает название изначального файла           =>(String)
        :return: Создает клиент для управления Логами в Телеграмм боте                                                          =>(No return)
        '''

        if File_name=="":
            way=sys.argv[0]
            File_name=way.split('\\')[-1]

        self.bot_token=Bot_token
        self.chat_id=int(Chat_id)
        self.Parser_mode=parse_mode
        self.project_name=Project_name
        self.file_name=File_name


    
    def send_log(self,log_text="Test log text",type_log="Standart"):

        '''    
        :param log_text : Принимает строку с текстом лога                                                                       =>(String)
        :param type_log: Принимает значение (Standart/Custom) которое обозначает формат логов                                   =>(String)
        :return: Отправляет сообщение с логом в Телеграмм чат                                                                   =>(No return)
        '''
        today = datetime.now()
        log_text=str(log_text)
        bot=tb.TeleBot(self.bot_token)
        if type_log=="Standart":
            bot.send_message(self.chat_id,f"Project name: {self.project_name}, file_name: {self.file_name}, Log: {log_text}, Date: {str(today)}",parse_mode=self.Parser_mode)
        elif type_log=="Custom":
            bot.send_message(self.chat_id,f"{log_text}, Date: {str(today)}",parse_mode=self.Parser_mode)    


        # ---------------------------------------------------------------------------------
        # Пример применения метода send_log
        # import traceback
        # tellog=ClientTGLogs()
        # try:
        #     lst=[1,2]
        #     for i,b in lst:
        #         print(i)
        # except Exception as e:

        #     bag=traceback.format_exc()
        #     bag_line=bag.split(',')[1][1:]    
        #     tellog.send_log(bag_line,type_log="Standart")
        # ----------------------------------result of working------------------------------
        # bot message: result:

        # BDLogsbot >>> "Project name: Project 1, file_name: ipykernel_launcher.py, Log: line 37"
        # ---------------------------------------------------------------------------------

        # Хорошая задумка реализовать функцию Help
        # def __help__(self,*func_name):
        #     func_name=func_name[0].__name__
        #     if "send_log" in func_name:
        #         print(self.send_log.Explanation)
    

    












"""
squidward is first alfa tester of my log library
don't offend squidward and it's so hard work to look at my crooked code

░░░░░▄▄▀██▀▀▀▄▄
░░▄██░░▄░░▀░▀░░▀▄
░█▀░░▀░░░░░░░░░░█
█▀░░░░▄▄▄░░░░░░░█
█▀░▄█████▄░░░░░▄▀░▄▄▄░░░░░░░░░░░░▄▄▀▀▀▀▄
▀▄░▀█▀▀▄▄░█▄▄█▀▀██▄▄▄▀░░░░░░░░▄▀▀░░▄▄██▀
░░▀▄██▄▀██▀░░░▄███▀▀░░░░░░░▄▀▀░░▄▄█▀▀▀
░░░░░██▀░░▄▄█▀█▄░█░░░░░▄▄▄▀░░▄█▀
░░░▄▀░░░▄▀▀███████████████▀▀▀
░░░█░░▄██░░░▀████████████
░░░█░████░░░░░██████████▀
░░░█▄█████░░░░░█████▀▀
░░░▀███████▄▄▄██████
░░░░░▀░█████████████
░░░░░░▄█████████████▄
░░░░░░██▀▀▀▀▀▀▀▀▀▀▀██
░░░░░░█░░░░░░░░░░░░░█
"""

