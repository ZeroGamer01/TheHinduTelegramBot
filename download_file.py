import requests


def download_file_from_google_drive(download_file_id, dest):
    URL = "https://www.newspaperpdf.online/download-the-hindu-adfree.php"
    session = requests.Session()
    response = session.get(URL, params={'id': download_file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': download_file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, dest)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)

