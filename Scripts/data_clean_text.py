#warnings :)

import warnings
warnings.filterwarnings('ignore')
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import re
import string
import numpy as np
import pandas as pd

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

custom_stop_words = ['immidiate', 'job','senior','looking','title','salary','junior','experience','contract','permanent','full-time','work', \
                    'officer','manager','capgemini','geelong','men','newcastle','business analyst','level','please','button',
                     'call','recruitment', 'international','need', 'follow','type' ,'fulltimesalary','company', 'base',\
                     'end', 'development','detail', 'understand','whats', 'next','opportunity', 'rolethe','level',\
                     'please','skills','delhi',  'responsibilitieswhat','cbd','opportunity','minimum','month','understandingattention',\
                     'detailwork','bonus' ,'great','terry', 'chandramun','cv', 'call','applicants','encourage','act',\
                     'australia','fourquarters', 'com','send', 'update','join','shortlist','contact','change','within',\
                     'first', 'instance','www', 'au','add','advantage','location', 'Mumbai','environment', 'excellent',\
                     'digital', 'service','new','ensure','accurate','lead', 'organisation','ability', 'quickly',\
                     'team', 'well','position', 'us','suit','look', 'confidential','discussion', 'career','would','ideal',\
                     'previouslyworking', 'Indore', 'ofexecutive', 'note', 'role', 'squad', 'youto', 'squad', 'anzat',\
                     'culture', 'companyour', 'responsiblefor', 'passion', 'good', 'maintenancebasic', 'professional', 'drive',\
                     'suburbs', 'learn', 'ideas', 'continuous', 'consdier', 'consdier', 'due', 'continuous','growth',\
                     'communication','India', 'innovative', 'anz', 'southeast','adelaide', 'successful', 'consider',\
                     'global', 'regard', 'citizens', 'chapter', 'clean', 'conduit', 'property', 'dan', 'closely', 'immediately',\
                     'wire', 'handle', 'also', 'successful', 'eventually', 'turn', 'candidate','smart', 'publish', 'disability',\
                     'Noida', 'personal', 'promote', 'underperformance', 'create', 'proactively', 'topic',\
                     'expertise','improve','datadriven','receive','data','set','standards','hill','prominent','woolworths',\
                     'highly','group','headquarters','wa','Pune','client','medical','center','seer','already',\
                     'technologyabout', 'youbechlors']
df = pd.read_csv("naukriunicloud.csv")

def res(text):
  s=[]
  for i in text:
    try:
      if(int(i)<20):
        s.append(i);
    except:
      s.append(i)
  return s



def remove_punc(text):
  no_punct=""
  for c in text:
    if c not in string.punctuation:
      no_punct=no_punct+c
    else:
      no_punct=no_punct+" "

  return no_punct
tokenizer=RegexpTokenizer(r'\w+')
df['Description']=df['Description'].astype(str)

df['Description']=df['Description'].apply(lambda x: tokenizer.tokenize(x.lower()))
df['Description']=df['Description'].apply(lambda x: res(x))
def remove_stopwords(text):
  words=[c for c in text if c not in stopwords.words('english')]

  return words
df['Description']=df['Description'].apply(lambda x: remove_stopwords(x))

lemmatizer=WordNetLemmatizer()
def word_lemmentizer(text):
  lem_text=[lemmatizer.lemmatize(i) for i in text]
  return lem_text
df['Description']=df['Description'].apply(lambda x: word_lemmentizer(x))
stemmer=PorterStemmer()
def word_stemmer(text):
  stem_text=" ".join([str(i) for i in text])
  return stem_text
df['Description']=df['Description'].apply(lambda x: word_stemmer(x))

#Clean Location
def clean_loc(text):
  if text.count(',')==2:
    e=text.find(',')
    text=text[e+1:]
    e=text.find(',')
    text=text[0:e]
  elif text.count(',')==1:
    e=text.find(',')
    text=text[0:e]
  text=text.strip()
  return text
df['Location']=df['Location'].apply(lambda x: clean_loc(x))
#File after cleaning decription andd have none salary
df.to_csv('cleanedandoidnaukri.csv')

