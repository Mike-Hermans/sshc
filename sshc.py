import sys
import re

from lib.config import Config

class SSHC:
    commands = [
    'help',     # Lists all commands
    'list',     # Lists all hosts
    'get',      # Get a single host
    'add',      # Add a new host
    'remove',   # Remove a host
    'sort',     # Sort the config file alphabetically 
    'update'    # Add or remove an option for a host
    ]
    command = 'list' # Default command
    args = False
    config = None
    debug = False

    def __init__(self):
        self.config = Config()
        self.get_args()
        self.execute()

    def get_args(self):
        # Check if there is more than 1 argument
        if len(sys.argv) < 2:
            return

        # Set command to second argument
        self.command = sys.argv[1]

        # Set all other arguments as self.args
        if len(sys.argv) > 2:
            self.args = sys.argv[2:]

    # Calls the function that belongs to the command
    def execute(self):
        if self.command in self.commands:
            if self.debug:
                getattr(self, "c_%s" % self.command)()
                return

            try:
                getattr(self, "c_%s" % self.command)()
            except Exception as error:
                print("Error executing command")
            return
        print("Command '%s' not found" % self.command)

    # Check if host entry exists, if not, exit
    def require_host(self, host):
        if not self.config.get_host(host):
            print("Host %s does not exist" % host)
            sys.exit(1)

    # Count if there are enough arguments
    def min_args(self, args):
        if not self.args or len(self.args) < len(args):
            print("Need %s arguments (%s)" % (len(args), ', '.join(args)))
            sys.exit(1)

    # Show a list of commands
    def c_help(self):
        print("Commands:")
        print("help             | Prints this list")
        print("list             | Lists all hosts")
        print("get <host>       | Returns information for chosen host")
        print("remove <host>    | Removes a host")
        print("sort             | Sorts the host file alphabetically")
        print("add <host> <user>@<hostname>[:port] [id_rsa key] | Adds a new host")
        print("update <host> <parameter> <value> | Adds a parameter to a host, removes it if value is unset")

    # List currently saved hosts
    def c_list(self):
        for config in self.config.read():
            # Print the first part at least 15 characters wide
            if config.get('Host'):
                line = '%-15s' % config['Host']

            if config.get('HostName') and config.get('User'):
                line += " [ %s@%s ]" % (config['User'], config['HostName'])

            if config.get('Port'):
                line += ":%s" % config['Port']

            if config.get('IdentityFile'):
                line += " (key: %s)" % config['IdentityFile']
            print(line)

    # Get more details about a specific host
    def c_get(self):
        self.min_args(['host'])

        config = self.config.get_host(self.args[0])
        if not config:
            print("Host '%s' not found." % self.args[0])
            sys.exit(1)

        for line in config:
            print(line + ": " + config[line])

    # Add a new entry to the config file
    def c_add(self):
        self.min_args(['host', 'user@server'])
        host = self.args[0]

        if self.config.get_host(host):
            print("Host %s already exists" % host)
            sys.exit(1)

        user_host = self.args[1]

        # Match it for [user]@[server]
        match = re.search(r'(.+)@(.+)', user_host)
        if not match:
            print("Invalid user@host")
            sys.exit(1)

        user = match.group(1)
        server = match.group(2).split(':')

        new_host = {
            'Host': host,
            'HostName': server[0],
            'User': user
        }

        if len(server) > 1:
            new_host['Port'] = server[1]

        if len(self.args) > 2:
            new_host['IdentityFile'] = '~/.ssh/%s' % self.args[2]

        self.config.add_host(new_host)

        self.config.save()
        print("%s has been added to the config file" % host)

    # Remove an entry from the config file
    def c_remove(self):
        self.min_args(['host'])
        host = self.args[0]
        self.require_host(host)

        self.config.remove_host(host)
        self.config.save()
        print("%s removed from config file" % host)

    # Update parameters for a host entry
    def c_update(self):
        self.min_args(['host', 'parameter', 'value'])
        host = self.args[0]
        self.require_host(host)

        valid_parameters = [
            'Host',
            'HostName',
            'User',
            'IdentityFile',
            'Port'
        ]

        parameter = self.args[1].capitalize()
        value = False

        if parameter not in valid_parameters:
            print("Parameter '%s' is not valid, valid parameters are: " % parameter)
            print(', '.join(valid_parameters))
            sys.exit(1)

        if self.args[2] != 'unset':
            value = self.args[2]

        self.config.update_host(host, parameter, value)
        self.config.save()
        if value == 'unset':
            print('%s: %s has been removed' % (host, parameter))
        else:
            print('%s: %s has been set to %s' % (host, parameter, value))

    # Sort the entries in the config file
    def c_sort(self):
        self.config.sort_config()
        self.config.save()
        print("Config file sorted!")
