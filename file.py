import pandas as pd
import math
import openpyxl
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

######################
#what job you want to search for
matchers = ['Application Developer Specialist IT','Application Operation Specialist','Data Analyst']

#insert path   ,   file_name.xlsx
xlsx_file = Path('C:/Users/NiklasWernich/OneDrive - Diadrom Holding AB/Dokument', 'AL_AB_Volvo_Postings.xlsx')
df = pd.read_excel(xlsx_file, index_col=0)
#print(df)
df.columns = df.iloc[0]
#remove first row from DataFrame
df = df[1:]

#view updated DataFrame
df['Job Posting Submit Date'] = pd.to_datetime(df['Job Posting Submit Date'])
df = df.set_index(df['Job Posting Submit Date'])
df = df.sort_index()
#print(df)
df = df.dropna()
# Printing dataframe
#print(df)
#distinct titles only
df_dist = df.drop_duplicates(subset = ['Title'])
#print(df_dist)
#new column with year
df['year'] = df['Job Posting Submit Date'].dt.year
#print(df)

df_freq = df.pivot_table(index = ['Title'], columns=['year'], aggfunc ='size')
df_freq = df_freq.fillna(0)
#print(df_freq)

index_list = df_freq.index.values.tolist()

#this in the beginning
#matchers = ['Application Developer Specialist IT','Application Operation Specialist']
#indices
for k in matchers:
    indices = [i for i, s in enumerate(index_list) if k in s]
    test = df_freq.iloc[indices].sum()
    fig, axes = plt.subplots(nrows=1, ncols=2)
    fig.suptitle(k)
    test.plot(ax=axes[0], kind = 'bar')
    df_freq.iloc[indices].plot(ax=axes[1], kind='bar')
    #plt.title(k)
plt.show()


#############################################



#############################################
words=["embedded","GIT", "Python", "REST", "C++", "Java", "Azure", "C/","C ","C.", "Linux", "SQL", "Matlab", "Jenkins", "Jira","Simulink","Kubernetes", "AWS","AUTOSAR","javascript",".net","CI","Android","Openshift","Iso26262","Angular","C#","Spring","React","Cybersecurity","Kotlin","Power BI","Node.js","YOCTO","Hibernate","CAN","LIN","Ethernet"]

#count words
description_list = df["Description"].values.tolist()
leng=[]
for k in words:
    count = [i for i, s in enumerate(description_list) if k in s]
    leng.append(len(count))
word_freq=pd.DataFrame(leng,index=[words],columns=['freq'])
word_freq.plot(kind='bar')
plt.show()

word_year_freq = df.pivot_table(index = [words], columns=['year'], aggfunc ='size')
word_year_freq = df_freq.fillna(0)
print(word_year_freq)