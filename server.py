'''
Created on 7 mai 2014

@author: victor-clevo
'''
import SocketServer, logging, os.path, robot

class Server(SocketServer.TCPServer):
    def __init__(self, server_address, handlerClass):
        SocketServer.TCPServer.allow_reuse_address = True
        try :
            SocketServer.TCPServer.__init__(self, server_address, handlerClass)
        except IOError as details:
            logging.error('socket.error : {}'.format(details))
        try :
            self.rebound = robot.Robot(self)
            logging.info('RPi library detected')
        except ImportError:
            logging.info('Robot : simulated')
            self.rebound = robot.BaseRobot(self)  # simulated robot (debug)


class Handler(SocketServer.BaseRequestHandler):
    # Instantiated once per connection        
    def handle(self):
        logging.info('Socket : {} is connected'.format(self.client_address))
        while True:
            self.server.rebound.task = self.request.recv(256).strip()
            if not self.server.order: break
            logging.info('Socket : Order is ##%s##' % self.server.order)
            self.server.rebound.execute()
        self.request.close()
        logging.info('Socket : {} is disconnected'.format(self.client_address))
        self.server.rebound.task = 'stop'  # arret du robot si la connexion est rompue
        self.server.rebound.execute()
