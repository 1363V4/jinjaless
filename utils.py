import os
from dotenv import load_dotenv
from exa_py import Exa
from typing import List, Dict, Any
from datetime import datetime, timedelta

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

def get_results(input_value: str) -> List[Dict]:
    search = exa.search_and_contents(
        "The latest news about" + input_value,
        type="magic",
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
    return results
