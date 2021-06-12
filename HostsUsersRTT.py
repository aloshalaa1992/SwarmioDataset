"""
This code is a test for callculating the RTT from the pings.

"""
import os
import re
import numpy as np


class HostsUsersRTT:
    
    """
    Initiallizing the object's members
        host        -- holding the ip of the host to be connected to 
        pings       -- holds the number of pings to calculate the RTT for
        RTT         -- holds the RTT between the current running machine and the host
        description -- description field
        lastseen    -- lastseen field
        modified    -- modified field
        published   -- published field
    """
    def __init__(self):

        #hosts and users
        self.hosts = json.load( open( "datacenters.json" ) )
        self.users = json.load( open( "user_id_ip.json" ) )

        #number of pings per host
        self.pings = 8

        #dictionary that holds the RTT table
        self.RTT = {}  #keys are hosts: values are the users and their averaged rtt
    
    """
    A function to return a read-friendly version of the object

        returns string of the members of the objects
    """
    def __str__(self):
        lines = ["Hosts: {}".format(self.hosts),
                "Users: {}".format(self.users),
                 "Number of Pings: {}".format(self.pings),
                 "RTT: {}".format(self.RTT),

                 "Description: {}".format(self.description),
                 "Lastseen: {}".format(self.lastseen),
                 "Modified: {}".format(self.modified),
                 "Published: {}".format(self.published)]
        return "\n".join(lines)


    """
    A function to make multiple pings and average
        the time needed for the icmp packets to come back
        in order to estimate the RTT of the host

    """
    def make_RTT(self):
        response =os.popen("ping -c "  + self.pings + " " + self.host).read()
        data = re.findall(r'time=(\S*)', response)
        data = list(map(float, data))

        if data:
            Rtt = np.mean(data) / 1000
            self.RTT = Rtt
            return Rtt

        else:
            self.RTT = -1 
            return -1
"""
Main function to test the class

"""


if __name__ == "__main__":
    from pssh.clients.miko import ParallelSSHClient
    server = "38.65.239.23"
    username = "ubuntu"
    password = "vHCkyDEp43UYuHNu"
    hosts = [server, '52.91.193.170']
    client = ParallelSSHClient(hosts, user=username, password=password)
    output = client.run_command('uname', sudo=True)
    print(output)