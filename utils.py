import os
from exa_py import Exa
from typing import List, Dict

exa = Exa(api_key=os.environ.get('EXA_API_KEY'))


def get_results(input_value: str) -> List[Dict]:
    search = exa.search_and_contents(
        "sandwich maker",
        type="neural",
        use_autoprompt=True,
        num_results=10,
        include_domains=["https://www.kickstarter.com/"],
        text={
            "max_characters": 50
        }
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
