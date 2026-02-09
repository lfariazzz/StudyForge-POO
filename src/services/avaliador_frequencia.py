# TODO: Integrar com os atributos finais de Aluno e Turma 
    # (Aguardando implementação de aluno.presenca e turma._diario_de_classe)

from src.core.configuracoes import Configuracoes

class AvaliadorFrequencia:
    def __init__(self):
        config = Configuracoes()
        self.frequencia_minima = config.FREQUENCIA_MINIMA

    """Método para cálculo da validação da frequeência do aluno 
    EM ESPERA: Depende da classe aluno(atributo presenca) e da classe turma(atributo de aulas)"""
    def aprovacao_presenca_aluno(self, aluno, turma):
        total_aulas = len(turma._diario_de_classe)
        if total_aulas == 0:
            print("Nâo há aulas registradas")
            return False
        percentual_presenca = (aluno.presenca) / total_aulas

        return percentual_presenca >= self.frequencia_minima