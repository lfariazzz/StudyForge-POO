from src.models.demanda import Demanda
from src.models.demanda_pedagogica import DemandaPedagogica
from src.models.demanda_infraestrutura import DemandaInfraestrutura
from src.core.configuracoes import Configuracoes
import uuid


class DemandaFactory:
    config = Configuracoes()

    @staticmethod
    def criar_demanda(tipo_demanda, solicitante, descricao=None, prioridade="NORMAL", **kwargs):
        id_demanda = str(uuid.uuid4())
        turma_selecionada = kwargs.get("turma")
        if turma_selecionada:
            if not descricao:
                
            else:
                #regra manual