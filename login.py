import json
import os
import cursos
import professores

DB_PATH = "database.json"


def carregar_dados():
    if not os.path.exists(DB_PATH):
        return {"alunos": [], "professores": []}
    with open(DB_PATH, "r") as f:
        return json.load(f)


def login():
    print("\n=== LOGIN NO SISTEMA ===")
    ra = input("RA: ").strip().upper()
    senha = input("Senha: ").strip()

    data = carregar_dados()

    # Aluno
    for aluno in data.get("alunos", []):
        if aluno["ra"] == ra and aluno["senha"] == senha:
            print(f"\n✅ Bem-vindo(a), {aluno['nome']} (Aluno)\n")
            cursos.menu_cursos(aluno)
            return "aluno", aluno

    # Professor
    for prof in data.get("professores", []):
        if prof["ra"] == ra and prof["senha"] == senha:
            print(f"\n✅ Bem-vindo(a), {prof['nome']} (Professor de {prof['materia']})\n")
            professores.menu_professor(prof)
            return "professor", prof

    print("❌ RA ou senha incorretos.\n")
    return None, None
