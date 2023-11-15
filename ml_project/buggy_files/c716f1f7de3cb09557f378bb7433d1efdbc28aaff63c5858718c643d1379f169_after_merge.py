async def run_background_trio_services(services: Sequence[ServiceAPI]) -> None:
    async with contextlib.AsyncExitStack() as stack:
        managers = tuple([
            await stack.enter_async_context(background_trio_service(service))
            for service in services
        ])
        # If any of the services terminate, we do so as well.
        await wait_first_trio([
            manager.wait_finished
            for manager in managers
        ])