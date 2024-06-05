import htpy as h

def header():
    return h.head[
        h.title["hello world"],
        h.meta(charset="UTF-8"),
        h.meta(name="viewport", content="width=device-width, initial-scale=1.0"),
        h.link(rel="stylesheet", href="/static/css/simple.min.css"),
        h.script(src="/static/js/htmx.min.js")
    ]

def home_page():
    return h.html[
        header(),
        "hello world"
    ]
