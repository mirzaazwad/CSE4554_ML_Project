    def __add_new_params__(self) -> str:
        query = {
            'aid': 1988,
            'app_name': 'tiktok_web',
            'device_platform': 'web',
            'Referer': '',
            'user_agent': self.__format_new_params__(self.userAgent),
            'cookie_enabled': 'true',
            'screen_width': self.width,
            'screen_height': self.height,
            'browser_language': self.browser_language,
            'browser_platform': self.browser_platform,
            'browser_name': self.browser_name,
            'browser_version': self.browser_version,
            'browser_online': 'true',
            'ac': '4g',
            'timezone_name': self.timezone_name,
            'appId': 1233,
            'appType': 'm',
            'isAndroid': False,
            'isMobile': False,
            'isIOS': False,
            'OS': 'windows'
        }
        return urlencode(query)