    def createBatchSystem(config, jobStore=None, userScript=None):
        """
        Creates an instance of the batch system specified in the given config. If a job store and
        a user script are given then the user script can be hot deployed into the workflow.

        :param toil.common.Config config: the current configuration

        :param toil.jobStores.abstractJobStore.AbstractJobStore jobStore: an instance of a jobStore

        :param ModuleDescriptor userScript: a handle to the Python module defining the root job

        :return: an instance of a concrete subclass of AbstractBatchSystem

        :rtype: batchSystems.abstractBatchSystem.AbstractBatchSystem
        """
        kwargs = dict(config=config,
                      maxCores=config.maxCores,
                      maxMemory=config.maxMemory,
                      maxDisk=config.maxDisk)

        if config.batchSystem == 'parasol':
            from toil.batchSystems.parasol import ParasolBatchSystem
            batchSystemClass = ParasolBatchSystem

        elif config.batchSystem == 'single_machine' or config.batchSystem == 'singleMachine':
            from toil.batchSystems.singleMachine import SingleMachineBatchSystem
            batchSystemClass = SingleMachineBatchSystem

        elif config.batchSystem == 'gridengine' or config.batchSystem == 'gridEngine':
            from toil.batchSystems.gridengine import GridengineBatchSystem
            batchSystemClass = GridengineBatchSystem

        elif config.batchSystem == 'lsf' or config.batchSystem == 'LSF':
            from toil.batchSystems.lsf import LSFBatchSystem
            batchSystemClass = LSFBatchSystem

        elif config.batchSystem == 'mesos' or config.batchSystem == 'Mesos':
            from toil.batchSystems.mesos.batchSystem import MesosBatchSystem
            batchSystemClass = MesosBatchSystem

            kwargs['masterAddress'] = config.mesosMasterAddress

        elif config.batchSystem == 'slurm' or config.batchSystem == 'Slurm':
            from toil.batchSystems.slurm import SlurmBatchSystem
            batchSystemClass = SlurmBatchSystem

        else:
            raise RuntimeError('Unrecognised batch system: %s' % config.batchSystem)

        if not config.disableCaching and not batchSystemClass.supportsWorkerCleanup():
            raise RuntimeError('%s currently does not support shared caching.  Set the '
                               '--disableCaching flag if you want to '
                               'use this batch system.' % config.batchSystem)
        logger.info('Using the %s' %
                    re.sub("([a-z])([A-Z])", "\g<1> \g<2>", batchSystemClass.__name__).lower())

        if jobStore is not None:
            if userScript is not None:
                if not userScript.belongsToToil and batchSystemClass.supportsHotDeployment():
                    userScriptResource = userScript.saveAsResourceTo(jobStore)
                    with jobStore.writeSharedFileStream('userScript') as f:
                        f.write(userScriptResource.pickle())
                    kwargs['userScript'] = userScriptResource
            else:
                from toil.jobStores.abstractJobStore import NoSuchFileException
                try:
                    with jobStore.readSharedFileStream('userScript') as f:
                        userScriptResource = Resource.unpickle(f.read())
                    kwargs['userScript'] = userScriptResource
                except NoSuchFileException:
                    pass

        return batchSystemClass(**kwargs)