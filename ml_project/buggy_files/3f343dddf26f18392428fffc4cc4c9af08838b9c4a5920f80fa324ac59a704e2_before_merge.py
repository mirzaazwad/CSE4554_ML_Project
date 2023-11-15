    def set(self, value):

        db.metrics.update_one(
            {
                "group": self.group,
                "name": self.name
            },
            {
                "group": self.group,
                "name": self.name,
                "title": self.title,
                "description": self.description,
                "value": value,
                "type": "gauge"
            },
            True
        )