import sys

Usage = """
Usage: DNSparse.py This script will read a dns output file and test if the entries are found in a safe list; if not they will output.

The input commands should be as follows: python DNSparse.py dns.file safe.list output.file

dns.file format: (tab formatted) bro-cut query id.orig_h < dns.log | sort -u > dns.out
safebrowsing.cache.l.google.com 10.10.249.51
safebrowsing.cache.l.google.com 10.1.1.14
img.youtube.com 10.1.1.14
4162278-0001    10.1.55.190

safe.list format: ie alexa top 1million sites
1,google.com
2,youtube.com
3,facebook.com
4,baidu.com
5,yahoo.com

local.safe format:
google.com,Comment
apple-dns.com, comment

"""

if len(sys.argv) != 4:
        print Usage
else:
        DNS = open(sys.argv[1], "r")
        Safe = open(sys.argv[2], "r")
        Out = open(sys.argv[3], "w")
        LocalSafe = open('local.safe',"r")

        LocalSafeLine=LocalSafe.readline().strip()
        SafeLine=Safe.readline().strip()        #enters into first line of file
        SafeEntries=0

        SafeDict={}     #key is entry, value is 1
        while LocalSafeLine !='':
                SafeName=LocalSafeLine.split(',')[0]
                if SafeName not in SafeDict:
                        SafeDict[SafeName]=1
                        SafeEntries+=1
                else:
                        print 'Error! Duplicated entry in safe list!',LocalSafeLine
                        sys.exit(0)
                LocalSafeLine=LocalSafe.readline().strip()

        while SafeLine != '':
                SafeName=SafeLine.split(',')[1]
                if SafeName not in SafeDict:
                        SafeDict[SafeName]=1
                        SafeEntries+=1
                else:
                        print 'Error! Duplicated entry in safe list!',SafeLine
                        sys.exit(0)
                SafeLine=Safe.readline().strip()
        DNSLine=DNS.readline().strip()  #enters into first line of file
        DNSnotFound=0
        DNSfound=0
        LocalEntry=0

        while DNSLine != '':
                DNSsiteName=DNSLine.split('\t')[0]
                if DNSsiteName.count('.') == 0: #filters out the Scripps internal computers (no periods)
                        LocalEntry+=1
                else:
                        DNSsiteNameFields=DNSsiteName.split('.')
                        WebsiteName='.'.join(DNSsiteNameFields[-2:])    #last 2 fields in website
                        #print WebsiteName+'\n'
                        if len(WebsiteName) < 6:        # change this to a higher number if need be
                                WebsiteName='.'.join(DNSsiteNameFields[-3:])    #last 3 fields in website
                        if WebsiteName not in SafeDict:
                                #Out.write(WebsiteName+'\n')
                                Out.write(DNSLine+'\n')
                                DNSnotFound+=1
                        else:
                                DNSfound+=1
                DNSLine=DNS.readline().strip()

        print 'Number of entries in safe list: '+str(SafeEntries)
        print 'Number of DNS entries not found in safe list: '+str(DNSnotFound)
        print 'Number of DNS entries found in safe list: '+str(DNSfound)
        print 'Number of Local entries: '+str(LocalEntry)


