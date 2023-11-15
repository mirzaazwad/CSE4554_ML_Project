def main():
    """Main"""
    argument_spec = vmware_argument_spec()
    argument_spec.update(
        cluster_name=dict(type='str', required=False),
        esxi_hostname=dict(type='str', required=False),
        capabilities=dict(type='bool', required=False, default=False),
        directpath_io=dict(type='bool', required=False, default=False),
        sriov=dict(type='bool', required=False, default=False),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_one_of=[
            ['cluster_name', 'esxi_hostname'],
        ],
        supports_check_mode=True,
    )

    host_vmnic_mgr = HostVmnicMgr(module)
    module.exit_json(changed=False, hosts_vmnics_facts=host_vmnic_mgr.gather_host_vmnic_facts())