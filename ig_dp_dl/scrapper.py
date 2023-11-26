import json
import requests

from rich import print


def pretty_print_http_request(req: requests.models.PreparedRequest) -> None:
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.

    Reference: https://stackoverflow.com/a/23816211/19705722

    Args:
        req (requests.models.PreparedRequest): The request to print.
    """
    if "Host" not in req.headers:
        req.headers["Host"] = req.url.split("/")[2]

    path = req.url.split(req.headers["Host"])[-1]
    http_version = f"HTTP/1.1"

    print(
        "{}\n{}\r\n{}\r\n\r\n{}\n{}".format(
            "-----------START-----------",
            f"{req.method} {path} {http_version}",
            "\r\n".join("{}: {}".format(k, v) for k, v in req.headers.items()),
            req.body or "",
            "------------END------------",
        )
    )


def pretty_print_http_response(resp: requests.models.Response) -> None:
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.

    Args:
        resp (requests.models.Response): The response to print.
    """
    http_version = f"HTTP/{resp.raw.version // 10}.{resp.raw.version % 10}"

    try:
        response_body = json.dumps(json.loads(resp.text), indent=2)
    except json.decoder.JSONDecodeError:
        response_body = resp.text or resp.content.decode()

    print(
        "{}\n{}\r\n{}\r\n\r\n{}\n{}".format(
            "-----------START-----------",
            f"{http_version} {resp.status_code} {resp.reason}",
            "\r\n".join("{}: {}".format(k, v) for k, v in resp.headers.items()),
            "",
            "------------END------------",
        )
    )


def print_response_summary(response: requests.models.Response) -> None:
    """
    Print a summary of the response.

    Args:
        response (requests.models.Response): The response to print.
    """
    if response.history:
        print("[bold yellow]Request was redirected![/]")
        print("------ ORIGINAL REQUEST ------")
        pretty_print_http_request(response.history[0].request)
        print("------ ORIGINAL RESPONSE ------")
        pretty_print_http_response(response.history[0])
        print("------ REDIRECTED REQUEST ------")
        pretty_print_http_request(response.request)
        print("------ REDIRECTED RESPONSE ------")
        pretty_print_http_response(response)
    else:
        print("Request was not redirected")
        pretty_print_http_request(response.request)
        pretty_print_http_response(response)


def build_cookie(response: requests.models.Response) -> str:
    """
    Build cookie
    """
    return "; ".join([f"{key}={value}" for key, value in response.cookies.items()])


def send_request(username: str) -> None:
    """
    Send request

    Args:
        username (str): Username
    """
    url = "https://indown.io"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Dnt": "1",
        "Origin": "https://indown.io",
        "Referer": "https://indown.io/",
        "Sec-Ch-Ua": '"Chromium";v="118", "Brave";v="118", "Not=A?Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Brave Chrome/118.0.0.0 Safari/537.36",
    }
    payload = {
        "referer": "https://indown.io/download",
        "locale": "en",
        "_token": "QOZMjWdA6YMNVcrCVG7DNXMDQpYDpS1x48fs3xKN",
        "link": f"https://instagram.com/{username}",
    }

    with requests.Session() as session:
        response = session.get("https://indown.io")
        print_response_summary(response)
        cookie = build_cookie(response)

        print("------ COOKIES ------")
        print(cookie)
        print("------ END COOKIES ------")

        headers["Cookie"] = cookie

        response = session.post(url, headers=headers, data=payload)
        print_response_summary(response)

        # TODO: Fix error 405 Method Not Allowed
