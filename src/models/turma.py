from .professor import Professor
from .aluno import Aluno

class Turma:
    def __init__(self, id_turma, nome, ano_letivo, id_escola):
        self._id_turma = id_turma
        self._nome = nome
        self.ano_letivo = ano_letivo # Usa o setter para validar no momento da criação
        self._id_escola = id_escola
        
        self._professores_regentes = []
        self._alunos_matriculados = []
        self._diario_de_classe = []

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor or len(valor.strip()) == 0:
            raise ValueError("O nome da turma não pode estar vazio.")
        self._nome = valor

    @property
    def id_turma(self):
        return self._id_turma

    @property
    def ano_letivo(self):
        return self._ano_letivo

    @ano_letivo.setter
    def ano_letivo(self, valor):
        try:
            valor_int = int(valor)
        except (ValueError, TypeError):
            raise ValueError("Ano letivo deve ser um número válido.")
            
        if valor_int < 2000 or valor_int > 2100:
            raise ValueError("Ano letivo inválido. Deve estar entre 2000 e 2100.")
        self._ano_letivo = valor_int
    
    @property
    def id_escola(self):
        return self._id_escola
    
    @property
    def alunos_matriculados(self):
        return self._alunos_matriculados

    # Métodos de Associação para preencher as listas do diagrama
    def adicionar_aluno(self, aluno):
        "Espera uma instância da classe Aluno."
        self._alunos_matriculados.append(aluno)

    def adicionar_professor(self, professor):
        "Espera uma instância da classe Professor."
        self._professores_regentes.append(professor) 

    # Métodos de Negócio definidos no UML
    def obter_quadro_horario(self):

        nomes = [p.nome for p in self._professores_regentes]
        return {
            "Turma": self._nome,
            "Professores": nomes if nomes else "Nenhum alocado"
        }

    def registrar_aula(self, data, conteudo: str):
        "Valida o conteúdo e armazena no histórico da turma."

        if not conteudo or len(conteudo.strip()) < 5:
            print("Erro: Conteúdo da aula muito curto ou vazio.")
            return False
        
        #dicionário com os dados da aula
        nova_aula = {
            "data": data,
            "conteudo": conteudo,
            "id_turma": self._id_turma
        }
        
        # Salvamos na lista diario_de_classes no __init__ # classe nova
        self._diario_de_classe.append(nova_aula)
        print(f"[{self._nome}] Aula registrada em {data}: {conteudo}")
        return True

    def to_dict(self):
        "Converte os dados da turma para um dicionário."
        return {
            "id_turma": self._id_turma,
            "nome_truma": self._nome,
            "ano_letivo": self._ano_letivo,
            "total_alunos": len(self._alunos_matriculados),
            "total_professores": len(self._professores_regentes),
            "id_escola": self._id_escola
        }

    def __str__(self):
        return f"Turma: {self._nome} - {self._ano_letivo} (ID: {self._id_turma})"