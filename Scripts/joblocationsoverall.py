import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("Final 2titles.csv")

x = df['Location'].value_counts()
dict(x)

list_of_others = []
for key, value in x.items():
    if value <= 5:
        list_of_others.append(key)

for i in range(len(df)):
    if df.loc[i, 'Location'] in list_of_others:
        df.loc[i, 'Location'] = 'Others'

p=np.array(df['Title'].value_counts())
def absolute_value(val):
    a  = np.round(val/100.*p.sum(), 0)
    return a

y = dict(df['Location'].value_counts())
print(y)
plt.pie(y.values(), labels=y.keys(), radius=2.27, autopct=absolute_value)
plt.title("Distribution of job locations",loc='left',backgroundcolor='white', color='black',fontstyle='italic')
plt.show()