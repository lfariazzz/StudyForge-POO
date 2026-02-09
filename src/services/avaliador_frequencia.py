# TODO: Integrar com os atributos finais de Aluno e Turma 
    # (Aguardando implementação de aluno.presenca e turma._diario_de_classe)

from src.core.configuracoes import Configuracoes
from datetime import date 
from src.models.turma import Turma
from src.models.aluno import Aluno
from src.models.demanda_pedagogica import DemandaPedagogica

class AvaliadorFrequencia:
    def __init__(self):
        config = Configuracoes()
        self.frequencia_minima = config.FREQUENCIA_MINIMA

    """Método para cálculo da validação da frequência do aluno 
    EM ESPERA: Depende da classe turma(atributo diario_de_classe)"""
    def aulas_mes_turma(self, turma, mes):
        total_aulas_mes = 0
        for aula in turma._diario_de_classe:
            if aula["data"].month == mes:
                total_aulas_mes += 1

        return total_aulas_mes
    

    """EM ESPERA: Depende da classe aluno(atributo presenca)"""
    def presencas_mes_aluno(self, aluno, mes):
        total_presencas_mes_aluno = 0
        for presenca in aluno.presenca:
            if presenca["data"].month == mes:
                total_presencas_mes_aluno += 1

        return total_presencas_mes_aluno

    def media_presenca_mensal_aluno(self, aluno, turma, mes):
        aulas_mes_turma = self.aulas_mes_turma(turma,mes)
        if aulas_mes_turma != 0:
            return (self.presencas_mes_aluno(aluno, mes)) / aulas_mes_turma
        else:
            raise ValueError ("Não existem aulas registradas")
        
    def media_presenca_mensal_turma(self, turma, mes):
        total_alunos = len(turma._alunos_matriculados)
        somatorio_media_alunos = 0
        for aluno in turma._alunos_matriculados:
           somatorio_media_alunos += self.media_presenca_mensal_aluno(aluno, turma, mes)
        
        if total_alunos != 0:
            return somatorio_media_alunos / total_alunos
        else:
            raise ValueError ("Não existem alunos registradas")
        
    def verificar_media_frequencia_mensal(self, turma, mes):
        media_mensal = self.media_presenca_mensal_turma(turma, mes)
        if media_mensal < self.frequencia_minima:
            print(f"Média de presença mensal da turma {media_mensal}\n Gerando demanda pedagógica...")
            """EM ESPERA: Depende da classe DemandaFactory"""
            demanda_evasao = DemandaPedagogica()