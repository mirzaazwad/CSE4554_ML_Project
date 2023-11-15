def main():
    """entry point for module execution
    """
    argument_spec = dict(
        commands=dict(type='list', required=True),
        display=dict(choices=['text', 'json', 'xml'], default='text', aliases=['format', 'output']),

        # deprecated (Ansible 2.3) - use junos_rpc
        rpcs=dict(type='list'),

        wait_for=dict(type='list', aliases=['waitfor']),
        match=dict(default='all', choices=['all', 'any']),

        retries=dict(default=10, type='int'),
        interval=dict(default=1, type='int')
    )

    argument_spec.update(junos_argument_spec)

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=True)


    warnings = list()
    check_args(module, warnings)

    commands = parse_commands(module, warnings)

    wait_for = module.params['wait_for'] or list()
    display = module.params['display']
    conditionals = [Conditional(c) for c in wait_for]

    retries = module.params['retries']
    interval = module.params['interval']
    match = module.params['match']

    while retries > 0:
        responses = run_commands(module, commands)

        for item in list(conditionals):

            for index, (resp, cmd) in enumerate(zip(responses, commands)):
                if cmd['output'] == 'xml':
                    if not HAS_JXMLEASE:
                        module.fail_json(msg='jxmlease is required but does not appear to '
                            'be installed.  It can be installed using `pip install jxmlease`')
                    responses[index] = jxmlease.parse(resp)

            try:
                if item(responses):
                    if match == 'any':
                        conditionals = list()
                        break
                    conditionals.remove(item)
            except FailedConditionalError:
                pass

        if not conditionals:
            break

        time.sleep(interval)
        retries -= 1

    if conditionals:
        failed_conditions = [item.raw for item in conditionals]
        msg = 'One or more conditional statements have not be satisfied'
        module.fail_json(msg=msg, failed_conditions=failed_conditions)

    result = {
        'changed': False,
        'warnings': warnings,
        'stdout': responses,
        'stdout_lines': to_lines(responses)
    }


    module.exit_json(**result)