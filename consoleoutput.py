from newsapi import NewsApiClient
import json
import requests

api = NewsApiClient(api_key='0233006c7dc448ffaffea5cdfd337976')

top_headlines = api.get_top_headlines(sources='die-zeit', language='de')

#print(json.dumps(top_headlines, indent=4))

#Attempt to retrieve number of articles from JSON data dump
#For this case, It should be 10

print(top_headlines['totalResults'])



#sources = api.get_sources

#print(sources)

articles = top_headlines['articles']

results = []

for ar in articles:
    results.append(ar['title'])

for i in range (len(results)):
    print(i + 1, results[i])