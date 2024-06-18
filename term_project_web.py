from flask import Flask, request, render_template_string, url_for
import torch
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast

app = Flask(__name__)

# 모델과 토크나이저 로드 경로
model_path = 'C:/project/nlptermproject/output6_full_300epoch'
# 또는 model_path = 'C:\\project\\nlptermproject\\output6_full_300epoch'

def load_model(model_path):
    model = GPT2LMHeadModel.from_pretrained(model_path)
    return model

def load_tokenizer(tokenizer_path):
    tokenizer = PreTrainedTokenizerFast.from_pretrained(tokenizer_path)
    return tokenizer

# 모델과 토크나이저를 미리 로드
model = load_model(model_path)
tokenizer = load_tokenizer(model_path)

def generate_text(sequence, max_length):
    ids = tokenizer.encode(f'{sequence}', return_tensors='pt')
    final_outputs = model.generate(
        ids,
        do_sample=True,
        max_length=max_length,
        pad_token_id=model.config.eos_token_id,
        top_k=30,
        top_p=0.95,
    )
    generated_text = tokenizer.decode(final_outputs[0], skip_special_tokens=True)
    
    first_bracket_index = generated_text.find('[')
    if first_bracket_index != -1:
        second_bracket_index = generated_text.find('[', first_bracket_index + 1)
        if second_bracket_index != -1:
            third_bracket_index = generated_text.find('[', second_bracket_index + 1)
            if third_bracket_index != -1:
                generated_text = generated_text[:third_bracket_index]

    return generated_text
@app.route('/')
def home():
    return render_template_string('''
        <!doctype html>
        <html lang="ko">
          <head>
            <meta charset="utf-8">
            <title>영화 줄거리 생성기</title>
            <style>
              body {
                font-family: Arial, sans-serif;
                background: url('{{ url_for('static', filename='images/e8a9a78da8a2c87f8ef25c28910afe0b.jpg') }}') no-repeat center center fixed;
                background-size: cover;
                color: #333;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
              }
              .container {
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background: rgba(255, 255, 255, 0.8);
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
              }
              h1 {
                color: #4CAF50;
              }
              label {
                display: block;
                margin: 15px 0 5px;
              }
              input[type="text"], input[type="number"] {
                width: 97%;
                padding: 10px;
                margin: 5px 0 20px;
                border: 1px solid #ccc;
                border-radius: 4px;
              }
              input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
              }
              input[type="submit"]:hover {
                background-color: #45a049;
              }
              .result {
                margin-top: 20px;
                padding: 10px;
                background-color: #e9ffe9;
                border: 1px solid #4CAF50;
                border-radius: 4px;
              }
            </style>
          </head>
          <body>
            <div class="container">
              <h1>영화 줄거리 생성기</h1>
              <form action="/generate" method="post">
                <label for="sequence">입력 텍스트:</label>
                <input type="text" id="sequence" name="sequence" value="[Q]">
                <label for="max_length">최대 길이:</label>
                <input type="number" id="max_length" name="max_length" value="80">
                <input type="submit" value="생성">
              </form>
              {% if generated_text %}
                <div class="result">
                  <h2>생성된 텍스트:</h2>
                  <p>{{ generated_text }}</p>
                </div>
              {% endif %}
            </div>
          </body>
        </html>
    ''')

@app.route('/generate', methods=['POST'])
def generate():
    sequence = request.form['sequence']
    max_length = int(request.form.get('max_length', 80))
    result = generate_text(sequence, max_length)
    return render_template_string('''
        <!doctype html>
        <html lang="ko">
          <head>
            <meta charset="utf-8">
            <title>영화 줄거리 생성기</title>
            <style>
              body {
                font-family: Arial, sans-serif;
                background: url('{{ url_for('static', filename='images/e8a9a78da8a2c87f8ef25c28910afe0b.jpg') }}') no-repeat center center fixed;
                background-size: cover;
                color: #333;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
              }
              .container {
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background: rgba(255, 255, 255, 0.8);
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
              }
              h1 {
                color: #4CAF50;
              }
              label {
                display: block;
                margin: 15px 0 5px;
              }
              input[type="text"], input[type="number"] {
                width: 97%;
                padding: 10px;
                margin: 5px 0 20px;
                border: 1px solid #ccc;
                border-radius: 4px;
              }
              input[type="submit"] {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer.
              }
              input[type="submit"]:hover {
                background-color: #45a049;
              }
              .result {
                margin-top: 20px;
                padding: 10px;
                background-color: #e9ffe9;
                border: 1px solid #4CAF50;
                border-radius: 4px;
              }
            </style>
          </head>
          <body>
            <div class="container">
              <h1>영화 줄거리 생성기</h1>
              <form action="/generate" method="post">
                <label for="sequence">입력 텍스트:</label>
                <input type="text" id="sequence" name="sequence" value="[Q]">
                <label for="max_length">최대 길이:</label>
                <input type="number" id="max_length" name="max_length" value="80">
                <input type="submit" value="생성">
              </form>
              <div class="result">
                <h2>생성된 텍스트:</h2>
                <p>{{ generated_text }}</p>
              </div>
            </div>
          </body>
        </html>
    ''', generated_text=result)

if __name__ == '__main__':
    app.run(debug=True)
