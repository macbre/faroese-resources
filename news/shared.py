import requests

_http_client = None

def get_http_client() -> requests.Session:
    """
    https://requests.readthedocs.io/en/latest/user/advanced/
    """
    global _http_client

    if _http_client is None:
        _http_client = requests.Session()
        _http_client.headers.update({'user-agent': 'faroese-resource/python'})

    return _http_client
