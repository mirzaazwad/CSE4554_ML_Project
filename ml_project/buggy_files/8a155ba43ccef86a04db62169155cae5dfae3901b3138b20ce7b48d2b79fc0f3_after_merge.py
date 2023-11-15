def printSyntax():
    printVersion()
    print(_("Usage: glances [options]"))
    print(_("\nOptions:"))
    print(_("\t-b\t\tDisplay network rate in Byte per second"))
    print(_("\t-B @IP|HOST\tBind server to the given IPv4/IPv6 address or hostname"))
    print(_("\t-c @IP|HOST\tConnect to a Glances server by IPv4/IPv6 address or hostname"))
    print(_("\t-C FILE\t\tPath to the configuration file"))
    print(_("\t-d\t\tDisable disk I/O module"))
    print(_("\t-e\t\tEnable sensors module"))
    print(_("\t-f FOLDER\tSet the HTML or CSV output folder"))
    print(_("\t-h\t\tDisplay the help and exit"))
    print(_("\t-m\t\tDisable mount module"))
    print(_("\t-n\t\tDisable network module"))
    print(_("\t-o OUTPUT\tDefine additional output (available: HTML or CSV)"))
    print(_("\t-p PORT\t\tDefine the client/server TCP port (default: %d)" %
            server_port))
    print(_("\t-P PASSWORD\tDefine a client/server password"))
    print(_("\t--password\tDefine a client/server password from the prompt"))
    print(_("\t-r\t\tDisable process list"))
    print(_("\t-s\t\tRun Glances in server mode"))
    print(_("\t-t SECONDS\tSet refresh time in seconds (default: %d sec)" %
            refresh_time))
    print(_("\t-v\t\tDisplay the version and exit"))
    print(_("\t-y\t\tEnable hddtemp module"))
    print(_("\t-z\t\tDo not use the bold color attribute"))
    print(_("\t-1\t\tStart Glances in per CPU mode"))