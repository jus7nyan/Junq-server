#from . import m_types
from socket import socket
from . import types
from .types import const
from . import user_types


import wave
import pyaudio

class MH:
    def __init__(self) -> None:
        self.const = const()
        
        self.sn = {}
        self.users = {}
        self.rooms = {"start":[]}
        self.snd = {}
    def handle(self, msg, server, version):
        if msg.mtype == self.const._LM_:
            client = msg.client
            nick = msg.fnick
            rsa_key = msg.req[:-1]

            print(nick, rsa_key)

            if nick not in self.users and str(msg.client) not in self.sn:
                user = user_types.User(nick, client, "logined", pub_key=rsa_key)
                
                if str(client) not in self.sn:
                    self.sn.update({str(client):{"nick":[], "rsa_key":[]}})
                    self.sn[str(client)]["nick"] = [nick]
                    self.sn[str(client)]["rsa_key"] = [rsa_key]
                else:
                    if nick not in self.sn[str(client)]:
                        self.sn[str(client)]["nick"].append(nick)
                        self.sn[str(client)]["rsa_key"].append(rsa_key)

                self.users.update({nick:user})
                self.rooms["start"].append(user)
            else:
                err = types.EM(server=server, from_=version, req="This nick is already logined")
                msg.from_.send(err.request())


        elif msg.mtype == self.const._KGM_:
            nick = msg.req

            if nick in self.users.keys():
                soc = self.users[nick].socket
                nicks = self.sn[str(soc)]["nick"]
                rsa = None
                for i in range(len(nicks)):
                    if nick == nicks[i]:
                        rsa = self.sn[str(soc)]["rsa_key"][i]
                        print(rsa)
                        break
                
                req = types.RTRM(server=server, from_=version, req=rsa)
                msg.from_.send(req.request())
            
            else:
                war = types.WRM(server=server, from_=version, req="This user is not logined")
                msg.from_.send(war.request())



        elif msg.mtype == self.const._PM_:
            to_nick = msg.to
            from_nick = msg.fnick
            client = msg.client

            if from_nick not in self.users.keys():
                from_nick = "ANONIM"
                msg.fnick = from_nick
                wrm = types.WRM(server=server, from_=version, req="Your nick not in db. message will be sent from ANONIM")
                client.send(wrm.request())

            if to_nick in self.users.keys():
                to_user = self.users[to_nick]
                to_socket = to_user.socket

                to_socket.send(msg.request())
                
                suc = types.SM(server=server, from_=version, req="Message sent successfully")
                client.send(suc.request())

            else:
                em = types.EM(server=server, from_=version, req="This user is not logined")
                client.send(em.request())
                
        elif msg.mtype == self.const._PSM_:
            if str(msg.client) not in self.snd.keys():
                print("mus user added")
                self.snd.update({str(msg.client):{"fnick":msg.fnick,"snd":[]}})
            else:
                print("mus user deleted")
                self.snd.pop(str(msg.client))
                FORMAT = pyaudio.paInt16
                CHANNELS = 1
                RATE = 44100

                with wave.open('output.wav', 'wb') as wf:
                    p = pyaudio.PyAudio()
                    wf.setnchannels(CHANNELS)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(RATE)
                    print("good")

                for i in self.snd[str(msg.client)]["snd"]:
                    print(i)
                    wf.writeframes(i)
                    
        elif msg.mtype == self.const._SNM_:
            if str(msg.client) in self.snd.keys():
                self.snd[str(msg.client)]["snd"].append(msg.req)
    
    def unregister(self, socket):
        try:
            nick = self.sn[str(socket)]["nick"]
            self.sn.pop(str(socket))
            for n in nick:
                self.users.pop(n)
            print("socket",socket.getpeername(),"unregistered")
        except:
            print("socket",socket.getpeername(),"unregistered")
