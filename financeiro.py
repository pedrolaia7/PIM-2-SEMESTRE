import json
import os
from datetime import datetime

DB_PATH = "database.json"

COURSE_FEES = {
    "Análise e Desenvolvimento de Sistemas (ADS)": 470.0,
    "Engenharia de Software": 720.0,
    "Ciência da Computação": 630.0,
    "Gestão da Tecnologia da Informação": 590.0,
    "Segurança da Informação": 530.0
}

MONTHS = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}


def carregar_dados():
    if not os.path.exists(DB_PATH):
        return {"alunos": [], "professores": []}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_dados(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def calcular_mensalidade(aluno, month_number=None):
    curso = aluno.get("curso")
    base = COURSE_FEES.get(curso, 0.0)
    bolsa = float(aluno.get("bolsa_percent", 0) or 0)
    valor_com_bolsa = base * (1 - bolsa / 100.0)

    surcharge = 0.0
    if month_number is None:
        month_number = datetime.now().month

    # adiciona R$100 se o aluno ficou de DP e o surcharge for desse mês
    surcharge_month = aluno.get("surcharge_month")
    if surcharge_month == month_number:
        surcharge = float(aluno.get("surcharge", 0) or 0)

    total = round(valor_com_bolsa + surcharge, 2)
    return {
        "base": base,
        "bolsa_percent": bolsa,
        "codigo_bolsa": aluno.get("codigo_bolsa"),
        "valor_com_bolsa": round(valor_com_bolsa, 2),
        "surcharge": surcharge,
        "total": total
    }


def menu_financeiro(aluno):
    while True:
        print("\n=== MENU FINANCEIRO ===")
        print("1 - Ver mensalidade do mês atual")
        print("2 - Ver mensalidade de um mês específico")
        print("3 - Listar todos os meses (Janeiro a Dezembro)")
        print("4 - Voltar")

        opc = input("Escolha: ").strip()
        if opc == "1":
            cur = datetime.now().month
            mostrar_mes(aluno, cur)
        elif opc == "2":
            try:
                m = int(input("Digite o número do mês (1-12): ").strip())
                if 1 <= m <= 12:
                    mostrar_mes(aluno, m)
                else:
                    print("❌ Mês inválido.")
            except:
                print("❌ Entrada inválida.")
        elif opc == "3":
            for m in range(1, 13):
                mostrar_mes(aluno, m, quiet=True)
            print("")
        elif opc == "4":
            break
        else:
            print("❌ Opção inválida.\n")


def mostrar_mes(aluno, month_number, quiet=False):
    info = calcular_mensalidade(aluno, month_number)
    mes_nome = MONTHS.get(month_number, f"Mês {month_number}")

    bolsa_info = ""
    if info["bolsa_percent"] > 0:
        codigo = info.get("codigo_bolsa", "N/A")
        bolsa_info = f" | Bolsa {info['bolsa_percent']}% (Código: {codigo})"

    line = f"{mes_nome}: Base R${info['base']:.2f}{bolsa_info} => R${info['valor_com_bolsa']:.2f}"
    if info["surcharge"] > 0:
        line += f" | + DP R${info['surcharge']:.2f}"
    line += f" | TOTAL: R${info['total']:.2f}"

    if quiet:
        print(line)
    else:
        print("\n" + line + "\n")
