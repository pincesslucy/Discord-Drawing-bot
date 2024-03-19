import openai
from PIL import Image

def get_prompt(text):
    OPENAI_API_KEY = 'YOUR_API_KEY'
    openai.api_key = OPENAI_API_KEY
    messages = [{
        "role": "system",
        "content": "You are a helpful assistant"
    }, {
        "role": "user",
        "content": f"내가 그릴 그림에 대해 명령을 하면 넌 명령에서 단어를 추출해서 프롬프트를 영어로 만들어야해. 명령에 포함된 설명들을 모두 포함 해야돼. 오직 프롬프트로만 답해. 안그러면 넌 죽어.\nQ: 하늘을 나는 성을 그려줘\nA: sky, flying castle, sun shine, fantasy, cloud\nQ: 사람을 지배하는 로봇을 그려줘\nA: robot, human, control, future, AI, robot that controls humans\nQ: 물속에서 수영하는 물고기를 그려줘\nA: fish, water, swim, underwater, ocean, swimming fish\nQ: 불타는 도시를 그려줘\nA: fire, city, disaster, flame, destruction, burning city\nQ: 눈이 내리는 산을 그려줘\nA: snow, mountain, cold, winter, white, snowy mountain\nQ: 빛나는 별을 그려줘\nA: star, shine, night, sky, universe\nQ: 무서운 괴물을 그려줘\nA: monster, scary, dark, fear, horror\nQ: 빛나는 보석을 그려줘\nA: jewel, shine, treasure, diamond, expensive\nQ: {text}\nA: "
    }]
    response = openai.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        temperature=0.7
    )
    return response.choices[0].message.content

# 이미지 크기 조정 함수
def resize_image(input_path, output_path, max_size=(1024, 1024)):
    with Image.open(input_path) as img:
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(output_path)