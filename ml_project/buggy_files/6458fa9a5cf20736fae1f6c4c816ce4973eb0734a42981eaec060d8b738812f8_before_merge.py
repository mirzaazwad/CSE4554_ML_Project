    def parse(cls, filename, library_file=None, cover_data=False,
            encoding_errors="strict", parse_speed=0.5, text=False,
            full=True, legacy_stream_display=False):
        """
        Analyze a media file using libmediainfo.
        If libmediainfo is located in a non-standard location, the `library_file` parameter can be used:

        >>> pymediainfo.MediaInfo.parse("tests/data/sample.mkv",
        ...     library_file="/path/to/libmediainfo.dylib")

        :param filename: path to the media file which will be analyzed.
            A URL can also be used if libmediainfo was compiled
            with CURL support.
        :param str library_file: path to the libmediainfo library, this should only be used if the library cannot be auto-detected.
        :param bool cover_data: whether to retrieve cover data as base64.
        :param str encoding_errors: option to pass to :func:`str.encode`'s `errors`
            parameter before parsing MediaInfo's XML output.
        :param float parse_speed: passed to the library as `ParseSpeed`,
            this option takes values between 0 and 1.
            A higher value will yield more precise results in some cases
            but will also increase parsing time.
        :param bool text: if ``True``, MediaInfo's text output will be returned instead
            of a :class:`MediaInfo` object.
        :param bool full: display additional tags, including computer-readable values
            for sizes and durations.
        :param bool legacy_stream_display: display additional information about streams.
        :type filename: str or pathlib.Path
        :rtype: str if `text` is ``True``.
        :rtype: :class:`MediaInfo` otherwise.
        :raises FileNotFoundError: if passed a non-existent file
            (Python ≥ 3.3), does not work on Windows.
        :raises IOError: if passed a non-existent file (Python < 3.3),
            does not work on Windows.
        :raises RuntimeError: if parsing fails, this should not
            happen unless libmediainfo itself fails.
        """
        lib = cls._get_library(library_file)
        if pathlib is not None and isinstance(filename, pathlib.PurePath):
            filename = str(filename)
            url = False
        else:
            url = urlparse.urlparse(filename)
        # Try to open the file (if it's not a URL)
        # Doesn't work on Windows because paths are URLs
        if not (url and url.scheme):
            # Test whether the file is readable
            with open(filename, "rb"):
                pass
        # Obtain the library version
        lib_version = lib.MediaInfo_Option(None, "Info_Version", "")
        lib_version = tuple(int(_) for _ in re.search("^MediaInfoLib - v(\\S+)", lib_version).group(1).split("."))
        # The XML option was renamed starting with version 17.10
        if lib_version >= (17, 10):
            xml_option = "OLDXML"
        else:
            xml_option = "XML"
        # Cover_Data is not extracted by default since version 18.03
        # See https://github.com/MediaArea/MediaInfoLib/commit/d8fd88a1c282d1c09388c55ee0b46029e7330690
        if cover_data and lib_version >= (18, 3):
            lib.MediaInfo_Option(None, "Cover_Data", "base64")
        # Create a MediaInfo handle
        handle = lib.MediaInfo_New()
        lib.MediaInfo_Option(handle, "CharSet", "UTF-8")
        # Fix for https://github.com/sbraz/pymediainfo/issues/22
        # Python 2 does not change LC_CTYPE
        # at startup: https://bugs.python.org/issue6203
        if (sys.version_info < (3,) and os.name == "posix"
                and locale.getlocale() == (None, None)):
            locale.setlocale(locale.LC_CTYPE, locale.getdefaultlocale())
        lib.MediaInfo_Option(None, "Inform", "" if text else xml_option)
        lib.MediaInfo_Option(None, "Complete", "1" if full else "")
        lib.MediaInfo_Option(None, "ParseSpeed", str(parse_speed))
        lib.MediaInfo_Option(None, "LegacyStreamDisplay", "1" if legacy_stream_display else "")
        if lib.MediaInfo_Open(handle, filename) == 0:
            raise RuntimeError("An eror occured while opening {}"
                    " with libmediainfo".format(filename))
        output = lib.MediaInfo_Inform(handle, 0)
        # Delete the handle
        lib.MediaInfo_Close(handle)
        lib.MediaInfo_Delete(handle)
        if text:
            return output
        else:
            return cls(output, encoding_errors)