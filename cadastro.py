import json
import os
import random
import string
from datetime import datetime

DB_PATH = "database.json"


def carregar_dados():
    if not os.path.exists(DB_PATH) or os.path.getsize(DB_PATH) == 0:
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump({"alunos": [], "professores": []}, f, indent=4)
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_dados(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def gerar_ra():
    letras = "".join(random.choices(string.ascii_uppercase, k=3))
    numeros = "".join(random.choices(string.digits, k=3))
    return letras + numeros


def listar_cursos():
    return {
        1: "Análise e Desenvolvimento de Sistemas (ADS)",
        2: "Ciência da Computação",
        3: "Engenharia de Software",
        4: "Gestão da Tecnologia da Informação",
        5: "Segurança da Informação"
    }


def cadastrar_usuario():
    print("\n=== CADASTRO DE USUÁRIO ===")
    tipo = input("Tipo (aluno/professor): ").strip().lower()

    if tipo not in ["aluno", "professor"]:
        print("❌ Tipo inválido!\n")
        return

    nome = input("Nome completo: ").strip()
    senha = input("Crie uma senha: ").strip()
    ra = gerar_ra()

    data = carregar_dados()
    cursos_ti = listar_cursos()

    # ===== CADASTRO DE PROFESSOR =====
    if tipo == "professor":
        print("\n=== CADASTRO DE PROFESSOR ===")
        print("Selecione o curso em que você dá aula:")
        for i, curso in cursos_ti.items():
            print(f"{i} - {curso}")
        try:
            opc = int(input("Escolha o número do curso: "))
            curso_professor = cursos_ti.get(opc)
            if not curso_professor:
                print("❌ Opção inválida!\n")
                return
        except ValueError:
            print("❌ Digite apenas números.\n")
            return

        materia = input("Qual matéria você aplica nesse curso? ").strip()

        novo_professor = {
            "nome": nome,
            "ra": ra,
            "senha": senha,
            "curso": curso_professor,
            "materia": materia
        }
        data["professores"].append(novo_professor)

    # ===== CADASTRO DE ALUNO =====
    else:
        print("\n=== CADASTRO DE ALUNO ===")
        print("Selecione o curso que você está cursando:")
        for i, curso in cursos_ti.items():
            print(f"{i} - {curso}")
        try:
            opc = int(input("Escolha o número do curso: "))
            curso_aluno = cursos_ti.get(opc)
            if not curso_aluno:
                print("❌ Opção inválida!\n")
                return
        except ValueError:
            print("❌ Digite apenas números.\n")
            return

        print("\nQual é a modalidade do seu curso?")
        modalidades = {1: "Presencial", 2: "EAD", 3: "SemiPresencial"}
        for k, v in modalidades.items():
            print(f"{k} - {v}")
        try:
            m = int(input("Escolha a modalidade (número): "))
            modalidade = modalidades.get(m, "Presencial")
        except ValueError:
            modalidade = "Presencial"

        # ===== BOLSA =====
        tem_bolsa = input("Você possui bolsa? (s/n): ").strip().lower()
        bolsa_percent = 0
        codigo_bolsa = None
        if tem_bolsa == "s":
            try:
                bolsa_percent = float(
                    input("Qual porcentagem da bolsa? (ex: 40 para 40%): ").strip()
                )
                if bolsa_percent < 0 or bolsa_percent > 100:
                    bolsa_percent = 0
            except:
                bolsa_percent = 0

            # ===== CÓDIGO DA BOLSA =====
            while True:
                codigo_bolsa = input("Digite o código da bolsa (ex: A123): ").strip()
                if len(codigo_bolsa) == 4 and codigo_bolsa[0].isalpha() and codigo_bolsa[1:].isdigit():
                    break
                else:
                    print("❌ Código inválido! O formato deve ser 1 letra e 3 números (ex: A123).")

        novo_aluno = {
            "nome": nome,
            "ra": ra,
            "senha": senha,
            "curso": curso_aluno,
            "modalidade": modalidade,
            "bolsa_percent": bolsa_percent,
            "codigo_bolsa": codigo_bolsa,
            "notas": {},
            "surcharge": 0,
            "surcharge_month": None
        }

        data["alunos"].append(novo_aluno)

    salvar_dados(data)
    print(f"\n✅ {tipo.capitalize()} cadastrado com sucesso!")
    print(f"📘 Seu RA é: {ra}\n")
