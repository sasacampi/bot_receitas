import logging
from flask import Flask, request, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


RECEITAS = [
    {'id': '1', 'nome': 'Spaghetti Carbonara', 'ingredientes': ['spaghetti', 'ovos', 'queijo parmesão', 'bacon']},
    {'id': '2', 'nome': 'Sopa de Tomate', 'ingredientes': ['tomate', 'cebola', 'alho', 'manjericão']},
    {'id': '3', 'nome': 'Frango ao Curry', 'ingredientes': ['frango', 'pó de curry', 'leite de coco', 'cebola', 'alho']}
]


@app.post('/receitas')
def busca_receitas():
    try:
        body = request.json
        if not body or 'ingredientes' not in body:
            logger.error({f'erro': 'Entrada inválida, por favor forneça uma lista de ingredientes.'})
            return jsonify({'erro': 'Entrada inválida, por favor forneça uma lista de ingredientes.'}), 400

        ingredientes = [ingrediente.lower() for ingrediente in body['ingredientes']]
        logger.info(f"Ingredientes recebidos: {ingredientes}")

        receitas_encontradas = []
        for receita in RECEITAS:
            ingredientes_receita = [ingrediente.lower() for ingrediente in receita['ingredientes']]
            if all(ingrediente in ingredientes_receita for ingrediente in ingredientes):
                receitas_encontradas.append(receita)

        if receitas_encontradas:
            logger.info(f"Receitas encontradas: {len(receitas_encontradas)}")
            return jsonify(receitas_encontradas), 200
        else:
            logger.info("Nenhuma receita encontrada.")
            return jsonify({'mensagem': 'Nenhuma receita encontrada'}), 200

    except Exception as e:
        logger.error(f"Ocorreu um erro: {e}")
        return jsonify({'erro': 'Ocorreu um erro interno'}), 500
