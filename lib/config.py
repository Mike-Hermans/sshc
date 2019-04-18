import os
import sys

class Config:
    config = False
    path = os.path.expanduser('~/.ssh/')

    def __init__(self):
        self.config = self.get_config_file()

    # Converts the config file into an easy to work with array
    def get_config_file(self):
        try:
            config = open(self.path + 'config')
        except:
            print "Could not open %sconfig file" % self.path
            sys.exit(1)
        hosts = []
        host = {}
        for line in config.read().splitlines():
            # If line is empty, create new host
            if not line:
                hosts.append(host)
                host = {}
                continue

            value = line.split()
            host[value[0]] = value[1]
        config.close()
        return hosts

    # Returns the config
    def read(self):
        return self.config

    # Returns a single host
    def get_host(self, host):
        for config in self.config:
            if config['Host'] == host:
                return config
        return False

    # Adds a host to the array
    def add_host(self, host):
        self.config.append(host)

    # Removes the host from the array
    def remove_host(self, host):
        for config in self.config:
            if config['Host'] == host:
                self.config.remove(config)

    # Update or add an value to Host
    def update_host(self, host, parameter, value):
        for config in self.config:
            if config['Host'] == host:
                # If value is False, unset the key
                if value is False:
                    del config[parameter]
                    return
                if parameter == 'IdentityFile':
                    value = '~/.ssh/' + value
                config[parameter] = value

    # Reorder config file alphabetically based on Host
    def sort_config(self):
        self.config = sorted(self.config, key=lambda k: k['Host'])

    # Saves the array to the file
    def save(self):
        with open(self.path + 'config', 'w') as config_file:
            for host in self.config:
                config_file.write("Host %s\n" % host.pop('Host', None))
                for value in host:
                    config_file.write("%s %s\n" % (value, host[value]))

                # When a dict or 'block' is finished, add an extra newline
                config_file.write("\n")