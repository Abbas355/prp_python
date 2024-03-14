from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import random

app = FastAPI()

# Download NLTK resources
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Initialize stopwords
stop_words = stopwords.words("english")

# Function to remove plagiarism
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

# Define request body model
class TextRequest(BaseModel):
    pr_text: str

# REST API endpoint
@app.post("/remove_plagiarism")
async def remove_plagiarism(request: TextRequest):
    pr_text = request.pr_text
    if pr_text is not None:
        pr_text = pr_text.strip()
        para_split = word_tokenize(pr_text)
        final_text = []
        for i in para_split:
            final_text.append(plagiarism_remover(i))
        result_text = " ".join(final_text)
        return {"result": result_text}
    else:
        raise HTTPException(status_code=400, detail="No text provided.")
