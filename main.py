'''
Created on 7 mai 2014

@author: victor-clevo
'''

# This is the main function that must be executed in order to get the server working
# main.py needs to be in the same directory as server.py, observer.py, daemon.py and robot.py

from daemon import Daemon
import logging, sys, server

# parameters:
log_path = '/var/log/rebound/light_server.log'  # make sure this file exists
pidfile_daemon = '/tmp/lightrebound_daemon.pid'
host = '0.0.0.0'  # '0.0.0.0' means listening on every IP address
channel = 233
rpi = False


# All the info will be writen in the same log, even when info comes from other scripts
logging.basicConfig(filename=log_path, format='%(asctime)s %(message)s', level=logging.INFO)

class DaemonScript(Daemon):
    def __init__(self, pidfile_daemon, host, channel):
        self.host = host
        self.channel = channel
        super(DaemonScript, self).__init__(pidfile_daemon)

    def run(self):
        self.sServer = server.Server((self.host, self.channel), server.Handler)
        logging.info('Server : Ready to serve on {}'.format(self.sServer.server_address))
        print 'something came up'
        self.sServer.serve_forever()
        # apparently after this function is being called, the self.sServer pointer is lost. It might be possible to write theDaemon as an argument of sServer.
        logging.error('Server : Abnormal end of the SocketServer, daemon still running')

    def stop(self):
        try:
            self.sServer.server_close()
        except AttributeError as details:
            logging.error(details)
        super(DaemonScript, self).stop()


if __name__ == "__main__":
    print 'log can be found at ' + log_path
    theDaemon = DaemonScript(pidfile_daemon, host, channel)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            logging.info("Daemon : Asked to start")
            theDaemon.start()
        elif 'stop' == sys.argv[1]:
            logging.info("Daemon : Asked to stop")
            theDaemon.stop()
        elif 'restart' == sys.argv[1]:
            logging.info("Daemon : Asked to restart")
            theDaemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
