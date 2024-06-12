import htpy as h
import datetime
from typing import List, Dict, Any


def head() -> h.Element:
    return h.head[
        h.title["kicknews"],
        h.meta(charset="UTF-8"),
        h.meta(name="viewport", content="width=device-width, initial-scale=1.0"),
        h.link(rel="icon", href="/static/img/kicknews_favicon.png"),
        h.link(rel="stylesheet", href="/static/css/simple.css"),
        h.link(rel="stylesheet", href="/static/css/custom.css"),
        h.script(src="/static/js/htmx.min.js")
    ]

def header() -> h.Element:
    return h.header[
        h.a(href="/")[
            h.img(src="/static/img/kicknews_logo.png")
        ]
    ]

def searchbar() -> h.Element:
    return h.div("#searchbar")[
        h.form(
            {
                'hx-post': "search",
                'hx-target': "#results_container",
                'hx-swap': "outerHTML",
                'hx-indicator': "#results_container"
            }
        )[
            h.input(
                "#input",
                type="text",
                name="searchbar",
                placeholder="The latest news about...",
            )
        ]
    ]

def topics(state) -> h.Element:
    return h.div(".topics")[
        [
            h.button(
                ".topic",
                hx_post="topic",
                hx_target="#results_container",
                hx_swap="outerHTML",
                hx_indicator="#results_container",
                name="topic",
                value=topic,
            )[topic] for topic in state['topics']
        ]
    ]

def result_div(result: Dict[str, Any]) -> h.Element:
    return h.div(".result_div")[
        [
            h.div(".title_div")[                
                h.a(href=result['url'])[
                    h.h4[result['title']]
                ],
                h.div(".date")[
                    result['date']
                ]
            ]
        ],
        h.p[
            result['text'] + "..."
        ]
    ]

def result_container(results: List[Dict[str, Any]]) -> h.Element:
    return h.div("#results_container")[
        h.div(".center")[
            h.img(
                ".htmx-indicator",
                src="/static/svg/circles.svg"
            )
        ],
        [result_div(result) for result in results],
    ]

def main(state: Dict[str, Any]) -> h.Element:
    return h.main[
        searchbar(),
        topics(state),
        result_container(results={})
    ]

def footer() -> h.Element:
    return h.footer[
        h.div[
            h.p["Copyright Kicknews ©" + datetime.datetime.now().strftime("%Y") + " "],
            h.a(href="https://github.com/1363V4/jinjaless")[
                h.img(
                    ".icons",
                    src="/static/svg/github-fill.svg"
                )
            ]
        ]
    ]

def body(state: Dict[str, Any]) -> h.Element:
    return h.body[
        header(),
        main(state),
        footer()
    ]

def home_page(state: Dict[str, Any]) -> h.Element:
    return h.html[
        head(),
        body(state),
    ]

def max_requests():
    return h.p[
        "You used all your requests.", 
        h.p[
            "Please upgrade to a ",
            h.a(href="https://www.youtube.com/watch?v=dQw4w9WgXcQ")["paid plan"],
            " to continue."
        ]
    ]

def snitch_page(data):
    return h.html[
        head(),
        [
            h.p[datum] for datum in data
        ]
    ]
