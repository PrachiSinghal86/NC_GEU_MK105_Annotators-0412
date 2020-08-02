import pandas as pd
df = pd.read_csv("final_dataset.csv")
arr1=["css","html","bootstrap","django","rest","nosql","laravel","sql","express","bootstrap","ajax","angularjs","mongodb","react","jquery","git","mysql","nodejs","python","php"]
freq1=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
c=0
def freq(title,text):


    if(title=='Full Stack Developer'):

        text = text.split(" ")

        for i in range(len(arr1)):
            if text.count(arr1[i])>0:
                freq1[i]+=1

        return c

for i in range(len(df)):
    freq(df['Title'][i], df['Description'][i])

print(arr1)
print(freq1)