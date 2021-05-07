from flask import Flask, request, render_template 
import pickle
import indexer

stopwords = []
stopwords_file = 'stopwords.txt'
with open(stopwords_file, 'r') as f:
    stopwords = f.read().split('\n')
    stopwords.pop(-1)   #pop last ''(empty) element

with open("inverted_index.txt", "rb") as fp:   # Unpickling
    inverted_index = pickle.load(fp)
with open("document_lengths.txt", "rb") as fp:   # Unpickling
    document_lengths = pickle.load(fp)
with open("num_docs.txt", "rb") as fp:   # Unpickling
    num_docs = pickle.load(fp)

# Flask constructor
app = Flask(__name__)   
  
# A decorator used to tell the application
# which URL is associated function
@app.route('/', methods =["GET", "POST"])
def gfg():
    if request.method == "POST":
       # getting input with name = fname in HTML form
       query = request.form.get("query")
       processed_queries = indexer.preprocess_query_(stopwords,[query])
       similarity_table = indexer.calc_similarity_table(processed_queries[0], 
                                         inverted_index, document_lengths, 
                                         num_docs)
       st = sorted(similarity_table.items(), key=lambda kv: kv[1], reverse=True)
       st10 = st[0:20]
       # getting input with name = lname in HTML form 
       questions = ['http://vfvc.uic.edu','http://vfvc.uic.edu','http://vfvc.uic.edu']
       return render_template("results.html", questions=st10)
    return render_template("form.html")
  
if __name__=='__main__':
   app.run()
