from transformers import pipeline
import glob
import os

summarizer = pipeline("summarization", model="plguillou/t5-base-fr-sum-cnndm")

summaries = []
for file in text_files_list:
    content = open(file, 'r').read()
    summary = summarizer(content)
    summaries.append(summary[0]['summary_text'])
    
    print(summary)

final_summary = ' '.join(summaries)

with open('summary.txt', 'w') as f:
    f.write(final_summary)
    f.close()