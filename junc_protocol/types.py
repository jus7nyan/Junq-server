import re

class const:
    def __init__(self) -> None:
        self._LM_      = 1      # Login Message
        self._PM_      = 2      # Private Message
        self._KGM_     = 3      # Key Get Message (rsa key)
        self._PSM_     = 4      # P sound message помогает понять к какому пользователю привязывать голосовое
        self._SNM_     = 5      # Sound Message

        self._NS_      = -1     # New session Message
        self._EM_      = -2     # Error Message
        self._WRM_     = -3     # Warrning Message
        self._RTRM_    = -4     # Response to a request (aka ответ на запрос)
        self._SM_      = -5     # Success message



class client_message:
    # сообщение от клиента (насследуемый класс)
    def __init__(self, client, to) -> None:
        self.const = const()

        self.to = to
        self.client = client

        self.req = ""
        self.fnick = ""
        self.mtype = None

    def request(self):
        msg = "{}<~${}<~${}<~${}".format(self.to, self.mtype, self.fnick, self.req).encode()
        
        return msg

class LM(client_message):
    # Сообщение авторизации
    # в req (по идее) должен быть rsa ключ
    def __init__(self, client, to, fnick, req) -> None:
        super().__init__(client, to)

        self.mtype = self.const._LM_
        
        self.req = req        # rsa
        self.fnick = fnick    # nick

class PM(client_message):
    # личное сообщение
    # в to должен быть ник другого клиента
    # может быть отправленно анонимно но выскочит предумпреждающее сообщение
    def __init__(self, client, to, fnick, req) -> None:
        super().__init__(client, to)

        self.mtype = self.const._PM_

        self.req = req       # client message text
        self.fnick = fnick   # client nick

class KGM(client_message):
    # сообщение о запросе rsa ключа клиента
    def __init__(self, client, to, req) -> None:
        super().__init__(client, to)

        self.mtype = self.const._KGM_
        
        self.req = req
################################################################################################
## Special messages


# class PSM(client_message):
#     def __init__(self, client, to, fnick) -> None:
#         super().__init__(client, to)

#         self.mtype = self.const._PSM_
        
#         self.fnick = fnick

# class SNM():
#     def __init__(self, client, req) -> None:
        
#         self.client = client
#         self.mtype = const()._SNM_

#         self.req = req



#################################################################################################



class server_message:
    # Сообщение от сервера (насследуемый класс)
    def __init__(self, server, from_) -> None:
        self.const = const()

        self.server = server
        self.from_ = from_                          # maybe version of server ???
        self.client = None

        self.mtype = None
        self.req = ""


    def request(self):
        msg = "{}<~${}<~${}".format(self.from_, self.mtype, self.req).encode()
        return msg


class NS(server_message):
    # сообщение о новой сессии
    # отправляется при подключении пользователя к скрверу
    def __init__(self, server, from_) -> None:
        super().__init__(server, from_)

        self.mtype = self.const._NS_


class EM(server_message):
    # сообщение об ошибке
    def __init__(self, server, from_, req) -> None:
        super().__init__(server, from_)

        self.mtype = self.const._EM_

        self.req = req

class WRM(server_message):
    # пердупреждающее сообщение
    def __init__(self, server, from_, req) -> None:
        super().__init__(server, from_)

        self.mtype = self.const._WRM_

        self.req = req


class RTRM(server_message):
    # Ответ на запрс
    # например на запрос rsa ключа пользователя
    def __init__(self, server, from_, req) -> None:
        super().__init__(server, from_)

        self.mtype = self.const._RTRM_

        self.req = req

class SM(server_message):
    # Сообщение об успешной операции
    def __init__(self, server, from_, req) -> None:
        super().__init__(server, from_)

        self.mtype = self.const._SM_

        self.req = req