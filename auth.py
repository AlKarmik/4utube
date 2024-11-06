# auth.py
import google_auth_oauthlib.flow
import googleapiclient.discovery
import pickle

def authorize_youtube(scopes, client_secret_file='client_secret.json', credentials_file='credentials.pkl'):
    """
    Виконує авторизацію та зберігає облікові дані в файл.
    """
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secret_file, scopes)
    credentials = flow.run_local_server(port=0)
    
    # Збереження облікових даних у файл
    with open(credentials_file, 'wb') as cred_file:
        pickle.dump(credentials, cred_file)

    print(f"Файл {credentials_file} успішно створений.")
    
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

if __name__ == "__main__":
    scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]
    authorize_youtube(scopes)
