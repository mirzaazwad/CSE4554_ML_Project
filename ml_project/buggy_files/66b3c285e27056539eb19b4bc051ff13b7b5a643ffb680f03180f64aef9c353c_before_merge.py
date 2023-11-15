def get_parser_to_add_opt_out_options_to(parser):
    """
    The pre-commit hook gets e.g. `--no-jwt-scan` type options
    as well as the subparser for `detect-secrets scan`.

    :rtype: argparse.ArgumentParser
    :returns: argparse.ArgumentParser to pass into PluginOptions
    """
    if parser.prog == 'detect-secrets-hook':
        return parser

    for action in parser._actions:  # pragma: no cover (Always returns)
        if isinstance(action, argparse._SubParsersAction):
            for subparser in action.choices.values():
                if subparser.prog.endswith('scan'):
                    return subparser