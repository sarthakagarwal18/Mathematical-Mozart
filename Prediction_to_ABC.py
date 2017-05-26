from math import floor
import random

def validnote(a):
    if a == 'A' or a == 'B' or a == 'C' or a == 'D' or a == 'E' or a == 'F' or a == 'G':
        return 3
    if  a == 'X' or a == 'Z' or a == 'x' or a == 'z':
        return 2
    if a == 'a' or a == 'b' or a == 'c' or a == 'd' or a == 'e' or a == 'f' or a == 'g' :
        return 1
    return 0


def fractostring(frac):#convert fraction to string

    if frac== 0:
        return ''
    if frac == 0.25:
        return '/4'
    if frac == 0.125:
        return '/8'
    if frac == 0.375:
        return '3/8'
    if frac == 0.5:
        return '/2'
    if frac == 0.625:
        return '5/8'
    if frac == 0.75:
        return '3/4'
    if frac == 0.875:
        return '7/8'
    if frac == 1.0:
        return ''
    if frac == 1.25:
        return '5/4'
    if frac == 1.5:
        return '3/2'
    if frac == 2.0:
        return '2'
    print(frac)


def convert(ch,text, temp, meter, key):#choice , predicted text, selected tempo, meter and key
    if (len(text) < 10):
        return ""
    meterstring = meter
    beats = float(meter[0])
    notelength = float(meter[2])
    keystring = key
    if temp == "Slow":
        tempo = 60
    else:
        tempo = 120

    text += "nnnnn"
    cnt = 0.0
    flag = 0
    flag2 = 0
    cntcol = 0
    inst=0
    if ch==0:
        inst=0
    elif ch==1:
        inst=24
    elif ch==2:
        inst=73
    else:
        inst=40
    res = "X:1\nT:PREDICTION\nM:" + meterstring + "\nK:" + keystring + "\nQ:1/2=" + str(tempo) + "\nV:1\n%%MIDI program "+str(inst)+"\n"#providing initial fixed syntax
    i = 0
    cntt = 0
    chord=""
    while i < len(text):
        if text[i]=='\n' or text[i]=="'" or text[i]==":":#remove new line characters and other redundant characters
            i+=1
            continue
        if text[i] == ',' or text[i] == '^' or text[i] == "'" or text[i] == '`':
            if text[i]=="," and validnote(res[-1])!=3:# ','(flat) can only be placed after capital letter characters 
                i+=1
                continue
            if (res[-1] >= '0' and res[-1] <= '9') or res[-1] == '/' or res[-1] == '|' or res[-1]=='"':#these characters should be after validnotes 
                i += 1
                continue

        if cnt == beats and flag == 0:# beat count reached add '|'
            if cntcol == 2:
                res += '::'
            if cntcol == 1 and flag2 == 0:
                res += ':'
            if cntcol != 2:
                res += '|'
            if cntcol == 1 and flag2 == 1:
                res += ':'
            if cntcol == 1:
                flag2 ^= 1
            res+=chord#adding the chord calculated previously
            chord = ""
            cnt = 0.0
            cntt += 1
            # print(cntt)
            cntcol = 0

        if text[i] == '_' or text[i]=='^':#after these characters a validnote should be there
            if (validnote(text[i+1])==1 or validnote(text[i+1])==3) and cnt<beats:
                res += text[i]
            i += 1
            continue

        if ((text[i] >= '0' and text[i] <= '9') or text[i] == '/'):# '|' or '"' should be followed by valid note
            if res[-1] == '|' or res[-1]=='"':
                i += 1
                continue

        if text[i] == 'n':#to end loop
            break
        if text[i] == '/' and ((validnote(res[-1]) == 0 and validnote(text[i + 1])) or res[-2] == '/'):# to avoid "/2/" since "2/" is allowed
            i += 1
            continue
        if text[i] == ':':#handle colons
            i += 1
            cntcol += 1
            continue

        if text[i] == '"':#creating chord ("")
            j=i+1
            while text[j]!='"' and j<=i+2:
                j+=1
            if validnote(text[i + 1])==3:
                chord = '"' + text[i + 1] + '"'
            elif validnote(text[i + 2])==3:
                chord = '"' + text[i + 2] + '"'
            else:
                num = int(random.uniform(0,7))
                chordname = chr(ord('A')+num)
                chord='"' + chordname + '"'
            i=j+1
            continue

        if text[i] >= '0' and text[i] <= '9' and res[-1] >= '0' and res[-1] <= '9':#number after number
            i += 1
            continue

        if validnote(text[i]) :# if letter
            res += text[i]
            i+=1
            if validnote(text[i])==3:
                while (text[i] == ','):# subsequent commas
                    res += text[i]
                    i += 1
            else:
                while (text[i] == ','):
                    i += 1
            if text[i] == '/' or (text[i] >= '0' and text[i] <= '9'):# if followed by a number
                continue
            else:
                if cnt + 1.0 > beats:
                    req = beats - cnt
                    res += fractostring(req)
                    cnt = beats
                else:
                    cnt += 1.0
                continue

        if text[i] >= '0' and text[i] <= '9':

            if text[i + 1] == '/' and text[i + 2] >= '0' and text[i + 2] <= '9':# fractions like 3/2 3/8 etc
                temp = text[i + 2]
                if temp == '3' or temp == '5' or temp == '6' or temp == '7' or temp == '9':
                    temp = '2'
                cur = float(float(ord(text[i]) - 48) / float(ord(temp) - 48))
                if cnt + cur > beats:
                    req = beats - cnt
                    if req <= 1.0:
                        res += fractostring(req)
                        cnt = beats
                    else:
                        req = floor(req)
                        res += chr(48 + int(req))
                        cnt += req
                else:
                    cnt += cur
                    res += text[i]
                    res += text[i + 1]
                    res += temp
                i += 3
            else:# whole numbers
                cur = float(ord(text[i]) - 48)
                if cnt + cur > beats:
                    req = beats - cnt
                    if req < 1:
                        res += fractostring(req)
                        cnt = beats
                    else:
                        req = floor(req)
                        res += chr(48 + int(req))
                        cnt += req
                else:
                    res += text[i]
                    cnt += cur
                i += 1
            continue

        if text[i] == '/' and not (text[i + 1] >= '0' and text[i + 1] <= '9'):#/=='/2' //=='/4'
            curcnt = 0
            while text[i] == '/':
                i += 1
                curcnt += 1
            p = 0.5
            while curcnt > 1:#calculate power of 2
                p = p * p
                curcnt -= 1
            if cnt + p > beats:
                req = beats - cnt
                cnt = beats
                res += fractostring(req)
            else:
                cnt += p
                res += fractostring(p)
            continue
        if text[i] == '/':
            temp = text[i + 1]
            if temp == '3' or temp == '5' or temp == '6' or temp == '7' or temp == '9':
                temp = '2'#powers of two supported in abc2midi
            cur = float(1.0 / (ord(temp) - 48))
            if cnt + cur > beats:
                req = beats - cnt
                cnt = beats
                res += fractostring(req)
            else:
                res += text[i]
                res += temp
                cnt += cur
            i += 2
            continue

        res += text[i]
        i += 1
    i = len(res) - 1
    while res[i] != '|':
        i -= 1
    return res[:i + 1]
