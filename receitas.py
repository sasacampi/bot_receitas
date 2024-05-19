import json
import logging
import os
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=OPENAI_API_KEY)


@app.post('/receitas')
def busca_receitas():
    try:
        body = request.json
        if not body or 'ingredientes' not in body:
            logger.error({f'erro': 'Entrada inválida, por favor forneça uma lista de ingredientes.'})
            return jsonify({'erro': 'Entrada inválida, por favor forneça uma lista de ingredientes.'}), 400

        ingredientes = ', '.join(body['ingredientes']).lower()
        logger.info(f"Ingredientes recebidos: {ingredientes}")

        completion_text = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um chef de cozinha procurando inspiração."},
                {"role": "user", "content": f"Sugira receitas que contenham os seguintes ingredientes: {ingredientes}. "
                                            f"Liste as receitas de forma completa no seguinte formato JSON, "
                                            f" incluindo todos os campos: "f"[{{'id': '1', 'nome': 'Nome da receita', "
                                            f" 'ingredientes_necessarios': ['nome': 'Nome do ingrediente', "
                                            f" 'quantidade': 'Peso ou Unidades'], "
                                            f" 'modo_de_preparo': 'Descrição do preparo', "
                                            f"'tempo_de_preparo': 'Tempo necessário', "
                                            f" 'tipo': 'Opções: Salgado, Doce, Agridoce'}}]"}
            ]
        )
        completion_text = completion_text.choices[0].message.content
        logger.info(completion_text)

        receitas_encontradas = json.loads(completion_text)
        logger.info(receitas_encontradas)

        if receitas_encontradas:
            logger.info(f"Receitas encontradas: {len(receitas_encontradas)}")
            return jsonify(receitas_encontradas), 200
        else:
            logger.info("Nenhuma receita encontrada.")
            return jsonify({'mensagem': 'Nenhuma receita encontrada'}), 200

    except Exception as e:
        logger.error(f"Ocorreu um erro: {e}")
        return jsonify({'erro': 'Ocorreu um erro interno'}), 500
