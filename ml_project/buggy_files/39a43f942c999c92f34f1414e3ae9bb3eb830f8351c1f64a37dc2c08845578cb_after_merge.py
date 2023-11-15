def main():
    argument_spec = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['absent', 'present']),
        data=dict(type='str'),
        data_is_b64=dict(type='bool', default=False),
        labels=dict(type='dict'),
        force=dict(type='bool', default=False)
    )

    required_if = [
        ('state', 'present', ['data'])
    ]

    client = AnsibleDockerClient(
        argument_spec=argument_spec,
        supports_check_mode=True,
        required_if=required_if,
        min_docker_version='2.6.0',
        min_docker_api_version='1.30',
    )

    try:
        results = dict(
            changed=False,
        )

        ConfigManager(client, results)()
        client.module.exit_json(**results)
    except DockerException as e:
        client.fail('An unexpected docker error occurred: {0}'.format(e), exception=traceback.format_exc())
    except RequestException as e:
        client.fail('An unexpected requests error occurred when docker-py tried to talk to the docker daemon: {0}'.format(e), exception=traceback.format_exc())