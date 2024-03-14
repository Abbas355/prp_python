from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# # Download NLTK resources and initialize stopwords
# nltk.download()
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

stop_words = stopwords.words("english")

def plagiarism_remover(word):
    synonyms = []
    if word in stop_words:
        return word
    if wordnet.synsets(word) == []:
        return word
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    pos_tag_word = nltk.pos_tag([word])
    pos = []
    for i in synonyms:
        pos.append(nltk.pos_tag([i]))
    final_synonyms = []
    for i in pos:
        if pos_tag_word[0][1] == i[0][1]:
            final_synonyms.append(i[0][0])
    final_synonyms = list(set(final_synonyms))
    if final_synonyms == []:
        return word
    if word.istitle():
        return random.choice(final_synonyms).title()
    else:
        return random.choice(final_synonyms)

@app.route('/', methods=['GET'])
def remove_plagiarism():
    pr_text = request.args.get('pr_text')
    if pr_text is not None:
        pr_text = pr_text.strip()
        para_split = word_tokenize(pr_text)
        final_text = []
        for i in para_split:
            final_text.append(plagiarism_remover(i))
        result_text = " ".join(final_text)
        response = {'result': result_text}
        
        # response = {'result': para_split}
    else:
        response = {'error': 'No "pr_text" parameter provided in the query string.'}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
