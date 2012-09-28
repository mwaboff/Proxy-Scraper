####################
#
#  Proxy Scraper
#  Michael Aboff
#
#  Scrapes proxies off of public proxy lists, many lists attempt
#  to obfuscate their lists to prevent programs exactly like this.
#
####################

import urllib2, time

# Define files to save
prefix = ""
saveSOCKS = "complete_socks.txt"
saveHTTP = "complete_http.txt"

# Should each server list save in a different place?
splitSaves = True

# Split Save locations
sockslistssave = "socks_sockslist.txt"         # Save location for sockslist.net
sockssamirsave = "socks_samair.txt"            # Save location for samair.ru
socksmegasockssave = "socks_megasocks.txt"     # Save location for megasocks.blogspot.com

httpproxyhttpsave = "http_proxyhttp.txt"       # Save location for proxyhttp.net
httpsublymecompsave = "http_sublymecomp.txt"   # Save location for Sublyme HTTP compilation


def getWebData(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    data = opener.open(url).readlines()
    opener.close()
    return data

##### Sublyme #####

def getSublymeListHttp():
    url = "http://www.sublyme.net/proxy/raw_httpproxy.php"
    
    result = parseSublyme(url)
    return result

def getSublymeListSocks():
    url = "http://www.sublyme.net/proxy/raw_socksproxy.php"
    
    result = parseSublyme(url)
    return result

def parseSublyme(url):
    webData = getWebData(url)
    proxyList = []
    for line in webData:
        for item in line.strip().split(" "):
            if ":" in item:
                proxyList.append(item)
    return proxyList


####### samair.ru #######
#Bad proxies not doing this anymore
def getSamairSocks():
    page1 = "http://samair.ru/proxy/socks01.htm"
    page2 = "http://samair.ru/proxy/socks02.htm"
    page3 = "http://samair.ru/proxy/socks03.htm"
    page4 = "http://samair.ru/proxy/socks04.htm"
    page5 = "http://samair.ru/proxy/socks05.htm"
    page6 = "http://samair.ru/proxy/socks06.htm"
    page7 = "http://samair.ru/proxy/socks07.htm"
    page8 = "http://samair.ru/proxy/socks08.htm"
    page9 = "http://samair.ru/proxy/socks09.htm"
    page10 = "http://samair.ru/proxy/socks10.htm"
    
    result = parseSamairPage(page1) + \
             parseSamairPage(page2) + \
             parseSamairPage(page3) + \
             parseSamairPage(page4) + \
             parseSamairPage(page5) + \
             parseSamairPage(page6) + \
             parseSamairPage(page7) + \
             parseSamairPage(page8) + \
             parseSamairPage(page9) + \
             parseSamairPage(page10)
    
    return result
    
def parseSamairPage(url):
    ipport = {}
    ip = ""
    port = ""
    webData = getWebData(url)
    for line in webData:
        if len(line) > 0:
            if "</script></head>" in line:
                samairDict = makeSamairDict(line.split("<")[0].strip())
            if "<tr><td>" in line:
                ipportLine = line.split("</tr>")
    result = []
    for part in ipportLine:
        if "write" in part:
            ip = part.split("td>")[1].split("<script")[0]
            portMess = part.split('write(":"+')[1].split(")")[0]
            portMessList = portMess.split("+")
            portMessTrans = []
            for thing in portMessList:
                portMessTrans.append(samairDict[thing])
            port = ''.join(portMessTrans)
            result.append(ip+":"+port)
            #print(result)
    return result

def makeSamairDict(mapLine):
    samairDict = {}
    for i in mapLine.split(";"):
        if "=" in i:
            mapLineMap = i.split("=")
            samairDict[mapLineMap[0]] = mapLineMap[1]
    return samairDict

##### proxyhttp.net #####

def getProxyHttp():
    page1 = "http://proxyhttp.net/free-list/anonymous-server-hide-ip-address#proxylist"
    page2 = "http://proxyhttp.net/free-list/anonymous-server-hide-ip-address/2#proxylist"
    page3 = "http://proxyhttp.net/free-list/anonymous-server-hide-ip-address/3#proxylist"
    page4 = "http://proxyhttp.net/free-list/anonymous-server-hide-ip-address/4#proxylist"
    page5 = "http://proxyhttp.net/free-list/anonymous-server-hide-ip-address/5#proxylist"
    page6 = "http://proxyhttp.net/free-list/anonymous-server-hide-ip-address/6#proxylist"
    page7 = "http://proxyhttp.net/free-list/anonymous-server-hide-ip-address/7#proxylist"
    page8 = "http://proxyhttp.net/free-list/anonymous-server-hide-ip-address/8#proxylist"
    page9 = "http://proxyhttp.net/free-list/anonymous-server-hide-ip-address/9#proxylist"


    result = parseSocksListPage(page1) + \
             parseSocksListPage(page2) + \
             parseSocksListPage(page3) + \
             parseSocksListPage(page4) + \
             parseSocksListPage(page5) + \
             parseSocksListPage(page6) + \
             parseSocksListPage(page7) + \
             parseSocksListPage(page8) + \
             parseSocksListPage(page9)
    
    return result

##### sockslist.net #####
def getSocksList():
    page1 = "http://sockslist.net/proxy/server-socks-hide-ip-address#proxylist"
    page2 = "http://sockslist.net/proxy/server-socks-hide-ip-address/2#proxylist"
    page3 = "http://sockslist.net/proxy/server-socks-hide-ip-address/3#proxylist"
    
    result = parseSocksListPage(page1) + parseSocksListPage(page2) + parseSocksListPage(page3)
    
    return result

    
def parseSocksListPage(url):
    ipport = {}
    ip = ""
    port = ""
    webData = getWebData(url)
    for line in webData:
        if len(line) > 0:
            if "^" in line and ";" in line and " = " in line:
                xorDict = crazyXORdecoding(line.strip())
            else:
                if "/check?i" in line and ip == "":
                    ip = line.split("=")[1].split(":")[0]
                if ">check</a>" in line and ip != "":
                    port = line.split("(")[1].split(")")[0]
                    ipport[ip] = port
                    ip = ""
                    port = ""
    #print(ipport)
    finalipport = {}
    for key in ipport:
        portparts = ipport[key].split("^")
        translateparts = []
        for i in portparts:
            if i.isdigit():
                translateparts.append(int(i))
            else:
                translateparts.append(int(xorDict[i]))
        total = translateparts[0]
        for j in range(1, len(translateparts)):
            total = total^translateparts[j]
        finalipport[key] = str(total)
    result = []
    
    for key in finalipport:
        result.append(key+":"+finalipport[key])
    
    return result
                
def crazyXORdecoding(line):
    """
    Recursion is for losers
    """
    xorDict = {}
    alist1 = line.split(";")
    for i in alist1:
        if "=" in i:
            xorDict[i.split(" = ")[0]] = i.split(" = ")[1]
    
    for i in xorDict:
        recursiveXORdecode(xorDict, i)
    return xorDict

def recursiveXORdecode(xorDict, akey):
    """
    Errr... I meant for winners!
    """
    if akey.isdigit():
        return akey
    avalue = xorDict[akey]
    if avalue.isdigit():
        return avalue
    elif "^" in avalue:
        avalue1, avalue2 = avalue.split("^")
        answer = str(int(recursiveXORdecode(xorDict, avalue1)) ^ int(recursiveXORdecode(xorDict, avalue2)))
        xorDict[akey] = answer
        return answer

#########################

def writeToFile(fileName, proxyList):
    print("[EMY SCRAPE] Writing to %s..." % fileName)
    stringToWrite = "\n".join(proxyList)
    f = open(prefix+fileName, 'w')
    f.write(stringToWrite)
    f.close()

def printIntro():
    print("#############################################")
    print("#                                           #")
    print("#   Proxy Scrape - A Python Proxy Scraper   #")
    print("#    by Michael Aboff                       #")
    print("#                                           #")
    print("#############################################")
    print("Proxies scraped from:")
    print("megasocks.blogspot.com, samair.ru, proxyhttp.net, and sockslist.net")
    print("\n")
    
    
def main():
    printIntro()    
    print("[SCRAPER] Beginning to scrape HTTP proxies...")
    starttime = time.time()
    starttime2 = time.time()
    proxyHttp = getProxyHttp()
    endtime2 = time.time() - starttime2
    starttime3 = time.time()
    sublymeHttp = getSublymeListHttp()
    endtime3 = time.time() - starttime3
    httpProxies = proxyHttp + sublymeHttp
    httpProxies = list(set(httpProxies))
    endtime = time.time() - starttime
    print("[SCRAPER] Total HTTP proxies:             %i (%.2fsec)" % (len(httpProxies), endtime))
    print("                proxyhttp.net:            %i (%.2fsec)" % (len(proxyHttp), endtime2))
    print("                sublyme.net:              %i (%.2fsec)" % (len(sublymeHttp), endtime3))
    writeToFile(saveHTTP, httpProxies)
    writeToFile(httpproxyhttpsave, proxyHttp)
    writeToFile(httpsublymecompsave, sublymeHttp)
    print("[SCRAPER] Write complete.")
    
    print("[SCRAPER] Beginning to scrape SOCKS proxies...")
    starttime = time.time()
    starttime2 = time.time()
    socksListNet = getSocksList()
    endtime2 = time.time() - starttime2
    starttime3 = time.time()
    #samairSocks = getSamairSocks()
    endtime3 = time.time() - starttime3
    starttime4 = time.time()
    megaSocks = getSublymeListSocks()
    endtime4 = time.time() - starttime4
    #socksProxies = socksListNet + samairSocks + megaSocks
    socksProxies = socksListNet + megaSocks
    socksProxies = list(set(socksProxies))
    endtime = time.time() - starttime
    print("[SCRAPER] Total HTTP proxies:             %i (%.2fsec)" % (len(socksProxies), endtime))
    print("                sockslist.net:            %i (%.2fsec)" % (len(socksListNet), endtime2))
#    print("                 samair.ru:                %i (%.2fsec)" % (len(samairSocks), endtime3))
    print("                megasocks.blogspot.com:   %i (%.2fsec)" % (len(megaSocks), endtime4))
    writeToFile(saveSOCKS, socksProxies)
    writeToFile(sockslistssave, socksListNet)
#    writeToFile(sockssamirsave, samairSocks)
    writeToFile(socksmegasockssave, megaSocks)
    print("[SCRAPER] Write complete.")

    print("[SCRAPER] Done.")
main()


