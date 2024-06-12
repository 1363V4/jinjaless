import os
from dotenv import load_dotenv
from exa_py import Exa
from typing import List, Dict, Any
from datetime import datetime, timedelta
from models import db, Search, News


load_dotenv()

exa = Exa(api_key=os.environ.get('EXA_API_KEY'))


def get_topics() -> Dict[str, Any]:
    return {
        'topics': [
            "biden",
            "nvidia",
            "israel",
            "french elections",
            "dofus",
            "age of empires"
        ]
    }

def save_results(input_value, results):
    search_entry = Search.create(search=input_value)
    for result in results:
        News.create(
            search=search_entry,
            title=result['title'],
            url=result['url'],
            text=result['text'],
            date=result['date'],
            saved_date=datetime.now(),
        )

def get_saved_results(input_value: str):
    search_entry = Search.get_or_none(Search.search == input_value)
    if search_entry:
        return [
            {
                'title': news.title,
                'url': news.url,
                'text': news.text,
                'date': news.date,
                'saved_date': news.saved_date,
            }
            for news in search_entry.news
        ]
    return None

def get_results(input_value: str) -> List[Dict]:
    saved_results = get_saved_results(input_value)
    if saved_results:
        return saved_results

    search = exa.search_and_contents(
        "The latest news about" + input_value,
        type="neural",
        use_autoprompt=True,
        num_results=3,
        text={
            "max_characters": 200
        },
        category="news",
        start_published_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
        end_published_date = datetime.now().strftime('%Y-%m-%d')
    ).results
    results = [
        {
            'title': search_result.title,
            'url': search_result.url,
            'text': search_result.text,
            'date': search_result.published_date if search_result.published_date else "fresh",
        }
        for search_result in search
    ]
    save_results(input_value, results)
    return results

def clean_db():
    cutoff_time = datetime.now() - timedelta(hours=24)
    News.delete().where(News.saved_date < cutoff_time).execute()
