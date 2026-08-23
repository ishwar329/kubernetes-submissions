import json
import urllib.request
import urllib.error

WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/Special:Random"
BACKEND_URL = "http://todo-backend-svc:2345/todos"


def get_random_wikipedia_url():
    request = urllib.request.Request(
        WIKIPEDIA_URL,
        method="GET",
        headers={"User-Agent": "todo-cronjob/2.9"},
    )

    opener = urllib.request.build_opener(
        urllib.request.HTTPRedirectHandler()
    )

    try:
        response = opener.open(request)
        return response.geturl()
    except urllib.error.HTTPError as e:
        location = e.headers.get("Location")
        if location:
            return location
        raise


def create_todo(url):
    data = json.dumps({
        "content": f"Read {url}"
    }).encode()

    request = urllib.request.Request(
        BACKEND_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        print(response.read().decode(), flush=True)


if __name__ == "__main__":
    url = get_random_wikipedia_url()
    print(f"Random Wikipedia article: {url}", flush=True)
    create_todo(url)
