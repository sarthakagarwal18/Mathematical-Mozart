
# coding: utf-8

# In[24]:

import os
import numpy
import Convert_MidiABC
import sys

# In[25]:

def validletter(a):
    if a == 'A' or a == 'B' or a == 'C' or a == 'D' or a == 'E' or a == 'F' or a == 'G' or a == 'X' or a == 'Z':
        return 1
    if a == 'a' or a == 'b' or a == 'c' or a == 'd' or a == 'e' or a == 'f' or a == 'g' or a == 'x' or a == 'z':
        return 1
    return 0



def cleantext(text):
	i=0
	j=0
	line = list()
	cnt = 0
	processedtext=""
	while j!=len(text):#seperating each line in abc file and removing lines which are not needed
		while(text[j]!='\n'):
			j+=1
		l = text[i:j+1]
		flag = 0
		for i in l:# if line doesn't contain '|' then it is redundant
			if i=='|':
				flag=1
				break
		if flag==1:
			line.append(l)
		j+=1
		i=j
		
	for l in line:
		if len(l) > 1:
			if (l[0] != '|' and l[0] != ':' and l[1] == ':') or l[0]=='*' or l[0] == '%':
				continue
		nl = ''
		i = 0
		cnt+=1
		while (i < len(l)):

			if l[i] == ' ' or l[i] == '~' or l[i] == '(' or l[i] == ')' or l[i] == '|' or l[i] == "\\" or l[i] == "." or l[
				i] == "+" or l[i] == "!" or l[i] == "-" or l[i] == "[" or l[i] == "]" or l[i] == "=" or l[i] == "\n" or l[
				i] == "{" or l[i] == "}"or l[i] == "*" or l[i] == "@"or l[i] == "0" or l[i] == "#":
				i += 1
				continue
			if l[i] == '%':#if comment in valid line
				break
			if validletter(l[i])==1 and (l[i+1]=='#' or l[i+1]=="'"):#abc2midi supports only one notation for sharp notes(#)
				nl += '^'
				nl+=l[i]
				i += 2
				continue
			if l[i] == '>':#a>b means a3/2b1/2
				nl += '3/2'
				if validletter(l[i + 1]) == 1:
					nl += l[i + 1]
				else:
					nl += 'G'
				nl += '/2'
				i += 2
				continue
			if l[i] == '<':#a<b means a1/2b3/2
				nl += '/2'
				if validletter(l[i + 1]) == 1:
					nl += l[i + 1]
				else:
					nl += 'G'
				nl += '3/2'
				i += 2
				continue
			if validletter(l[i]) == 1 or ((l[i] <= 'a' or l[i] >= 'z') and (l[i] <= 'A' or l[i] >= 'Z')):#add valid letters
				nl += l[i]
			i += 1
		processedtext += nl;#add modified line to final processed text
	return processedtext


# In[26]:

converted = []
for ix in range(129):
    converted.append('')


# In[27]:

def func(text):
    header = ''
    pos = 0
    ix = 0
    while ( ix < len(text) ):
        #new instrument
        if (text[ix] == 'V' and text[ix+1] == ':' and text[ix+2] >= '0' and text[ix+2]<='9'):# to get instrument voice 
            break
        else:
            header = header+ text[ix]
            ix = ix+1
    #print (header)
    while (ix<len(text)):
        
        #finding midi program number
        while (ix<len(text)):
            if (text[ix]=='%' and text[ix+1]=='%'):
                temptext = ''
                while (ix<len(text)):
                    if (text[ix] == '\n'):
                        ix = ix+1
                        break
                    else:
                        temptext = temptext + text[ix]
                        ix = ix+1
                #print (temptext)
                
                #3digit midi number
                if (temptext[-3]>='0' and temptext[-3]<='9'):
                    num = temptext[-3:] + ".txt"
                    #num = (ord(temptext[-3])-ord('0'))*100 + (ord(temptext[-2])-ord('0'))*10 + (ord(temptext[-1])-ord('0'))
                
                #2digit midi number
                else:
                    if (temptext[-2]>='0' and temptext[-2]<='9'):
                        num = temptext[-2:] + ".txt"
                        #num = (ord(temptext[-2])-ord('0'))*10 + (ord(temptext[-1])-ord('0'))
                        
                    #1digit midi number
                    else:
                        num = temptext[-1:] + ".txt"
                        #num = (ord(temptext[-1])-ord('0'))
                        
                #print (num)
                newfile = open(num,'a')
                break
            else:
                ix = ix+1
                
        
        #writing that midi program notes into the a temporary string\
        if (ix<len(text)):
            temptext = ''
            while (ix < len(text)):
                if (text[ix] == 'V' and text[ix+1] == ':' and text[ix+2] >= '0' and text[ix+2]<='9'):
                    break
                else:
                    temptext = temptext + text[ix]
                    ix = ix+1
            temptext = temptext + '\n'
            temptext = cleantext(temptext)
            if not newfile.closed:
                newfile.write(temptext)
                #newfile.write('\n')
            #converted[num] = converted[num]+ temptext
            #converted[num] = converted[num]+ '\n'
            #print (temptext)
            #newfile.close()


# In[28]:
version = sys.platform
for root,dirs,files in os.walk("."):
    for fname in files:
        if (fname[-3:] == "mid" or fname[-4:] == "midi"):
            full_path = os.path.join(root,fname)
            full_path = str(full_path)
            text = Convert_MidiABC.midi2abc(full_path)
            func(text)
            if (version == "win32"):
                os.system("cls")
            else:
                os.system("clear")
