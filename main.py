import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# [보안] Render 환경 변수에서 키를 가져옵니다.
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    print("CRITICAL ERROR: GEMINI_API_KEY is missing!")

@app.route('/')
def home():
    return "AI Novelist Server is Running!"

@app.route('/generate-novel', methods=['POST'])
def generate_novel():
    try:
        data = request.json
        subject = data.get('subject', '미정')
        
        # [핵심 수정] 따옴표 3개를 쓰면 아래처럼 여러 줄로 써도 에러가 절대 나지 않습니다.
        prompt = f"""당신은 노벨 문학상 후보에 오를 법한 모든 분야에 통달한 천재 현대 소설가입니다. 
다음 주제를 바탕으로 깊이 있는 은유와 세밀한 묘사가 담긴 짧은 소설을 작성하세요.
주제: {subject}"""
        
        response = model.generate_content(prompt)
        return jsonify({"novel": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render의 포트 설정
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port))


