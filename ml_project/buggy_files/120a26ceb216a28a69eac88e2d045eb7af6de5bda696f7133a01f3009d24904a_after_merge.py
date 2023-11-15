    def get_cookie(self, name):
        """Returns information of cookie with ``name`` as an object.

        If no cookie is found with ``name``, keyword fails. The cookie object
        contains details about the cookie. Attributes available in the object
        are documented in the table below.

        | = Attribute = |             = Explanation =                                |
        | name          | The name of a cookie.                                      |
        | value         | Value of the cookie.                                       |
        | path          | Indicates a URL path, for example ``/``.                   |
        | domain        | The domain the cookie is visible to.                       |
        | secure        | When true, cookie is only used with HTTPS connections.     |
        | httpOnly      | When true, cookie is not accessible via JavaScript.        |
        | expiry        | Python datetime object indicating when the cookie expires. |
        | extra         | Possible attributes outside of the WebDriver specification |

        See the
        [https://w3c.github.io/webdriver/#cookies|WebDriver specification]
        for details about the cookie information.
        Notice that ``expiry`` is specified as a
        [https://docs.python.org/3/library/datetime.html#datetime.datetime|datetime object],
        not as seconds since Unix Epoch like WebDriver natively does.

        In some cases, example when running browser in the cloud, it is possible that
        cookie contains other attributes than is defined in the
        [https://w3c.github.io/webdriver/#cookies|WebDriver specification].
        These other attributes are available in a ``extra`` attribute in the cookie
        object and it contains a dictionary of the other attributes. The ``extra``
        attribute is new in SeleniumLibrary 4.0.

        Example:
        | `Add Cookie`      | foo             | bar |
        | ${cookie} =       | `Get Cookie`    | foo |
        | `Should Be Equal` | ${cookie.name}  | bar |
        | `Should Be Equal` | ${cookie.value} | foo |
        | `Should Be True`  | ${cookie.expiry.year} > 2017 |

        New in SeleniumLibrary 3.0.
        """
        cookie = self.driver.get_cookie(name)
        if not cookie:
            raise CookieNotFound("Cookie with name '%s' not found." % name)
        return CookieInformation(**cookie)