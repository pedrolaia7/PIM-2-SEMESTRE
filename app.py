from flask import Flask, render_template, request, redirect, url_for
import json, os, random, string, re
from datetime import datetime

app = Flask(__name__)
DB_PATH = "database.json"

# ===================== Funções utilitárias =====================
def carregar_dados():
    if not os.path.exists(DB_PATH):
        return {"alunos": [], "professores": []}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_dados(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def gerar_ra():
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))
    numeros = ''.join(random.choices(string.digits, k=3))
    return letras + numeros

# ===================== Página inicial =====================
@app.route("/")
def home():
    return render_template("login.html")

# ===================== Cadastro =====================
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        tipo = request.form["tipo"]
        nome = request.form["nome"]
        senha = request.form["senha"]

        cursos = [
            "Análise e Desenvolvimento de Sistemas (ADS)",
            "Engenharia de Software",
            "Ciência da Computação",
            "Gestão da Tecnologia da Informação",
            "Segurança da Informação"
        ]

        curso = cursos[int(request.form["curso"]) - 1]
        data = carregar_dados()

        # ---------------- ALUNO ----------------
        if tipo == "aluno":
            modalidade = request.form["modalidade"]
            tem_bolsa = request.form.get("tem_bolsa", "nao")
            bolsa_percent = 0
            codigo_bolsa = ""

            # Se o aluno tiver bolsa, coleta e valida
            if tem_bolsa == "sim":
                bolsa_percent = float(request.form.get("bolsa_percent", 0))
                codigo_bolsa = request.form.get("codigo_bolsa", "").strip()

                # Validação do formato: 1 letra + 3 números (ex: A123)
                if not re.match(r"^[A-Za-z]\d{3}$", codigo_bolsa):
                    return render_template(
                        "cadastro.html",
                        erro="Código da bolsa inválido. Deve ter 1 letra e 3 números (ex: A123)."
                    )

            ra = gerar_ra()
            data["alunos"].append({
                "tipo": "aluno",
                "nome": nome,
                "senha": senha,
                "curso": curso,
                "ra": ra,
                "modalidade": modalidade,
                "bolsa_percent": bolsa_percent,
                "codigo_bolsa": codigo_bolsa,
                "notas": {},
                "dp": False
            })
            salvar_dados(data)
            return render_template("cadastro.html", sucesso=f"Aluno cadastrado com sucesso! Seu RA é {ra}")

        # ---------------- PROFESSOR ----------------
        elif tipo == "professor":
            materia = request.form["materia"]
            ra = gerar_ra()
            data["professores"].append({
                "tipo": "professor",
                "nome": nome,
                "senha": senha,
                "curso": curso,
                "ra": ra,
                "materia": materia
            })
            salvar_dados(data)
            return render_template("cadastro.html", sucesso=f"Professor cadastrado com sucesso! Seu RA é {ra}")

    return render_template("cadastro.html")

# ===================== Login =====================
@app.route("/login", methods=["POST"])
def login():
    ra = request.form["ra"]
    senha = request.form["senha"]
    data = carregar_dados()

    for aluno in data["alunos"]:
        if aluno["ra"] == ra and aluno["senha"] == senha:
            return redirect(url_for("portal_aluno", ra=ra))
    for prof in data["professores"]:
        if prof["ra"] == ra and prof["senha"] == senha:
            return redirect(url_for("portal_professor", ra=ra))
    return render_template("login.html", erro="RA ou senha incorretos!")

# ===================== Portal do aluno =====================
@app.route("/aluno/<ra>")
def portal_aluno(ra):
    data = carregar_dados()
    aluno = next((a for a in data["alunos"] if a["ra"] == ra), None)
    return render_template("portal_aluno.html", aluno=aluno)

@app.route("/notas/<ra>")
def notas(ra):
    data = carregar_dados()
    aluno = next((a for a in data["alunos"] if a["ra"] == ra), None)
    if not aluno:
        return "Aluno não encontrado."
    
    notas = aluno.get("notas", {})
    for mat, ns in notas.items():
        media = (ns.get("NP1", 0) + ns.get("NP2", 0) + ns.get("PIM", 0)) / 3
        if media < 7:
            aluno["exame"] = True
            aluno["exame_msg"] = f"Sua média é {media:.2f}. Você precisa de {7 - media:.2f} no exame para passar."
        else:
            aluno["exame"] = False
            aluno["exame_msg"] = f"Média final {media:.2f}. Aprovado!"
    salvar_dados(data)

    return render_template("notas.html", aluno=aluno, notas=notas)

@app.route("/financeiro/<ra>")
def financeiro(ra):
    data = carregar_dados()
    aluno = next((a for a in data["alunos"] if a["ra"] == ra), None)

    mensalidades = {
        "Análise e Desenvolvimento de Sistemas (ADS)": 470,
        "Engenharia de Software": 720,
        "Ciência da Computação": 630,
        "Gestão da Tecnologia da Informação": 590,
        "Segurança da Informação": 530
    }

    base = mensalidades.get(aluno["curso"], 0)
    valor = base * (1 - aluno.get("bolsa_percent", 0)/100)
    if aluno.get("dp"):
        valor += 100

    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
             "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]

    return render_template("financeiro.html", aluno=aluno, valor=valor, meses=meses)

# ===================== Portal do professor =====================
@app.route("/professor/<ra>", methods=["GET", "POST"])
def portal_professor(ra):
    data = carregar_dados()
    prof = next((p for p in data["professores"] if p["ra"] == ra), None)

    if request.method == "POST":
        ra_aluno = request.form["ra_aluno"]
        np1 = float(request.form["np1"])
        np2 = float(request.form["np2"])
        pim = float(request.form["pim"])

        aluno = next((a for a in data["alunos"] if a["ra"] == ra_aluno), None)
        if not aluno:
            return render_template("portal_professor.html", prof=prof, erro="Aluno não encontrado.")
        if aluno["curso"] != prof["curso"]:
            return render_template("portal_professor.html", prof=prof, erro="Aluno não pertence a este curso.")

        materia_prof = prof["materia"]
        aluno.setdefault("notas", {})
        aluno["notas"][materia_prof] = {"NP1": np1, "NP2": np2, "PIM": pim}
        media = (np1 + np2 + pim) / 3

        aluno["dp"] = media < 7
        salvar_dados(data)
        return render_template("portal_professor.html", prof=prof, sucesso=f"Notas lançadas com sucesso para {aluno['nome']}!")

    return render_template("portal_professor.html", prof=prof)

# ===================== Chatbot Junior 2.0 =====================
@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    msg = data.get("message", "").strip().lower()

    # Histórico simples
    hist_path = "chat_history.json"
    if not os.path.exists(hist_path):
        historico = []
    else:
        try:
            with open(hist_path, "r", encoding="utf-8") as f:
                historico = json.load(f)
        except json.JSONDecodeError:
            historico = []

    respostas = {
        "mensalidade": "💰 As mensalidades variam de acordo com o curso e a modalidade. Você pode ver o valor exato na aba *Financeiro* do portal.",
        "sistema": "📘 O sistema acadêmico foi criado para facilitar sua vida. Nele você acessa notas, boletos e informações do curso.",
        "pagamento": "💳 Os pagamentos podem ser feitos por boleto ou cartão. Caso esteja com atraso, fale com o setor financeiro.",
        "bolsa": "🎓 As bolsas vão de 5% até 70%. Se você tem um código de bolsa (ex: A123), insira no seu cadastro.",
        "curso": "🖥️ Nossos cursos incluem: ADS, Engenharia de Software, Ciência da Computação, Gestão de TI e Segurança da Informação.",
        "outros": "☎️ Tudo bem! Vou registrar seu pedido para atendimento humano. Um atendente entrará em contato em breve."
    }

    # IA básica
    if msg in ["1", "mensalidade"]:
        resposta = respostas["mensalidade"]
    elif msg in ["2", "como funciona", "sistema", "acadêmico"]:
        resposta = respostas["sistema"]
    elif msg in ["3", "pagamento", "boletos", "boleto"]:
        resposta = respostas["pagamento"]
    elif msg in ["4", "bolsa", "desconto"]:
        resposta = respostas["bolsa"]
    elif msg in ["5", "curso", "cursos", "matéria"]:
        resposta = respostas["curso"]
    elif msg in ["6", "atendente", "humano", "suporte"]:
        resposta = respostas["outros"]
    elif "obrigado" in msg or "valeu" in msg:
        resposta = "😄 Que bom poder ajudar! Qualquer coisa é só chamar o Junior novamente!"
    elif "oi" in msg or "olá" in msg or "ola" in msg:
        resposta = "👋 Olá! Eu sou o Junior, seu assistente acadêmico. Quer saber sobre mensalidades, cursos ou bolsas?"
    elif "pim" in msg:
        resposta = "📚 O PIM é o Projeto Integrado Multidisciplinar. Ele é uma atividade avaliativa prática e importante para a conclusão do semestre!"
    elif "quem criou você" in msg or "quem te criou" in msg:
        resposta = "😎 Fui criado por um desenvolvedor talentoso da UNIP — um projeto acadêmico incrível!"
    else:
        if any(p in msg for p in ["nota", "prova", "np1", "np2", "pim", "exame"]):
            resposta = "🧾 As notas ficam disponíveis na aba *Notas*. Caso ainda não apareçam, o professor pode não ter lançado."
        elif any(p in msg for p in ["financeiro", "mensalidade", "valor", "preço"]):
            resposta = respostas["mensalidade"]
        elif any(p in msg for p in ["curso", "matéria", "disciplinas"]):
            resposta = respostas["curso"]
        else:
            resposta = "🤔 Ainda estou aprendendo! Tente reformular sua dúvida ou escolha uma opção de 1 a 6."

    historico.append({"usuario": msg, "resposta": resposta})
    with open(hist_path, "w", encoding="utf-8") as f:
        json.dump(historico[-50:], f, indent=4, ensure_ascii=False)

    return {"resposta": resposta}

if __name__ == "__main__":
    app.run(debug=True)
