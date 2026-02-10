"""Classe responsável pela definição de limites e configurações padrões do sistema cumprindo as regras de negócio e 
fazendo uso do Pattern Singleton, mantendo a padronização das instâncias e da consistência global em todo o sistema
        Atributos:
        FREQUENCIA_MINIMA (float): Percentual mínimo de presença (RN02).
        INDICE_LACUNA_MINIMO (float): Limite inferior para detecção de lacunas (RN03).
        LIMITE_CUSTO_DEMANDA (float): Teto orçamentário para requisições (RN04)."""
class Configuracoes:
    _instancia = None
    FREQUENCIA_MINIMA = 0.75
    INDICE_LACUNA_MINIMO = 0.3
    LIMITE_CUSTO_DEMANDA = 15000.0

    def __new__(cls):
        """Método especial para criação da instância ou padronização de já criadas"""
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia


    def atualizar_parametro(self, nome, valor):
        """Método para alteração de limites e configurações pré-estabelecidas"""
        nome = nome.upper()
        if hasattr(self, nome) and not nome.startswith("_"):
            atual = getattr(self, nome)
            permitidos = (int, float) if isinstance(atual, float) else type(atual)
            if isinstance(valor, permitidos):
                setattr(self, nome, valor)
            else:
                raise TypeError("Valor fornecido inválido")
        else:
            raise ValueError("Parâmetro fornecido inválido")

    def resetar_padroes(self):
        """Método de redefinação das configurações iniciais do sistema"""
        for k in list(self.__dict__.keys()):
            if not k.startswith("_"):
                delattr(self, k)