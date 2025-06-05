import requests
from google import genai


class GenAIClient:
    def __init__(self, api_key: str, context: str = ""):
        self.client = genai.Client(api_key=api_key)
        self.context = context

    def generate_content(self, user_input: str) -> str:
        prompt = f"{self.context}\nユーザー: {user_input}"
        response = self.client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )

        return response.text


class VoiceVoxClient:
    def __init__(self, api_url: str = "http://localhost:50021", api_key: str = ""):
        self.api_url = api_url
        self.api_key = api_key

    def generate_speech(
        self,
        text: str,
        speaker_id: int = 1,  # ずんだもん
        speed: float = 1.25,
    ) -> str:
        response: requests.Response = requests.post(
            url=f"{self.api_url}/audio",
            params={
                "text": text,
                "speaker": speaker_id,
                "speed": speed,
                "key": self.api_key,
            },
        )

        if response.status_code != 200:
            error_json = response.json()

            # エラーメッセージを取得
            # 参考：https://voicevox.su-shiki.com/su-shikiapis/
            error_massage = error_json["errorMessage"]

            if error_massage == "invalidApiKey":
                raise ValueError("VoiceVoxAPI Error：不正なAPIキーです。")
            elif error_massage == "failed":
                raise ValueError("VoiceVoxAPI Error：音声合成に失敗しました。")
            elif error_massage == "notEnoughPoints":
                raise ValueError("VoiceVoxAPI Error：ポイントが不足しています。")
            else:
                raise ValueError(f"VoiceVoxAPI Error：{error_massage}")

        return response.content
