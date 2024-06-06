import htpy as h

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
    return h.div[
        h.img(src="/static/img/kicknews_logo.png")
    ]

def searchbar():
    return h.form(
        {
            'hx-post': "search",
            'hx-target': "#results_container",
            'hx-swap': "outerHTML"
        }
    )[
        h.input(
            type="text",
            name="searchfield",
            placeholder="Search Kickstarter projects about...",
            maxlength="50",
            min="0",
        )
    ]

def result_div(result):
    return h.div[
        h.a(href=result['url'])[
            h.h3[result['title']]
        ],
        h.p[
            result['text']
        ]
    ]

def result_container(results):
    return h.div("#results_container")[
        [result_div(result) for result in results]
    ]

def main(context):
    return [
        searchbar(),
        h.div("#results_container")
    ]

def footer():
    import datetime
    return h.p["Copyright ©" + datetime.datetime.now().strftime("%Y")]

def body(context): 
    return h.body[
        header(),
        main(context),
        footer()
    ]

def home_page(context):
    return h.html[
        head(),
        body(context),
    ]
