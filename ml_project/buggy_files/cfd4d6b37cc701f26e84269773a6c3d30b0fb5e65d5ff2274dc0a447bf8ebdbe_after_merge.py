    def __init__(self, vault_name, region):
        self.st = datetime.datetime.now()
        self.vault_name = vault_name
        self.region = region
        self.archives = {}
        self.jobs = {}