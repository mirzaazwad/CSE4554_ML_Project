def update_db_entry(app_dic, man_data_dic, man_an_dic, code_an_dic, cert_dic, bin_anal, apk_id) -> None:
    """Update an APK/ZIP DB entry"""
    try:
        # pylint: disable=E1101
        StaticAnalyzerAndroid.objects.filter(MD5=app_dic['md5']).update(
            TITLE='Static Analysis',
            APP_NAME=app_dic['app_name'],
            SIZE=app_dic['size'],
            MD5=app_dic['md5'],
            SHA1=app_dic['sha1'],
            SHA256=app_dic['sha256'],
            PACKAGENAME=man_data_dic['packagename'],
            MAINACTIVITY=man_data_dic['mainactivity'],
            TARGET_SDK=man_data_dic['target_sdk'],
            MAX_SDK=man_data_dic['max_sdk'],
            MIN_SDK=man_data_dic['min_sdk'],
            ANDROVERNAME=man_data_dic['androvername'],
            ANDROVER=man_data_dic['androver'],
            MANIFEST_ANAL=man_an_dic['manifest_anal'],
            PERMISSIONS=man_an_dic['permissons'],
            BIN_ANALYSIS=bin_anal,
            FILES=app_dic['files'],
            CERTZ=app_dic['certz'],
            ICON_HIDDEN=app_dic['icon_hidden'],
            ICON_FOUND=app_dic['icon_found'],
            ACTIVITIES=man_data_dic['activities'],
            RECEIVERS=man_data_dic['receivers'],
            PROVIDERS=man_data_dic['providers'],
            SERVICES=man_data_dic['services'],
            LIBRARIES=man_data_dic['libraries'],
            BROWSABLE=man_an_dic['browsable_activities'],
            CNT_ACT=man_an_dic['cnt_act'],
            CNT_PRO=man_an_dic['cnt_pro'],
            CNT_SER=man_an_dic['cnt_ser'],
            CNT_BRO=man_an_dic['cnt_bro'],
            CERT_INFO=cert_dic['cert_info'],
            ISSUED=cert_dic['issued'],
            SHA256DIGEST=cert_dic['sha256Digest'],
            API=code_an_dic['api'],
            DANG=code_an_dic['findings'],
            URLS=code_an_dic['urls'],
            DOMAINS=code_an_dic['domains'],
            EMAILS=code_an_dic['emails'],
            STRINGS=app_dic['strings'],
            ZIPPED=app_dic['zipped'],
            MANI=app_dic['mani'],
            EXPORTED_ACT=man_an_dic['exported_act'],
            E_ACT=man_an_dic['exported_cnt']["act"],
            E_SER=man_an_dic['exported_cnt']["ser"],
            E_BRO=man_an_dic['exported_cnt']["bro"],
            E_CNT=man_an_dic['exported_cnt']["cnt"],
            APK_ID=apk_id,
        )
    except:
        PrintException("Updating DB")