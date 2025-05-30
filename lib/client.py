from google import genai


class GenAIClient:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def generate_content(self, contents: str):
        response = self.client.models.generate_content(
            model="gemini-2.0-flash", contents=contents
        )

        return response.text
