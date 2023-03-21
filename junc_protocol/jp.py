import socket
import selectors

from . import types
#from . import m_types

from . import mh


# Протокол получения отправки и обработки сообщений


class JP:
    def __init__(self, port, msize) -> None:
        self.const = types.const()
        self.version = "server version 0.1"
        
        self.port = port                                            # Порт серверного сокета
        self.msize = msize                                          # Максимальный размер сообщения
        
        self.selector = selectors.DefaultSelector()                 # Селектор (по факту для асинхронности)

        self.mh = mh.MH()

        self.server_socet = socket.socket()
        self.server_socet.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.server_socet.bind(("",self.port))
        self.server_socet.listen()

        ##########################################################################################
        # Регистрация действий при доступе для чтения серверного сокета                          #
        # если для чтения доступен серверный сокет то нужно принять соединение                   #
        # срабатывает ОДИН раз для нового подключения                                            #
        # каждое новое подключение вызывает метод accept_connect                                 #
        # передается СЕРВЕРНЫЙ сокет как аргумент                                                #
        self.selector.register(self.server_socet, selectors.EVENT_READ, data=self.accept_connect)

    def accept_connect(self, server_socet):
        client_socket, addr = server_socet.accept()                # Разрешение подключение клиентского сокета
        print(f"{addr} connected!")
        # msg = m_types.NS_Message("server", addr)
        msg = types.NS(server=server_socet, from_=self.version)
        
        client_socket.send(msg.request())

        
        
        ##########################################################################################
        # Регистрация действий при доступе для чтения клиентского сокета                         #
        # если для чтения доступен клиентский сокет то нужно принять сообщение                   #
        # срабатывает при КАЖДОМ сообщении от клиента                                            #
        # каждое новое сообщение вызывает метод get_message                                      #
        # передается КЛИЕНТСКИЙ сокет как аргумент                                               #
        self.selector.register(client_socket, selectors.EVENT_READ, data=self.get_message)
    
    def get_message(self, client_socket):

        request = client_socket.recv(self.msize)
        if request:
            try:
                request = request.decode()
                try:
                    to_, type_, nick, req_ = request.split("<~$")


                    if type_ == str(self.const._LM_):
                        msg = types.LM(client=client_socket, to=to_, fnick=nick, req=req_)
                        
                    elif type_ == str(self.const._KGM_):
                        msg = types.KGM(client=client_socket, to=to_, req=req_)
                    
                    elif type_ == str(self.const._PM_):
                        msg = types.PM(client=client_socket, to=to_, fnick=nick, req=req_)
                    
                    # elif type_ == str(self.const._PSM_):
                    #     msg = types.PSM(client=client_socket, to=to_, fnick=nick)
                    
                    else:
                        msg = None
                    
                    self.mh.handle(msg, self.server_socet, self.version)
                    


                except:
                    msg = types.EM(server=self.server_socet, from_=self.version, req="Bad message syntax")
                    client_socket.send(msg.request())

                    print("wrong request syntax from", client_socket.getpeername(), request)

            except:
                pass
                # print("mus")
                # msg = types.SNM(client=client_socket, req=request)
                # self.mh.handle(msg, self.server_socet, self.version)


        else: # отсутствие request говорит о том что клиент закрыл соединение и надо убрать его из всех обработчиков
            self.selector.unregister(client_socket)
            self.mh.unregister(client_socket)
            print(client_socket.getpeername(),"close")
            client_socket.close()

            
    
    def main_loop(self):
        while True:
            events = self.selector.select()
            
            for key, _ in events:
                callback = key.data
                callback(key.fileobj)
