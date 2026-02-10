from src.core.configuracoes import Configuracoes
from src.core.demanda_factory import DemandaFactory
class AvaliadorFrequencia:
    def __init__(self):
        config = Configuracoes()
        self.frequencia_minima = config.FREQUENCIA_MINIMA

    """Método para cálculo da quantidade de aulas em um mês de uma turma,
    permitindo saber a presença individual e coletiva mensal."""
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
        
    def qtd_alunos_abaixo_media_frequencia(self, turma, mes):
        qtd_media_abaixo = 0
        for aluno in turma._alunos_matriculados:
            if self.media_presenca_mensal_aluno(aluno, turma, mes) < self.frequencia_minima:
                qtd_media_abaixo +=1
        return qtd_media_abaixo
            
        
    def verificar_media_frequencia_mensal(self, turma, mes):
        media_mensal = self.media_presenca_mensal_turma(turma, mes)
        if media_mensal < self.frequencia_minima:
            print(f"Média de presença mensal da turma {media_mensal}\n Gerando demanda pedagógica...")
            alunos_abaixo_media = self.qtd_alunos_abaixo_media_frequencia(turma, mes)
            demanda_evasao = DemandaFactory.criar_demanda("PEDAGOGICA", "SISTEMA", None, turma=turma, 
                                               media_mensal=media_mensal, alunos_abaixo_media=alunos_abaixo_media)
            return demanda_evasao