    def get_service(self):
        import httplib2
        try:
            from googleapiclient.discovery import build
        except:
            from apiclient.discovery import build

        http = httplib2.Http()
        http = self.credentials.authorize(http)
        bigquery_service = build('bigquery', 'v2', http=http)

        return bigquery_service