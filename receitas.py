import requests

class BotReceitas:
    def __init__(self, api_url):
        self.api_url = api_url
    
    def buscar_receitas_por_ingredientes(self, ingredientes):
        url = f"{self.api_url}/todas"
        response = requests.get(url)
        if response.status_code == 200:
            receitas = response.json()
            receitas_compatíveis = []
            for receita in receitas:
                if all(ingrediente in receita["ingredientes"].lower() for ingrediente in ingredientes):
                    receitas_compatíveis.append(receita)
            return receitas_compatíveis
        else:
            return None
    
    def obter_modo_preparo(self, id_receita):
        url = f"{self.api_url}/{id_receita}"
        response = requests.get(url)
        if response.status_code == 200:
            receita = response.json()
            return receita.get("modo_preparo", "Modo de preparo não disponível")
        else:
            return "Receita não encontrada."

api_url = "https://gold-anemone-wig.cyclic.app/receitas"
bot = BotReceitas(api_url)

while True:
    ingredientes_disponiveis = input("Digite os ingredientes disponíveis separados por vírgula (ou 'sair' para encerrar): ")
    if ingredientes_disponiveis.lower() == 'sair':
        break
    
    receitas_compatíveis = bot.buscar_receitas_por_ingredientes(ingredientes_disponiveis.split(','))
    
    if receitas_compatíveis:
        print("Receitas sugeridas:")
        for i, receita in enumerate(receitas_compatíveis, 1):
            nome = receita.get("receita", "Nome da receita não disponível")
            print(f"{i}. {nome}")
        
        escolha = input("Escolha o número da receita para ver o modo de preparo (ou 'sair' para voltar): ")
        if escolha.lower() == 'sair':
            continue
        
        try:
            indice_receita = int(escolha) - 1
            id_receita = receitas_compatíveis[indice_receita].get("id")
            modo_preparo = bot.obter_modo_preparo(id_receita)
            print(f"Modo de preparo da receita selecionada:\n{modo_preparo}")
        except (ValueError, IndexError):
            print("Escolha inválida. Por favor, escolha um número válido.")
    else:
        print("Não foi possível encontrar receitas compatíveis com os ingredientes fornecidos.")
