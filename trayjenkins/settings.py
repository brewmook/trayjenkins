from optparse import OptionParser


class Settings(object):

    def __init__(self, host, username='', password=''):

        self.host = host
        self.username = username
        self.password = password

    def __eq__(self, other):

        return other is not None \
           and self.host == other.host \
           and self.username == other.username \
           and self.password == other.password

    def __repr__(self):

        return "Settings(host='%s',username='%s',password='%s')" % (
               self.host,
               self.username,
               self.password)


class CommandLineSettingsParser(object):

    def __init__(self):

        self._parser = OptionParser(usage='usage: %prog [options] host')
        self._parser.add_option('-p', '--password',
                                dest='password',
                                default='',
                                help='password for remote host')
        self._parser.add_option('-u', '--username',
                                dest='username',
                                default='',
                                help='username for remote host')

    def parse_args(self, args):

        (options, args) = self._parser.parse_args(args)  # @UnusedVariable

        if len(args) is 1:
            result = Settings(args[0])
            result.username = options.username
            result.password = options.password
        else:
            result = None

        return result

    def print_help(self):

        self._parser.print_help()
