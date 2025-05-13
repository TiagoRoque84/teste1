# main.py
import json, statistics

def carrega_dados():
    with open('dados.json','r') as f: return json.load(f)

def salva_dados(d): 
    with open('dados.json','w') as f: json.dump(d,f,indent=2)

def cadastro():
    d = carrega_dados()
    nome = input("Nome: ")
    novo = {"id":len(d["usuarios"])+1, "nome":nome, "acertos":[]}
    d["usuarios"].append(novo)
    salva_dados(d)
    print("✅ Usuário cadastrado!")

def quiz():
    d = carrega_dados()
    uid = int(input("ID do usuário: "))
    user = next(u for u in d["usuarios"] if u["id"]==uid)
    perguntas = [("2+2?","4"),("média de 2,4,6?","4")]
    acertos = sum(1 for q,a in perguntas if input(q+" ")==a)
    user["acertos"].append(acertos)
    salva_dados(d)
    print(f"🎯 Acertou {acertos}/{len(perguntas)}")

def estatisticas():
    d = carrega_dados()
    todas = [score for u in d["usuarios"] for score in u["acertos"]]
    if not todas: return print("Sem dados ainda.")
    print("Média:",statistics.mean(todas))
    print("Mediana:",statistics.median(todas))
    print("Moda:",statistics.mode(todas))

def menu():
    while True:
        print("\n1.Cad 2.Quiz 3.Stats 4.Sair")
        op = input(">> ")
        if op=="1": cadastro()
        elif op=="2": quiz()
        elif op=="3": estatisticas()
        else: break

if __name__=="__main__":
    menu()
