import subprocess
import sys
import os

def midi2abc(filename):
    version = sys.platform
    if (version == "win32"):
        string = "midi2abc.exe " + filename + " -o tt.txt"
        os.system(string)
        file = open("tt.txt","r")
        result = file.read()
        file.close()
        os.remove("tt.txt")
    else:
        result = subprocess.check_output(["midi2abc",filename])
    return result

def abc2midi(filename):
    version = sys.platform
    if (os.path.isfile("count.txt")== False):
        file = open("count.txt","w")
        file.write("output0.mid")
        file.close()
    file = open("count.txt","r")
    cnt = file.read()
    cnt = cnt[6:-4]
    cnt = int(cnt)
    cnt = cnt+1
    cnt = str(cnt)
    file.close()
    file = open("count.txt","w")
    string = "output"+cnt+".mid"
    file.write(string)
    file.close()
    if (version == "win32"):
        string = "abc2midi.exe " + filename + " -o output" + cnt + ".mid"
    else:
        string = "abc2midi " + filename + " -o output"+cnt+".mid"        
    os.system(string)