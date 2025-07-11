from itertools import permutations as p
class tas_io:
    def __init__(self, file='.tas'):
        self.file = file

    def save(self, inputs):
        encode,c = {'u':'1',
                    'd':'2',
                    'l':'3',
                    'r':'4',
                    'a':'5',
                    'b':'6',
                    'y':'7',
                    's':'8',
                    'n':'0'},''
        for i in inputs:
            a=''
            for j in i:
                try:
                    a+=encode[j]
                except:
                    raise ValueError(f"Invalid input: {j}")
            b=bin(int(''.join(min(p(a)))))[2:]+'10111001'
            c+=b
        c+='0'*min(8-(len(c)%8),abs((len(c)%8)-8))
        d=[int(c[k:k+8],2) for k in range(0,len(c),8)]
        with open(self.file+'.tas','wb') as f:
            f.write(bytes(d))
    
    def load(self):
        decode,b,c,d,e,f,g = {'1':'u',
                              '2':'d',
                              '3':'l',
                              '4':'r',
                              '5':'a',
                              '6':'b',
                              '7':'y',
                              '8':'s',
                              '0':'n'},False,0,[],[],'',[]
        with open(self.file+'.tas', 'rb') as f:
            a=bin(int(f.read().hex(),16))[2:]
        for i in range(len(a)):
            if a[i:i+8]=='10111001':
                b,c=True,i
                continue
            if b:
                b=False
                d.append(c)    
        e.append(a[:d[0]])
        for j in range(0,len(d)-1):
            e.append(a[d[j]+8:d[j+1]])
            c=j      
        for k in e:
            f=''
            for l in str(int(k,2)):
                if l in decode:
                    f+=decode[l]
                else:
                    raise ValueError(f"Invalid input: {l}")
            g.append(f)      
        return g

# 185 / b10111001 as a spacer between frames
#
#   1 / b1   up        / u
#   2 / b10  down      / d
#   3 / b11  left      / l
#   4 / b100 right     / r
#
#   5 / b101  normal   / a
#   6 / b110  special  / b
#   7 / b111  jump     / y
#   8 / b1000 shield   / s
#   0 / b0    no input / n