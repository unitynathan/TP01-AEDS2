from faker import Faker
import random
from aluno import Aluno

def gerar_lista_alunos(num_registros):
    # gera lista de alunos
    fake = Faker('pt_BR')
    alunos = []
    cursos = ['Engenharia de computacao', 'Sistemas de informacao', 'Engenharia eletrica', 'Engenharia de producao']
    
    for _ in range(num_registros):
        aluno = Aluno(
            matricula=random.randint(100000000, 999999999),
            nome=fake.name(),
            cpf=fake.cpf().replace('.', '').replace('-', ''),
            curso=random.choice(cursos),
            filiacao_mae=fake.name_female(),
            filiacao_pai=fake.name_male(),
            ano_ingresso=random.randint(2015, 2024),
            ca=round(random.uniform(6.0, 10.0), 2)
        )
        alunos.append(aluno)
    return alunos