import json
from datetime import datetime
import time
from utils import str_para_data, calcular_proxima_data



def carregar_tarefas(caminho="tarefas.json"):
    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    # converter ultima_data (string) → objeto date
    for tarefa in dados:
        tarefa["ultima_data"] = str_para_data(tarefa["ultima_data"])

    return dados


def calcular_status_tarefas(ultima_data, intervalo):
    proxima_data = calcular_proxima_data(ultima_data, intervalo)
    hoje = datetime.today().date()

    if proxima_data < hoje:
        status = "Atrasado"
    elif proxima_data == hoje:
        status = "Hoje"
    else:
        status = "OK"

    return {"status": status, "proxima_data": proxima_data}

def exibir_tarefas(tarefas):
    for tarefa in tarefas:
        resultado = calcular_status_tarefas(tarefa["ultima_data"], tarefa["intervalo_dias"])
        status = resultado["status"]
        proxima_data = resultado["proxima_data"].strftime("%Y-%m-%d")

        print(f"Tarefa: {tarefa['titulo']}")
        print(f"Próxima data: {proxima_data}")
        print(f"Status: {status}")
        print("-" * 20)
    input("Pressione Enter para continuar...")


def concluir_tarefa(tarefa):
    tarefa["ultima_data"] = datetime.today().date()
    return tarefa


def marcar_tarefa_como_concluida(nome, tarefas):
    for tarefa in tarefas:
        if tarefa["titulo"].lower() == nome.lower():
            concluir_tarefa(tarefa)
            return True
    return False


def atualizar_tarefas(tarefas, caminho="tarefas.json"):
    # converter ultima_data (objeto date) → string
    dados_atualizados = []
    for tarefa in tarefas:
        tarefa_copy = tarefa.copy()
        tarefa_copy["ultima_data"] = tarefa_copy["ultima_data"].strftime("%Y-%m-%d")
        dados_atualizados.append(tarefa_copy)

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados_atualizados, arquivo, indent=4, ensure_ascii=False)




# Programa (Menu)

while True:
    print("\n------------------------")
    print("Gerenciador de Tarefas")
    print("------------------------")

    try:
        opcao = int(input(" 1) Listar tarefas\n 2) Marcar tarefa como concluída\n 3) Ver concluídas hoje\n 4) Sair\n Escolha uma opção: "))
        print("------------------------")
    except ValueError:
        print("Digite apenas númenos de 1 a 4.")
        continue

    tarefas = carregar_tarefas()

    if opcao == 1:
        exibir_tarefas(tarefas)

    elif opcao == 2:
        nome_tarefa = input("Digite o nome da tarefa que você concluiu: \n")
        if marcar_tarefa_como_concluida(nome_tarefa, tarefas):
            atualizar_tarefas(tarefas)
            print(f"Tarefa '{nome_tarefa}' marcada como concluída.")
        else:
            print(f"Tarefa '{nome_tarefa}' não encontrada.")
        input("Pressione Enter para continuar...")

    elif opcao == 3:
        hoje = datetime.today().date()
        concluidas_hoje = [tarefa for tarefa in tarefas if tarefa["ultima_data"] == hoje]

        if concluidas_hoje:
            print("Tarefas concluídas hoje:")
            for tarefa in concluidas_hoje:
                print(f"- {tarefa['titulo']}")
        else:
            print("Nenhuma tarefa foi concluída hoje.")
        input("Pressione Enter para continuar...")

    elif opcao == 4:
        print("Saindo do gerenciador de tarefas.")
        time.sleep(1)
        break
    else:
        print("Opção inválida. Tente novamente.")
    