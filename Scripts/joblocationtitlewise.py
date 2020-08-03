import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("Final 2titles.csv")

df = df.where(df['Title'] == 'Data Scientist and Analyst')
df.dropna(inplace=True)
s=df['Location'].size
l = list(range(0, s))
df.set_index(pd.Index(l), inplace=True)
x = df['Location'].value_counts()
dict(x)

list_of_others = []
for key, value in x.items():
    if value <= 5:
        list_of_others.append(key)

for i in range(len(df)):
    if df.loc[i, 'Location'] in list_of_others:
        df.loc[i, 'Location'] = 'Others'

y = dict(df['Location'].value_counts())
plt.pie(y.values(), labels=y.keys(), radius=2, autopct=absolute_value)
plt.title("Distribution of job locations",loc='left',backgroundcolor='white', color='black',fontstyle='italic')
plt.show()