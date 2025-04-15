from dataclasses import dataclass
import requests

from src.settings import Settings

import datetime

@dataclass
class GoogleClient:
    settings: Settings
    
    def get_user_info(self, auth_code: str) -> dict:
        access_token = self.get_user_access_token(auth_code)
        response = requests.get(
            self.settings.google_user_info_url, 
            headers={ "Authorization": f"Bearer {access_token}" }
        )
        return response.json()
    
    def get_user_access_token(self, auth_code: str) -> dict:
        data = {
            "code": auth_code,
            "client_id": self.settings.google_client_id,
            "client_secret": self.settings.google_client_secret,
            "redirect_uri": self.settings.google_redirect_uri,
            "grant_type": "authorization_code"
        }
        response = requests.post(self.settings.google_token_url, data)
        return response.json()['access_token']
