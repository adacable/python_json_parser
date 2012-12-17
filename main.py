import sys, json, os
def digest(jsonin,basepath):
    if type(jsonin) == list:
        n = 0
        for i in jsonin:
            try:
                os.mkdir(basepath)
            except:
                pass
            digest(i,basepath +"/" + str(n))
            n = n+1
    elif type(jsonin) == dict:
        try:
            os.mkdir(basepath)
        except:
            pass
        for k in jsonin.keys():
            digest(jsonin[k],basepath + "/" + k)
    elif type(jsonin) in [int,str]:
        fileout = open(basepath,"w") 
        fileout.write(str(jsonin))
        fileout.close()
currentpath = "./jsonout"
options = "-o=output directory"
for arg in sys.argv[1:]:
    if arg[:2] == "-o":
        currentpath = arg[3:]
    else:
        print("unknown argument- current options:")
        print(options)
        raise Exception('Bad input')
for line in sys.stdin.readlines():
    digestedjson = json.loads(line)
    digest(digestedjson,currentpath)
