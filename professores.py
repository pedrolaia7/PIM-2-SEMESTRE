# professores.py
import json
import os
from datetime import datetime, timedelta

DB_PATH = "database.json"

def carregar_dados():
    if not os.path.exists(DB_PATH):
        return {"alunos": [], "professores": []}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_dados(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def menu_professor(professor):
    while True:
        print("\n=== MENU DO PROFESSOR ===")
        print(f"Curso: {professor['curso']}")
        print(f"Matéria: {professor['materia']}")
        print("1 - Lançar ou alterar notas dos alunos (NP1/NP2/PIM)")
        print("2 - Registrar nota do exame")
        print("3 - Voltar ao menu principal")

        opc = input("Escolha: ").strip()

        if opc == "1":
            lancar_notas(professor)
        elif opc == "2":
            registrar_exame(professor)
        elif opc == "3":
            break
        else:
            print("❌ Opção inválida!\n")

def lancar_notas(professor):
    data = carregar_dados()
    curso_prof = professor["curso"]
    materia_prof = professor["materia"]

    print(f"\n=== LANÇAMENTO DE NOTAS ({curso_prof}) - {materia_prof} ===")
    alunos_mesmo_curso = [a for a in data["alunos"] if a["curso"] == curso_prof]

    if not alunos_mesmo_curso:
        print("⚠️ Nenhum aluno cadastrado nesse curso.\n")
        return

    for aluno in alunos_mesmo_curso:
        print(f"\nAluno: {aluno['nome']} | RA: {aluno['ra']} | Curso: {aluno['curso']}")

        if "notas" not in aluno:
            aluno["notas"] = {}

        # solicita NP1 NP2 PIM
        try:
            np1 = float(input("Nota NP1 (ou deixe em branco para pular): ").strip() or "nan")
        except:
            np1 = None
        try:
            np2 = float(input("Nota NP2 (ou deixe em branco para pular): ").strip() or "nan")
        except:
            np2 = None
        try:
            pim = float(input("Nota PIM (ou deixe em branco para pular): ").strip() or "nan")
        except:
            pim = None

        # se notas forem NaN (string blank), tratar como None
        def normaliza(x):
            return None if x is None or (isinstance(x, float) and (x != x)) else x

        np1 = normaliza(np1)
        np2 = normaliza(np2)
        pim = normaliza(pim)

        # guarda notas
        aluno["notas"].setdefault(materia_prof, {})
        if np1 is not None: aluno["notas"][materia_prof]["NP1"] = np1
        if np2 is not None: aluno["notas"][materia_prof]["NP2"] = np2
        if pim is not None: aluno["notas"][materia_prof]["PIM"] = pim

        # calcula média semestral se as 3 notas existirem
        notas_mat = aluno["notas"][materia_prof]
        if all(k in notas_mat for k in ("NP1","NP2","PIM")):
            vals = [float(notas_mat["NP1"]), float(notas_mat["NP2"]), float(notas_mat["PIM"])]
            semester_avg = round(sum(vals)/3, 2)
            aluno["notas"][materia_prof]["semester_avg"] = semester_avg
            if semester_avg >= 7.0:
                aluno["notas"][materia_prof]["status"] = "Aprovado"
                aluno["notas"]["materia_prof"].pop("exam_needed", None)
                print(f"✅ {aluno['nome']} média = {semester_avg} → Aprovado direto.")
            else:
                exam_needed = round(max(0, 7.0 - semester_avg), 2)
                aluno["notas"][materia_prof]["status"] = "Exame pendente"
                aluno["notas"][materia_prof]["exam_needed"] = exam_needed
                print(f"ℹ️ {aluno['nome']} média = {semester_avg} → Vai para exame. Precisa de {exam_needed} no exame (diferença para 7).")
        else:
            print("ℹ️ Nem todas as 3 notas (NP1/NP2/PIM) foram preenchidas para calcular média.")

    salvar_dados(data)
    print("💾 Todas as notas foram salvas com sucesso!\n")

def registrar_exame(professor):
    data = carregar_dados()
    curso_prof = professor["curso"]
    materia_prof = professor["materia"]

    alunos_mesmo_curso = [a for a in data["alunos"] if a["curso"] == curso_prof]
    if not alunos_mesmo_curso:
        print("⚠️ Nenhum aluno cadastrado nesse curso.\n")
        return

    print(f"\n=== Registrar exame ({materia_prof}) ===")
    for aluno in alunos_mesmo_curso:
        notas_mat = aluno.get("notas", {}).get(materia_prof)
        if not notas_mat or notas_mat.get("status") != "Exame pendente":
            # se aluno não tem exame pendente, pular
            continue

        print(f"\nAluno: {aluno['nome']} | RA: {aluno['ra']}")
        try:
            exame = float(input("Nota do exame: ").strip())
        except:
            print("Entrada inválida. Pulando.")
            continue

        notas_mat["exam_grade"] = exame
        # regra de aprovação no exame: precisa >= 5
        if exame >= 5.0:
            notas_mat["status"] = "Aprovado pelo exame"
            # opcional: calcular média final (por exemplo, última média é exam)
        else:
            notas_mat["status"] = "DP"
            # agenda surcharge +100 para o próximo mês
            from datetime import datetime
            next_month = (datetime.now().month % 12) + 1
            aluno["surcharge"] = aluno.get("surcharge", 0) + 100
            aluno["surcharge_month"] = next_month
            print(f"⚠️ {aluno['nome']} ficou DP. Será adicionado R$100 na mensalidade do mês {next_month}.")

        print(f"✅ Exame registrado. Status atual: {notas_mat['status']}")

    salvar_dados(data)
    print("💾 Registros de exame atualizados.\n")