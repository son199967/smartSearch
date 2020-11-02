from flask import Flask
import math
import json
import numpy as np
import pymysql
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from vncorenlp import VnCoreNLP
from python_rdrsegmenter import load_segmenter
from flask import request

print("ajaha")
app = Flask(__name__)
segmenter = load_segmenter()

def tokenizer(sequence):
    return segmenter.tokenizer(sequence)
@app.route("/")
def hello():

    df = pd.read_csv('data.csv')
    # df.head()
    a = {'camera': 'camera', 'máy tính': "computer", 'cpu': "cpu", 'ghế': "desk", 'laptop': "laptop",
         'tai nghe': 'listen', "mainboard": "Mainboard",
         "chuột": "mouse", "máy in": "print", "ram": "ram", "màn hình": "screen", "tivi": "tivi", "usb": "usb",
         "vga": "VGA"}

    list = []
    query = request.args.get('search')
    print("sdjskjd"+query)
    m = query.split(" ")
    for i in m:
        if i in a:
            list.append(a[i])
    dfk = df[df['type'] == list[0]]
    segmenter = load_segmenter()
    dfk['discription'] = dfk['discription'].map(lambda x: segmenter.tokenizer(x.replace(":", " ")))
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(dfk['discription'].values.astype('U'))  # Store tf-idf representations of all docs
    query_vec = vectorizer.transform([segmenter.tokenizer(query.lower())])  # Ip -- (n_docs,x), Op -- (n_docs,n_Feats)
    results = cosine_similarity(X, query_vec).reshape((-1,))
    print(results.shape)
    print(results.max)
    ref = []
    for i in results.argsort()[-10:][::-1]:
        # print(i)
        ref.append(int(dfk.iloc[i, 0]))
        # print(i)
        # print(dfk.iloc[i, 0], "--", dfk.iloc[i, 1], "--", dfk.iloc[i, 2], dfk.iloc[i, 3])
    json_string = json.dumps(ref)
    return json_string





if __name__ == "__main__":
    app.run()