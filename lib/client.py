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
