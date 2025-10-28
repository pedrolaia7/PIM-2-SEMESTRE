# cursos.py
def menu_cursos(aluno):
    print(f"=== Bem-vindo(a), {aluno['nome']} ===")
    print(f"📘 Curso: {aluno['curso']}")
    print(f"📄 Modalidade: {aluno.get('modalidade', 'N/A')}")
    print(f"💸 Bolsa: {aluno.get('bolsa_percent', 0)}%\n")

    mostrar_materias(aluno)

def mostrar_materias(aluno):
    curso = aluno["curso"]
    materias_ti = {
        "Análise e Desenvolvimento de Sistemas (ADS)": [
            "Python 1",
            "Banco de Dados 1",
            "Engenharia de Software",
            "Algoritmos e Lógica de Programação",
            "Redes de Computadores"
        ],
        "Ciência da Computação": [
            "Python 1",
            "Estrutura de Dados",
            "Arquitetura de Computadores",
            "Matemática Discreta",
            "Linguagens Formais"
        ],
        "Engenharia de Software": [
            "Python 1",
            "Modelagem de Sistemas",
            "Banco de Dados 1",
            "Testes de Software",
            "Gestão de Projetos"
        ],
        "Gestão da Tecnologia da Informação": [
            "Python 1",
            "Infraestrutura de T.I.",
            "Gestão de Equipes",
            "Sistemas Operacionais",
            "Banco de Dados 1"
        ],
        "Segurança da Informação": [
            "Python 1",
            "Criptografia",
            "Redes Seguras",
            "Análise de Vulnerabilidades",
            "Governança de T.I."
        ]
    }

    if curso not in materias_ti:
        print("❌ Curso não encontrado.\n")
        return

    notas_encontradas = False
    print(f"\n=== Disciplinas do curso: {curso} ===\n")
    for materia in materias_ti[curso]:
        notas = aluno.get("notas", {}).get(materia)
        if notas:
            notas_encontradas = True
            np1 = notas.get("NP1", "—")
            np2 = notas.get("NP2", "—")
            pim = notas.get("PIM", "—")
            sem = notas.get("semester_avg", "—")
            status = notas.get("status", "—")
            line = f"- {materia}: NP1={np1} | NP2={np2} | PIM={pim} | Média={sem} | Status={status}"
            if status == "Exame pendente":
                line += f" | Precisa no exame: {notas.get('exam_needed')}"
            if "exam_grade" in notas:
                line += f" | Exame={notas.get('exam_grade')}"
            print(line)
        else:
            print(f"- {materia}: As notas ainda não foram postadas pelo professor.")

    if not notas_encontradas:
        print("\n📢 Nenhuma nota foi postada ainda para o seu curso.\n")
