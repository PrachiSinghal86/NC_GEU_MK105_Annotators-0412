import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from palettable.colorbrewer.qualitative import Pastel1_7


df = pd.read_csv("Final 2titles.csv")
df=df.where(df['Location']=='Pune')
df.dropna(inplace=True)
d=dict(df['Title'].value_counts())
print(d)
x=d.values()
y=d.keys()
q=np.array(df['Title'].value_counts())
def absolute_value(val):
    a  = np.round(val/100.*q.sum(), 0)
    return a

my_circle=plt.Circle( (0,0), 0.8, color='white')
plt.pie(x,labels=y,radius=2,autopct=absolute_value,colors=Pastel1_7.hex_colors)
plt.title("City wise distribution of job titles ",loc='left',backgroundcolor='black', color='white',fontstyle='italic')
p=plt.gcf()
p.gca().add_artist(my_circle)
plt.show()