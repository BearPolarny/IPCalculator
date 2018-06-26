import numpy as np
from IPCalcExceptions import InvalidIPException, InvalidMaskException


class IPCalc:

    __viable_octets = [255, 254, 252, 248, 240, 224, 192, 128, 0]

    def __init__(self, ip, mask):
        """
        :param ip: Address IP in '0.0.0.0' format
        :param mask: IP mask in '0.0.0.0' or 'n' format
        """
        self.ip, self.mask = self.__read_ip__(ip, mask)
        self.network, self.broadcast = self.__calculate_ip_borders__()
        self.min_Host, self.max_Host = self.__calculate_border_hosts__()
        self.hosts = self.__calculate_available_hosts__()

    @staticmethod
    def __negate_mask__(mask):
        for i in range(4):
            mask[i] = 255 - mask[i]
        return mask

    def __calculate_ip_borders__(self):
        net = []
        for oct_ip, oct_mask in zip(self.ip, self.mask):
            net.append(oct_ip & oct_mask)

        mask = self.__negate_mask__(self.mask)

        bro = []
        for oct_ip, oct_mask in zip(self.ip, mask):
            bro.append(oct_ip | oct_mask)

        return net, bro

    def __calculate_border_hosts__(self):
        network = self.network.copy()
        broadcast = self.broadcast.copy()

        network[3] += 1
        broadcast[3] -= 1

        return network, broadcast

    def __calculate_available_hosts__(self):

        available_hosts = 1

        for oct_min, oct_max in zip(self.network, self.broadcast):
            available_hosts *= (oct_max - oct_min + 1)

        available_hosts -= 2

        return available_hosts

    @staticmethod
    def __calc_mask__(num):

        mask = ''

        for i in range(num):
            mask += '1'

        while len(mask) != 32:
            mask += '0'

        mask_d = []

        for i in range(4):
            mask_d.append(mask[i*8:(i+1)*8])

        mask = []

        for octet in mask_d:
            mask.append(int(octet, 2))

        return np.array(mask)

    def __read_ip__(self, ip, mask):
        ip = np.array(ip.split('.')).astype(int)
        for octet in ip:
            if octet > 255 or octet < 0:
                raise InvalidIPException
        if len(mask) < 4:
            mask = int(mask)
            if mask < 1 or mask > 30:
                raise InvalidMaskException
            mask = self.__calc_mask__(int(mask))
        else:
            mask = np.array(mask.split('.')).astype(int)
            for octet in mask:
                if octet not in self.__viable_octets:
                    raise InvalidMaskException

        return ip, mask

    def __str__(self):
        string = 'Network: '    + str(self.network)     + '\n' + \
                 'Broadcast: '  + str(self.broadcast)   + '\n' + \
                 'Min Host: '   + str(self.min_Host)    + '\n' + \
                 'Max Host: '   + str(self.max_Host)    + '\n' + \
                 'Hosts: '      + str(self.hosts)       + '\n'

        return string
