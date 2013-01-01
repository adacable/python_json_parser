import sys, json, os,re
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
def streamdigest(level,patternlist,jsonin):
    try:
        if type(jsonin) == list:
            for i in range(len(jsonin)):
                if type(patternlist[level].match(str(i))) == None:
                    pass
                elif type(patternlist[level].match(str(i))) != None:
                    streamdigest(level + 1,patternlist,jsonin[i])
        elif type(jsonin) == dict:
            for key in jsonin.keys():
                if patternlist[level].match(key):
                    streamdigest(level + 1,patternlist,jsonin[key])
        elif type(jsonin) in [str,int,unicode]:
            if type(jsonin) == str:
                try:
                    jsonin = json.load(jsonin)
                    streamdigest(level + 1,patternlist,jsonin[key])
                except:
                    print jsonin
            else:
                print jsonin
    except:
        pass
def patterntolist(pattern):
     listin = pattern.split('@')
     for n in range(len(listin)):
         try:
             if  listin[n][-1:] == "\\":
                 listin[n] = listin[n] +"@"+ listin[n+1]
                 del(listin[n+1])
         except:
            break
     return [re.compile(i) for i in listin]
currentpath = "./jsonout"
options = """-o=output directory
-s=pattern  for streaming interface. use -h for more or -eg for examples
-h help
-eg for -s examples"""
helptext = "current options are:" + options + """\n basic instructions- pipe json into stdin (hint- use curl for web or '< filename' from a file)
If -o is used, the program will create a file tree based on the json input- lists will create a set of directories numbered after the positive intitgers, and the values are stored in plain text files.
    If no =path is used, the program writes to /jsonout as standard
If -s<pattern> is used, then a pattern should be passed to tell the program what to pass on. If no pattern is passed, it the program will act as a transparent pipe, and print every line it is passed to stdout.
    A pattern should be constucted in the following form:
    '@<segment>@<segment>@<segment>' (quotes included)
    Where a segment is a python regex to match each level of the filetree. leave a null string(<pattern>@@<pattern> to match any text or number)
use -eg for examples"""
for arg in sys.argv[1:]:
    if arg[:2] == "-o":
        if arg[3:] == "":
            pass
        else:
            currentpath = arg[3:]
        for line in sys.stdin.readlines():
            digestedjson = json.loads(line)
            digest(digestedjson,currentpath)
    if arg[:2] == "-h":
        print helptext
    if arg[:2] == "-s":
        if arg[3:] == "":
            for line in sys.stdin.readlines():
                print line
        else:
            for line in sys.stdin.readlines():
                streamdigest(0,patterntolist(arg[2:]),json.loads(line))
    else:
        print("unknown argument- current options:")
        print(options)
        raise Exception('Bad input')
