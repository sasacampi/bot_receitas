import json
import logging
import os
from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def is_valid_json(variable):
    try:
        return json.loads(variable)
    except json.JSONDecodeError:
        return False


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/recipes')
def recipes():
    try:
        body = request.json
        if not body or 'ingredientes' not in body:
            logger.error({f'erro': 'Entrada inválida, por favor forneça uma lista de ingredientes.'})
            return jsonify({'erro': 'Entrada inválida, por favor forneça uma lista de ingredientes.'}), 400

        ingredients = ', '.join(body['ingredientes']).lower()
        logger.info(f"Ingredientes recebidos: {ingredients}.")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um chef de cozinha procurando inspiração."},
                {"role": "user", "content": f"Sugira até 2 receitas que contenham os seguintes ingredientes: {ingredients}. "
                                            f"Liste as receitas de forma completa no seguinte formato JSON, "
                                            f" incluindo todos os campos: "f"[{{'id': '1', 'nome': 'Nome da receita', "
                                            f" 'ingredientes_necessarios': ['nome': 'Nome do ingrediente', "
                                            f" 'quantidade': 'Peso ou Unidades'], "
                                            f" 'modo_de_preparo': 'Descrição do preparo', "
                                            f"'tempo_de_preparo': 'Tempo necessário', "
                                            f" 'tipo': 'Opções: Salgado, Doce, Agridoce'}}]"}
            ],
            n=2,
            temperature=0.3,
            max_tokens=1500
        )
        response = response.choices[0].message.content
        recipes_found = is_valid_json(response)

        if recipes_found:
            logger.info(f"Receitas encontradas com sucesso.")
            return jsonify(recipes_found), 200
        else:
            logger.info("Nenhuma receita encontrada para o(s) ingrediente(s) informado(s).")
            return jsonify({'mensagem': 'Nenhuma receita encontrada para o(s) ingrediente(s) informado(s).'}), 200

    except Exception as e:
        logger.error(f"Ocorreu um erro: {e}")
        return jsonify({'erro': 'Ocorreu um erro interno.'}), 500
