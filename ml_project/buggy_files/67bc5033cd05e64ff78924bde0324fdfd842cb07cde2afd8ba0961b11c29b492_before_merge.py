async def setup_pex_process(request: PexProcess, pex_environment: PexEnvironment) -> Process:
    argv = pex_environment.create_argv(
        f"./{request.pex.name}",
        *request.argv,
        # If the Pex isn't distributed to users, then we must use the shebang because we will have
        # used the flag `--use-first-matching-interpreter`, which requires running via shebang.
        always_use_shebang=request.pex.internal_only,
    )
    env = {**pex_environment.environment_dict, **(request.extra_env or {})}
    process = Process(
        argv,
        description=request.description,
        level=request.level,
        input_digest=request.input_digest,
        env=env,
        output_files=request.output_files,
        output_directories=request.output_directories,
        timeout_seconds=request.timeout_seconds,
        execution_slot_variable=request.execution_slot_variable,
    )
    return await Get(Process, UncacheableProcess(process)) if request.uncacheable else process