import os
from dotenv import load_dotenv
from exa_py import Exa
from datetime import datetime, timedelta
import redis
import json

load_dotenv()

exa = Exa(api_key=os.environ.get('EXA_API_KEY'))
redis_url = os.environ.get('REDIS_URL')
redis_client = redis.from_url(redis_url)

def get_topics():
    return {
        'topics': [
            "biden",
            "nvidia",
            "israel",
            "french elections",
            "dofus",
            "age of empires",
        ]
    }

def save_results(input_value, results):
    redis_client.lpush(input_value, json.dumps(results))

def get_saved_results(input_value):
    saved_results = redis_client.lrange(input_value, 0, -1)
    if saved_results:
        return json.loads(saved_results)
    return None

def get_results(input_value):
    saved_results = get_saved_results(input_value)
    if saved_results:
        return saved_results

    search = exa.search_and_contents(
        f"Give me the latest news about {input_value}. Only consider news sites and blog posts.",
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

def get_searches():
    return [key.decode('utf-8') + "___" + redis_client.hget(key, "saved_date").decode('utf-8') for key in redis_client.keys()]

def clean_db() -> None:
    redis_client.flushdb()