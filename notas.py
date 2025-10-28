def calcular_media(notas):
    return sum(notas) / len(notas)

def notas_menu():
    print("\n=== Controle de Notas ===")
    nome = input("Nome do aluno: ")
    notas = []
    for i in range(1, 4):
        n = float(input(f"Nota {i}: "))
        notas.append(n)

    media = calcular_media(notas)
    status = "Aprovado ✅" if media >= 6 else "Reprovado ❌"

    print(f"\nAluno: {nome}\nMédia: {media:.2f}\nStatus: {status}\n")

if __name__ == "__main__":
    notas_menu()
