from flask import Flask, request, render_template
import pandas as pd
import pickle
import os

app = Flask(__name__, template_folder="../templates")  # Point to MovieRecommendationSystem/templates/

# Load precomputed similarity matrix and data
with open(r'C:\Users\vijay\OneDrive\Desktop\MovieRecommendationSystem\dataset\similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)
imdb_data = pd.read_csv(r'C:\Users\vijay\OneDrive\Desktop\MovieRecommendationSystem\dataset\cleaned_imdb_data.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie = request.form['movie']
    try:
        idx = imdb_data[imdb_data['primaryTitle'] == movie].index[0]
        distances = similarity[idx]
        movie_indices = distances.argsort()[::-1][1:6]
        recommendations = imdb_data.iloc[movie_indices]['primaryTitle'].tolist()
        return render_template('recommendations.html', recommendations=recommendations)
    except:
        return render_template('recommendations.html', recommendations=["Movie not found!"])

if __name__ == '__main__':
    app.run(debug=True)