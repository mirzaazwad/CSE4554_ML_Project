def view(request):
    """View File"""
    logger.info("Viewing File")
    try:
        typ = ''
        fil = ''
        rtyp = ''
        dat = ''
        if re.match('^[0-9a-f]{32}$', request.GET['md5']):
            fil = request.GET['file']
            md5_hash = request.GET['md5']
            typ = request.GET['type']
            src = os.path.join(settings.UPLD_DIR,
                               md5_hash + '/DYNAMIC_DeviceData/')
            sfile = os.path.join(src, fil)
            # Prevent Directory Traversal Attacks
            if ("../" in fil) or ("%2e%2e" in fil) or (".." in fil) or ("%252e" in fil):
                return HttpResponseRedirect('/error/')
            else:
                with io.open(sfile, mode='r', encoding="utf8", errors="ignore") as flip:
                    dat = flip.read()
                if (fil.endswith('.xml')) and (typ == 'xml'):
                    rtyp = 'xml'
                elif typ == 'db':
                    dat = handle_sqlite(sfile)
                    rtyp = 'asciidoc'
                elif typ == 'others':
                    rtyp = 'asciidoc'
                else:
                    return HttpResponseRedirect('/error/')
                context = {'title': escape(ntpath.basename(fil)), 'file': escape(
                    ntpath.basename(fil)), 'dat': dat, 'type': rtyp, }
                template = "general/view.html"
                return render(request, template, context)

        else:
            return HttpResponseRedirect('/error/')
    except:
        PrintException("[ERROR] Viewing File")
        return HttpResponseRedirect('/error/')