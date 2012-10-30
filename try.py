
p=4
q=19
D=p-q
r=21
s=24

j=[]
for i in range(0,26):
    if(((D*i)%26)==1):
        j.append(i)

print j        
k=j[0]
a=(k*(r-s))%26
b=(k*(p*s-q*r))%26

print a," ", b
