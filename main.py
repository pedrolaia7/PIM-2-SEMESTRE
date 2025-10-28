import cadastro
import login
import professores
import cursos
import financeiro  # integrado ao menu do aluno

def main():
    while True:
        print("\n=== SISTEMA ACADÊMICO ===")
        print("1 - Cadastrar aluno/professor")
        print("2 - Fazer login")
        print("3 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastro.cadastrar_usuario()

        elif opcao == "2":
            usuario, tipo = login.login()

            if usuario:
                if tipo == "aluno":
                    menu_aluno(usuario)
                elif tipo == "professor":
                    professores.menu_professor(usuario)

        elif opcao == "3":
            print("Saindo do sistema... Até logo!")
            break
        else:
            print("❌ Opção inválida, tente novamente.\n")

def menu_aluno(aluno):
    while True:
        print(f"\n=== MENU DO ALUNO ({aluno['nome']}) ===")
        print("1 - Ver cursos e notas")
        print("2 - Financeiro")
        print("3 - Sair")

        opc = input("Escolha: ").strip()
        if opc == "1":
            cursos.menu_cursos(aluno)
        elif opc == "2":
            financeiro.menu_financeiro(aluno)
        elif opc == "3":
            print("Voltando ao menu principal...\n")
            break
        else:
            print("❌ Opção inválida!\n")

if __name__ == "__main__":
    main()
