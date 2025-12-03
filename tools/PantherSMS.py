import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Sample trained model for demo
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(["Congratulations! You won","Call me","Free entry","Hello friend"])
y = [1,0,1,0]  # 1=spam, 0=ham
model = MultinomialNB()
model.fit(X, y)

def run():
    text = input("Enter SMS text: ")
    vect = vectorizer.transform([text])
    pred = model.predict(vect)
    print("SPAM" if pred[0]==1 else "HAM")
