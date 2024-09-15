import requests

class WhisperAPIClient:
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def transcribe(self, audio_file_path):
        url = f"{self.base_url}/audio/transcriptions"
        headers = self._get_headers()
        # files = {
        #     'file': open(audio_file_path, 'rb')
        # }
        if audio_file_path.startswith("http"):
            data = {
                "url": audio_file_path
            }
            response = requests.post(url, headers=headers, json=data)
        else:
            # multipart
            response = requests.post(url, headers=headers, files=files)
        return response.json()

# Usage
api_key = "sk-TWD6tbXtsmOhkq8YdId6gw"
custom_base_url = "https://gptapi.lilbillbiscuit.com/"

client = WhisperAPIClient(api_key, custom_base_url)
result = client.transcribe("https://hackmit2024.lilbillbiscuit.com/output_short.aac")

print(result)
