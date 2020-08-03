import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
fig = plt.figure()
ax = fig.add_axes([0.8,0.8,0.8,0.8])
df=pd.read_csv('Final 2titles.csv')
x=df['Title']

val=[]
c=dict(df['Title'].value_counts())
x=c.values()
y=c.keys()
p=np.array(df['Title'].value_counts())
def absolute_value(val):
    a  = np.round(val/100.*p.sum(), 0)
    return a
plt.pie(x,labels=y,radius=2,autopct=absolute_value)
plt.title("Distribution of job titles",loc='left',backgroundcolor='white', color='black',fontstyle='italic')
plt.show()