import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re


df = pd.read_csv("Final 2.csv")
for i in df['Salary']:
  if(type(i)==float):
    print(i)
def avg(text):
  if '-' not in text:
    return int(text)
  else:
    x=text.find('-')
    c=(int(text[:x])+int(text[x+1:]))//2
    return c
y=avg(df['Salary'][0])
print(y)
print(type(df['Salary'][0]))
df['Salary']=df['Salary'].apply(avg)
print(co)
x=[]
for i in range(len(df)):
    if(df['Title'][i]=='App Developer'):
        if(df['Salary'][i]<3000000):
            x.append(df['Salary'][i])

plt.hist(x, bins = 20, edgecolor='white')
plt.ticklabel_format(axis='x',style='plain')
x_ticks = np.arange(0, 3000000, 250000)
plt.xticks(x_ticks)
plt.xticks(fontsize=6)
plt.yticks(fontsize=15)
plt.xlabel('Salary')
plt.ylabel('No. of Jobs')
plt.show()