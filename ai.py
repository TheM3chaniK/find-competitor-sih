import os
from dotenv import load_dotenv

load_dotenv()
from groq import Groq


class AI:
    def __init__(self) -> None:
        with open("./prompt.txt", "r") as f:
            self.prompt_temp = f.read()

        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )

    def get_prdiction(self, content):
        completion = self.client.chat.completions.create(
            model="moonshotai/kimi-k2-instruct-0905",
            messages=[
                {
                    "role": "system",
                    "content": self.prompt_temp,
                },
                {"role": "user", "content": content},
            ],
            temperature=0.6,
            max_completion_tokens=4096,
            top_p=1,
            stream=True,
            stop=None,
        )

        ans = str()
        for chunk in completion:
            ans += chunk.choices[0].delta.content or ""
        return ans
