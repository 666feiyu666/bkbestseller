import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import nltk

# 下载所需资源（只运行一次）
nltk.download('stopwords')

# 构建清洗后的停词表
def clean_stopwords(words):
    cleaned = [re.sub(r'[^a-z\s]', '', w.lower()) for w in words]
    return [w for w in cleaned if len(w) > 1]

raw_stopwords = stopwords.words('english') + [
    "book", "books", "read", "reading", "author", "publisher", "edition",
    "york", "times", "press", "bestselling", "bestseller", "bestsellers",
    "amazon", "amazoncom", "selling", "seller", "sellers", "top", "ten", "best",
    "also",
]
custom_stopwords = set(clean_stopwords(raw_stopwords))

def custom_tokenizer(text):
    return re.findall(r'\b[a-z]{2,}\b', text.lower())

def extract_keywords_with_phrases(text, top_n=20, ngram_range=(1, 3)):
    vectorizer = CountVectorizer(
        tokenizer=custom_tokenizer,
        token_pattern=None,
        stop_words=None,
        ngram_range=ngram_range
    )
    X = vectorizer.fit_transform([text])
    sum_words = X.sum(axis=0)

    # 构建词频表
    words_freq = [(word, int(sum_words[0, idx])) for word, idx in vectorizer.vocabulary_.items()]

    # 后期停词过滤（整词组）
    def is_valid_ngram(ngram):
        return all(w not in custom_stopwords for w in ngram.split())

    words_freq = [item for item in words_freq if is_valid_ngram(item[0])]
    words_freq.sort(key=lambda x: x[1], reverse=True)
    return words_freq[:top_n]


# 每年分析与保存
def analyze_year(year):
    input_path = f"data/top10desc/{year}.csv"
    output_path = f"output/wordanalysis/{year}_keywords.csv"

    df = pd.read_csv(input_path)
    text = ' '.join(df['description'].dropna().astype(str).tolist())
    keywords = extract_keywords_with_phrases(text)

    result_df = pd.DataFrame(keywords, columns=["word", "frequency"])
    result_df.to_csv(output_path, index=False)
    print(f"✅ {year} 完成，保存至 {output_path}")

# 批量分析所有年份
for year in range(1995, 2025):
    analyze_year(year)
