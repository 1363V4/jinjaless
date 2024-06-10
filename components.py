import htpy as h
import datetime


def head():
    return h.head[
        h.title["kicknews"],
        h.meta(charset="UTF-8"),
        h.meta(name="viewport", content="width=device-width, initial-scale=1.0"),
        h.link(rel="icon", href="/static/img/kicknews_favicon.png"),
        h.link(rel="stylesheet", href="/static/css/simple.css"),
        h.link(rel="stylesheet", href="/static/css/custom.css"),
        h.script(src="/static/js/htmx.min.js")
    ]

def header():
    return h.header[
        h.a(href="/")[
            h.img(src="/static/img/kicknews_logo.png")
        ]
    ]

def searchbar():
    return h.div("#searchbar")[
        h.form(
            {
                'hx-post': "search",
                'hx-target': "#results_container",
                'hx-swap': "outerHTML"
            }
        )[
            h.input(
                type="text",
                name="searchbar",
                placeholder="The latest news about...",
            )
        ]
    ]

def result_div(result):
    return h.div(".result_div")[
        h.a(href=result['url'])[
            h.h4[result['title']]
        ],
        h.p[
            result['text']
        ]
    ]

def result_container(results):
    return h.div("#results_container")[
        [result_div(result) for result in results]
    ]

def main(state):
    return h.main[
        searchbar(),
        h.div("#results_container")
    ]

def footer():
    return h.footer[
        "Copyright Kicknews ©" + datetime.datetime.now().strftime("%Y") + " ",
        h.a(href="https://github.com/1363V4/jinjaless")[
            h.img(
                ".icons",
                src="/static/svg/github-fill.svg"
            )
        ]
    ]

def body(state): 
    return h.body[
        header(),
        main(state),
        footer()
    ]

def home_page(state):
    return h.html[
        head(),
        body(state),
    ]
