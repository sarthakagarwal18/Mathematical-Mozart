fp=open(r'C:\Users\vaibhav\Desktop\tunes.txt')
gp=open(r'C:\Users\vaibhav\Desktop\tunesfinal.txt','w')
line=list()
while 1:
    l=fp.readline()
    line.append(l)
    if not l:
        break
for l in line:
    if len(l)>1:
        if (ord(l[0])>=65 and ord(l[0])<=90 and l[1]==':') or l[0]=='%' :
            continue
    print(l)
    gp.write(l)

