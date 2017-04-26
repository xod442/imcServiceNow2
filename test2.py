vxlan = {}
    url = 'http://%s:%s@%s/command-api' % (cvp_user,cvp_word,vx['ipAddress'])
    switcher = Server(url)
    try:
        response = switcher.runCmds(1,['show interfaces vxlan 1'])
        vxlan_list.append(response[0]['interfaces']['vlanToVtepList'])
    except:
        pass
