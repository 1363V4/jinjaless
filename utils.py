import os
from dotenv import load_dotenv
from exa_py import Exa
from typing import List, Dict

load_dotenv()

exa = Exa(api_key=os.environ.get('EXA_API_KEY'))


def get_results(input_value: str) -> List[Dict]:
    search = exa.search_and_contents(
        "The latest news about" + input_value,
        type="magic",
        use_autoprompt=True,
        num_results=3,
        text={
            "max_characters": 200
        },
        category="news"
    ).results
    results = [
        {
            'title': search_result.title,
            'url': search_result.url,
            'text': search_result.text,
        }
        for search_result in search
    ]
    return results
