.. _readme:

Manage_env.py
~~~~~~~~~~~~~

Simple script, to perform pining HW node to different network and env schema.
Useful for auto-deployment on real hardware.

Modules for run:
~~~~~~~~~~~~~~~~

#. fuel-qa_
#. fuel-devops_

.. _fuel-qa: https://github.com/openstack/fuel-qa
.. _fuel-devops: https://github.com/openstack/fuel-devops

Strict lab config:
~~~~~~~~~~~~~~~~~~
File: strict_lab_config.yaml

.. code-block:: yaml

    assign_method: "hw_pin"
    nodes:                                                                          
      cz0001.com:                                                                   
        l3_ifaces:                                                                  
          phys_nic_map: *default_compute_phys                                       
          virt_nic_map: *default_compute_virt                                       
        roles:                                                                      
          - compute                                                                                               
      cz0005.com:                                                                   
        l3_ifaces:                                                                  
          phys_nic_map: *default_controller_phys                                    
          virt_nic_map: *default_controller_virt                                    
        roles:                                                                      
          - controller   


Simple lab config:
~~~~~~~~~~~~~~~~~~
File: random_lab_config.yaml

.. code-block:: yaml

    assign_method: "simple"
    ...
    roller:                                                                         
  controller:                                                                   
    l3_ifaces:                                                                  
      phys_nic_map: *default_controller_phys                                    
      virt_nic_map: *default_controller_virt                                    
    roles:                                                                      
      - controller                                                              
    count: 3                                                                    
  compute:                                                                      
    l3_ifaces:                                                                  
      phys_nic_map: *default_compute_phys                                       
      virt_nic_map: *default_compute_virt                                       
    roles:                                                                      
      - compute                                                                 
      - cinder                                                                  
    count: 1    

Steps logic:
~~~~~~~~~~~~

.. code-block:: bash

    $ export CLUSTER_CONFIG=config.yaml
    $ python manage_env.py


#. Remove env by name, if exist.
#. wait for enough discover nodes count
#. Create env with name and configuration from config
#. Update network and attributes
#. update common part
#. create extra part
#. replace env repos, if exist
#. Wait for needed nodes count
#. Assign nodes to cluster

- In case assign_method == 'simple':

  #. Call simple_pin_nodes_to_cluster and simple pin random node with role. Nodes
     count taken from config['roller']['controller'] OR ['compute']

 
- In case assign_method == 'hw_pin':

  #. Call strict_pin_node_to_cluster which try to find need node, using func
     check_for_name_.

10. assign\create network role to nic per node

- In case assign_method == 'simple':

  #. Call simple_pin_nw_to_node which will try to push network map for each 
     node looking into map from roller[role]['l3_ifaces']


- In case assign_method == 'hw_pin':

  #. call strict_pin_nw_to_node which will try to get network map from each 
     lab_config['nodes'][node['name']]['l3_ifaces']




.. _check_for_name:

How is script determine which node are?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
File: ipmi/netifnames.yaml

Take a look into check_for_name func.
(In general : try's find node-name from yaml by nic-mac)



Copyright
~~~~~~~~~
Script distributed by 'as-is' licence, and no one care about how its work.
Script and repo itself can brake your system.

