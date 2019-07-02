import os
import re
import configparser


class Enclosure:
    def __init__(self):
        pass

    def bay_mapping(self, enc_sas):
        # map the bay with the block devices
        bays = {}
        for file_name in os.listdir('/sys/class/enclosure/' + enc_sas):
            if 'DriveBay' in file_name:
                block = os.listdir('/sys/class/enclosure/' + enc_sas + '/' +
                                   file_name + '/device/block/')[0]
                bay = int(re.match(r'.*DriveBay(\d+).*', file_name).group(1))
                bays[bay] = [block]
        return bays

    def get_enclosures(self):
        enclosures = {}
        for enc_sas in os.listdir('/sys/class/enclosure/'):
            if '{"Name":"DriveBay1"}' in os.listdir('/sys/class/enclosure/' +
                                                    enc_sas):
                # Valid HPE naming scheme of an enclosure
                with open('/sys/class/enclosure/' + enc_sas + '/id',
                          'r') as enc_id_f:
                    enc_id = enc_id_f.read().strip()
                    if enclosures.get(enc_id) is None:
                        # new detected enclosure
                        enclosures[enc_id] = {}
                        enclosures[enc_id]['sas_id'] = [enc_sas]
                        enclosures[enc_id]['bays'] = self.bay_mapping(enc_sas)
                    else:
                        # new path to the same devices
                        enclosures[enc_id]['sas_id'].append(enc_sas)
                        mapping = self.bay_mapping(enc_sas)
                        # merge the list of each key to have multiple blocks
                        for bay in mapping.keys():
                            enclosures[enc_id]['bays'][bay].append(
                                mapping[bay][0])
        return enclosures

    def jbod_bay(self, block):
        enclosures = self.get_enclosures()
        for enc in enclosures.keys():
            for bay in enclosures[enc]['bays']:
                if block in enclosures[enc]['bays'][bay]:
                    return (enc, bay)

    def jbod_alias(self, enc, alias_path):
        config = configparser.ConfigParser()
        config.read(alias_path)
        return config.get('alias', enc, fallback='undefined_alias')

    def jbod_multipath_bay(self, dm):
        # check the slaves in the mpath device
        slave = os.listdir('/sys/block/' + dm + '/slaves')[0]
        return self.jbod_bay(slave)
