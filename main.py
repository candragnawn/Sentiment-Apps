from scrapper import NewsScraper
from preprocessor import DataCleaner
from transformers import pipeline

scrapper = NewsScraper()
cleaner = DataCleaner()


model_name = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
sentiment_analyser = pipeline("sentiment-analysis", model=model_name)

def run_project():
    keyword = input(" : ")
    print(f"mencari data terkait '{keyword}")
    raw_data = scrapper.fetch_news(keyword)
    print(f"menganalisis {len(raw_data)} berita\n")

    for item in raw_data:
        cleaned_text = cleaner.clean_text(item['title'])
        prediction = sentiment_analyser(cleaned_text)[0]

        print(f"berita: {item['title']}")
        print(f"sentimen: {prediction['label']} ({round(prediction['score']*100, 2)}%)")
        print("-" * 30)


if __name__ == "__main__":
    run_project()