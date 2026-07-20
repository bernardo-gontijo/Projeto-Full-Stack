import pandas as pd
import random
from datetime import timedelta, datetime

random.seed(42)

nomes = [
    "Ana", "Bruno", "Bernardo", "Carla", "Diego", "Elisa", "Fábio",
    "Gabriela", "Henrique", "Isabela", "João", "Karina", "Lucas",
    "Mariana", "Nicolas", "Olívia", "Pedro", "Queila", "Rafael",
    "Sofia", "Tiago", "Ursula", "Vitor", "Wesley", "Yasmin",
    "Amanda", "Bianca", "Caio", "Daniela", "Eduardo", "Fernanda",
    "Gabriel", "Helena", "Igor", "Juliana", "Kevin", "Lethicia",
    "Marcelo", "Natália", "Otávio", "Paulo", "Rodrigo", "Sabrina",
    "Thiago", "Valentina", "Walter", "Kauan", "Yago", "Zinedine"
]
unidades = ["Flores", "Torres", "Cidade Nova", "Centro", "Alvorada", "Morada", "Japiim"]
planos = ["Básico", "Intermediário", "Avançado"]
objetivos = ["Emagrecimento", "Hipertrofia", "Condicionamento", "Performance"]

def data_aleatoria(inicio, fim):
    delta = fim - inicio
    dias_aleatorios = random.randint(0, delta.days)
    return inicio + timedelta(days=dias_aleatorios)

def telefone_aleatorio():
    parte1 = random.randint(90000, 99999)
    parte2 = random.randint(1000, 9999)
    return f"({92}) {parte1}-{parte2}"

data_inicio = datetime(2022, 1, 1)
data_fim = datetime(2026, 7, 19)

registros = []
for i in range(1, 201):
 registros.append({
 "id": i,
 "nome": random.choice(nomes),
 "idade": random.randint(18, 65),
 "unidade": random.choice(unidades),
 "plano": random.choice(planos),
 "objetivo": random.choice(objetivos),
 "data_matricula": data_aleatoria(data_inicio, data_fim).strftime("%Y-%m-%d"),
 "telefone": telefone_aleatorio()
 })

df = pd.DataFrame(registros)
df.to_csv("dados.csv", index=False)
print(df.head())
