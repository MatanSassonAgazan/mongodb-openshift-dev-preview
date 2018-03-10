#!/usr/bin/python

from ansible.module_utils.basic import *


def project_present(data):
  
  def get_nvpair(name,default_value):
    value = data.get(name, default_value)
    if not value:
      value
    return { name : value }
  
  number_nodes = data['number_of_agents_only_pods']
  if not isinstance(number_nodes,int):
    try:
      number_nodes = int(number_nodes)
    except Exception as e:
      print "Can't convert number_of_agents_only_pods='%s' to int" % number_of_nodes
      print "Exception was '%s'" % s
      print "Defaulting to 3 nodes"
      number_of_nodes = 3
  auto_config = data['automation_config']
  project_name = data['cluster_name']

  # TODO: Move these default values into playbook params
  s = "mongodb-service-%s" % project_name
  d = "default.svc.cluster.local"
  processes = []
  backupVersions = []
  monitoringVersions = []
  for i in range(0,number_nodes):
    hostname = 'mongodb-server-%s-%s.%s.%s' % (project_name, i,s,d)
    backupVersion = { "hostname": hostname }

    #     "logPath": "/var/vcap/sys/log/mongod_node/backup-agent.log",$
    #     "logRotate": {$
    #         "sizeThresholdMB": 1000,$
    #         "timeThresholdHrs": 24$
    monitoringVersion = { "hostname": hostname }
    backupVersions.append( backupVersion )
    monitoringVersions.append( monitoringVersion )
  # add agents
  auto_config['backupVersions']=backupVersions
  auto_config['monitoringVersions']=monitoringVersions
 
  return { "auto_config" : auto_config
         , "meta" : "Added %s angents-only pods to %s" % (number_nodes, project_name) }


# remove cluster_name from automationConfig
def project_absent(data):
  auto_config = data['automation_config']
  project_name = data['cluster_name']
  
  
  msg = "ERROR: Not supported yet."
  return { "auto_config" : auto_config, "meta" : msg }


def main():

  fields = {
    "cluster_name" : { "required" : True, "type" : "str" },
    "automation_config" : { "required" : True, "type" : "dict" },
    "number_of_agents_only_pods" : { "type" : "int" },
    "state" : { 
      "default" : "present",
      "choices" : [ "present", "absent" ],
      "type" : "str"
    }
  }

  choice_map = { 
    "present" : project_present,
    "absent"  : project_absent
  }

  module = AnsibleModule(argument_spec=fields)
  response = {"hello": "world", "cluster_name" : module.params['cluster_name'] }
  response = choice_map.get(module.params['state'])(module.params)
  module.exit_json(changed=False, meta=response)


if __name__ == '__main__':  
    main()
