from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import re

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('reviews.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def analyze_sentiment(text):
    text_lower = text.lower()
    
    # Позитивные слова
    positive_words = [
        'хорош', 'отлично', 'прекрасно', 'замечательно', 'великолепно',
        'нравится', 'люблю', 'супер', 'круто', 'классно', 'восхитительно',
        'потрясающе', 'превосходно', 'удивительно', 'фантастически',
        'радует', 'довольн', 'счастлив', 'восторг', 'идеально'
    ]
    
    # Негативные слова
    negative_words = [
        'плохо', 'ужасно', 'отвратительно', 'кошмар', 'жуткий',
        'ненавижу', 'отстой', 'гадость', 'позор', 'безобразие',
        'расстроен', 'разочарован', 'злой', 'недоволен', 'проблем',
        'ошибк', 'сломан', 'не работает', 'баг', 'глюк'
    ]
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    else:
        return 'neutral'

@app.route('/reviews', methods=['POST'])
def create_review():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Поле text обязательно'}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({'error': 'Текст отзыва не может быть пустым'}), 400
        
        # Анализ настроения
        sentiment = analyze_sentiment(text)
        
        # Сохранение в БД
        created_at = datetime.utcnow().isoformat()
        
        conn = sqlite3.connect('reviews.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)',
            (text, sentiment, created_at)
        )
        review_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'id': review_id,
            'text': text,
            'sentiment': sentiment,
            'created_at': created_at
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500

@app.route('/reviews', methods=['GET'])
def get_reviews():
    try:
        sentiment_filter = request.args.get('sentiment')
        
        conn = sqlite3.connect('reviews.db')
        cursor = conn.cursor()
        
        if sentiment_filter:
            if sentiment_filter not in ['positive', 'negative', 'neutral']:
                return jsonify({'error': 'Неверное значение sentiment'}), 400
            
            cursor.execute(
                'SELECT id, text, sentiment, created_at FROM reviews WHERE sentiment = ? ORDER BY created_at DESC',
                (sentiment_filter,)
            )
        else:
            cursor.execute(
                'SELECT id, text, sentiment, created_at FROM reviews ORDER BY created_at DESC'
            )
        
        reviews = []
        for row in cursor.fetchall():
            reviews.append({
                'id': row[0],
                'text': row[1],
                'sentiment': row[2],
                'created_at': row[3]
            })
        
        conn.close()
        
        return jsonify(reviews), 200
        
    except Exception as e:
        return jsonify({'error': 'Внутренняя ошибка сервера'}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)