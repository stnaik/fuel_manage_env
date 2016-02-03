import yaml
import os
import netifaces
import uuid
import sys

load_f = 'netifnames.yaml'
save_f = 'netifnames.yaml'
# schema save method
# schema='e_name'
schema = 'e_name'
lab= 'lab5'

"""
#export nodes=$(fuel node list|awk {'print $9'} | grep -E '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' )
#export nodes=$(fuel node list|awk {'print $10'} | grep -E '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' )
# awk skip some ips o_O should be investigated!
export nodes=$(fuel node list |grep -E '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' | cut -d\| -f5)
export qm='-q -o "StrictHostKeyChecking no" '
for i in ${nodes} ; do scp ${qm} netifnames.yaml dump_iface.py $i:/root/ ; ssh ${qm} $i python /root/dump_iface.py ; scp  ${qm} $i:/root/netifnames.yaml . ; done

"""
example_hw_list = {
    'hostname_{random}': {
        'nics': {'mac1': {'e_name': 'eth0', 'b_name': 'p1p1'},
                 'mac2': {'e_name': 'eth1', 'b_name': 'p1p2'}}},
    'hostname_{random2}': {
        'nics': {'mac1': {'e_name': 'eth0', 'b_name': 'p1p1'},
                 'mac2': {'e_name': 'eth1', 'b_name': 'p1p2'}}}
}


def is_physical(iface):
    """Returns true if virtual is not in the iface's linked path."""
    # A virtual interface has a symlink in /sys/class/net pointing to
    # a subdirectory of /sys/devices/virtual
    # $ cd /sys/class/net
    # $ readlink lo
    # ../../devices/virtual/net/lo
    # $ readlink enp2s0f0
    # ../../devices/pci0000:00/0000:00:1c.0/0000:02:00.0/net/enp2s0f0
    return 'virtual' not in \
        os.path.realpath('/sys/class/net/{0}'.format(iface))


def get_physical_ifaces():
    """Returns a sorted list of physical interfaces."""
    ifaces = netifaces.interfaces()
    phys = sorted(filter(is_physical, ifaces))
    dict1 = {}
    for nic in phys:
        n_mac = netifaces.ifaddresses(nic)[netifaces.AF_LINK]
        dict1[n_mac[0]['addr']] = nic
    return dict1


def check_if_exist(ifs, hw_dict):
    """
    Check if mac in host['nics']
    Will stop on first founded
    :param ifs:
    :param hw_dict:
    :return:
    """
    for hw in hw_dict:
        for nic in hw_dict[hw]['nics']:
            if nic in ifs.keys():
                print 'INFO: {2} {0} from node {1}'.format(
                    nic, hw, ifs[nic])
                print 'INFO: OLD data:{0}'.format(
                    hw_dict[hw]['nics'][nic])
                return hw
    return None


def get_nics_dict(ifs, nics=None):
    """ return dict with new schema

    :param ifs:
    :return:
    """
    if nics is None:
        nics = {}
    for nic in ifs.keys():
        nics.setdefault(nic, {schema: None})
        nics[nic].update({schema: ifs[nic]})
    return nics


if __name__ == '__main__':
    # remove anchors from dump
    na_d = yaml.dumper.SafeDumper
    na_d.ignore_aliases = lambda self, data: True
    ###################################
    if os.path.isfile(load_f):
        with open(load_f, 'r') as f1:
            i_yaml = yaml.load(f1)
    else:
        i_yaml = {}
    hw_dict = i_yaml.get('hw_server_list', {})
    ifs = get_physical_ifaces()

    check_hw = check_if_exist(ifs, hw_dict)

    if check_hw is None:
        print 'INFO: adding new-one hw'
        new_hw_uuid = 'new_hw_{0}'.format(str(uuid.uuid4()))
        hw_dict[new_hw_uuid] = {'nics': get_nics_dict(ifs), 'lab' : lab}
        print 'INFO: New: {0}'.format(hw_dict[new_hw_uuid])
    else:
        print 'INFO: update'
        hw_dict[check_hw]['nics'] = get_nics_dict(ifs,
                                                   hw_dict[check_hw]['nics'])
        hw_dict[check_hw]['lab'] = lab

    # save magic
    i_yaml['hw_server_list'] = hw_dict
    with open(save_f, 'w') as f2:
        f2.write(yaml.dump(i_yaml, default_flow_style=False, Dumper=na_d))



