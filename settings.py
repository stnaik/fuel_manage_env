import os

OPENSTACK_RELEASE_UBUNTU = 'ubuntu'

# Default 'KEYSTONE_PASSWORD' can be changed for keystone on Fuel master node
KEYSTONE_CREDS = {'username': os.environ.get('KEYSTONE_USERNAME', 'admin'),
                  'password': os.environ.get('KEYSTONE_PASSWORD', 'admin'),
                  'tenant_name': os.environ.get('KEYSTONE_TENANT', 'admin')}
OPENSTACK_RELEASE = os.environ.get(
    'OPENSTACK_RELEASE', OPENSTACK_RELEASE_UBUNTU).lower()




# Input params:
CLUSTER_CONFIG = os.environ.get("CLUSTER_CONFIG", "test_lab.yaml")

# optional
START_DEPLOYMENT = os.environ.get("START_DEPLOYMENT", "false")
# UPLOAD_DEPLOYMENT_INFO = os.environ.get("UPLOAD_DEPLOYMENT_INFO", "false")
IPMI_CONFIGS = os.environ.get("IPMI_CONFIGS", "ipmi/netifnames.yaml")
