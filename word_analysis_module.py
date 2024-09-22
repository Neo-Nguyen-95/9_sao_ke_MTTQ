#%% LIBRARY
from collections import Counter
from nltk import ngrams
from data_module import data_module
import seaborn as sns
from datetime import datetime

#%% FIND MOST FREQUENT N-GRAMS
def find_frequent_ngrams(paragraph, n):
    words = paragraph.split()
    
    n_grams = ngrams(words, n)
    
    ngrams_counts = Counter(n_grams)
    
    most_comment_ngrams =  ngrams_counts.most_common(30)
    
    return most_comment_ngrams

#%% N-GRAM ANALYSIS WITH RESULT
def ngram_analysis(df, item_col):  
    text = ''
    for words in df[item_col].values:
        text += ' ' + words
    
    # print(text[:100])
    
    most_frequent_2_grams = find_frequent_ngrams(text, 2)
    print('\nMost frequent bi-gram are:')
    for g in most_frequent_2_grams:
        print(g[0][0], g[0][1])
    
    most_frequent_3_grams = find_frequent_ngrams(text, 3)
    print('\nMost frequent tri-gram are:')
    for g in most_frequent_3_grams:
        print(g[0][0], g[0][1], g[0][2])
        
#%% TEST SITE
dataObject = data_module()
df = dataObject.load_data()

df['content_length'] = df['content'].apply(lambda row: len(row.split(' ')))

# sns.histplot(df, x='content_length')

ngram_analysis(df[df['content_length']>20], 'content')

df[df['content_length']>22]['content'].values

#%%
filter_date = datetime(2024,9,12).date()
df_before = df[df['date'] <= filter_date]
df_after = df[df['date'] > filter_date]

df_before['content_length'] = df_before['content'].apply(lambda row: len(row.split(' ')))
df_after['content_length'] = df_after['content'].apply(lambda row: len(row.split(' ')))

sns.histplot(df_before, x='content_length')
sns.histplot(df_after, x='content_length')

df_before['content_length'].describe()
df_after['content_length'].describe()
