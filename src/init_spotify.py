from requests import post
import base64

ENCODING = 'utf-8'


def setup_request(client_secret: str, client_id: str):
    spotify_url = "https://accounts.spotify.com/api/token"
    b64_string = base64.b64encode(f"{client_id}:{client_secret}".encode(ENCODING))
    auth_string = str(b64_string, ENCODING)
    headers = {
        "Authorization": f"Basic {auth_string}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials"
    }
    return {
        'url': spotify_url,
        'headers': headers,
        'data': data
    }


def get_token(client_secret: str, client_id: str):
    token = None
    req = setup_request(client_secret, client_id)
    result = post(url=req['url'], headers=req['headers'], data=req['data'])
    if result.status_code != 200:
        print("[*] - Error while trying to authenticate with the Spotify API")
        exit()
    else:
        token = result.json()['access_token']
        print("[*] - Logged in to Spotify successfully.")
    return token
