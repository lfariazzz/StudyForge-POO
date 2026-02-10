from src.models.demanda_pedagogica import DemandaPedagogica
from src.models.demanda_infraestrutura import DemandaInfraestrutura
from src.core.configuracoes import Configuracoes
import uuid

"""Classe que faz uso do pattern factory, centralizando a criação de instâncias de demanda e isolando essa criação do funcionamento da classe."""
class DemandaFactory:
    config = Configuracoes()

    """Métodos que permitem a criação de instâncias de demanda de acordo com o tipo e validam as regras de negócio:
    02 - Geração de demanda pedagógica automática caso a evasão de uma turma ultrapasse 25% 
    03 - Alteração automática do status de uma demanda de insfraestrutura caso ultrapasse o valor limite definido"""
    @staticmethod
    def criar_demanda(tipo_demanda, solicitante, descricao=None, prioridade="NORMAL", **kwargs):
        id_demanda = str(uuid.uuid4())
        turma_selecionada = kwargs.get("turma")
        if tipo_demanda.upper() == "PEDAGOGICA":
            if turma_selecionada:
                total_alunos = len(turma_selecionada._alunos_matriculados)
                alunos_abaixo_media = kwargs.get("alunos_abaixo_media")
                frequencia_turma = kwargs.get("frequencia_turma")
                alunos_presentes = kwargs.get("alunos_presentes")
                if not descricao:
                    solicitante = "SISTEMA"
                    media_mensal = kwargs.get("media_mensal", 0)
                    prioridade = "ALTA"
                    descricao = f"Demanda pedagógica gerada automaticamente para a turma {turma_selecionada} devido alta taxa de evasão de {(1 - media_mensal) * 100}%"
                    
                return DemandaPedagogica(id_demanda, descricao, prioridade, solicitante, 
                                        total_alunos, alunos_abaixo_media,frequencia_turma, alunos_presentes, turma_selecionada)
            else:
                raise ValueError("Informe uma turma para criar uma demanda!")
            
        elif tipo_demanda.upper() == "INFRAESTRUTURA":
            custo_estimado = kwargs.get("custo_estimado", 0)
            localizacao_demanda = kwargs.get("localizacao_demanda")
            if custo_estimado > DemandaFactory.config.LIMITE_CUSTO_DEMANDA:
                prioridade = "MAXIMA"
                if  descricao:  
                    descricao += "[GERADO PELO SISTEMA]: Valor estimado da demanda ultrapassa o valor limite.\nSolicitando autorização do Secretário Municipal para aprovação"
                else:
                    descricao = "[GERADO PELO SISTEMA]: Valor estimado da demanda ultrapassa o valor limite.\nSolicitando autorização do Secretário Municipal para aprovação"
            nova_demanda = DemandaInfraestrutura(id_demanda, descricao, prioridade, solicitante, custo_estimado, localizacao_demanda)
            if prioridade == "MAXIMA":
                nova_demanda.atualizar_status("AGUARDANDO LICITACAO")

            return nova_demanda

        
        else:
            raise ValueError("Tipo de demanda inexistente")
