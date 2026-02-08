
from .escola import Escola

class Municipio:
    def __init__(self, nome, id_municipio, estado, verba_disponivel_municipio):
        self._nome = nome
        self._id_municipio = id_municipio
        self.estado = estado  # Aciona o setter para validação
        self._verba_disponivel_municipio = float(verba_disponivel_municipio)
        
        self._escolas_situadas = []  
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def id_municipio(self):
        return self._id_municipio
    
    @property
    def estado(self):
        return self._estado
    
    @estado.setter
    def estado(self, valor):
        # Garante que só aceite siglas como SP, RJ, MG...
        if not isinstance(valor, str) or len(valor) != 2:
            raise ValueError("O estado (UF) deve conter exatamente 2 caracteres alfabéticos.")
        self._estado = valor.upper()
    
    @property
    def verba_disponivel_municipio(self):
        return self._verba_disponivel_municipio
    
    @verba_disponivel_municipio.setter
    def verba_disponivel_municipio(self, valor):
        if valor < 0:
            raise ValueError("A verba disponível não pode ser negativa.")
        self._verba_disponivel_municipio = float(valor)
    
    @property
    def escolas_situadas(self):
        return self._escolas_situadas

    def cadastrar_escola(self, escola):
        # Verificamos se o que está vindo é realmente um objeto
        if escola not in self._escolas_situadas:
            self._escolas_situadas.append(escola)
            print(f"Escola '{escola.nome}' cadastrada no município {self._nome}.")
            return True
        return False
    
    def calcular_investimento_total(self):
        "Calcula a verba do município somada à verba de todas as escolas situadas."
        verba_escolas = sum(escola.verba_disponivel_escola for escola in self._escolas_situadas)
        return self._verba_disponivel_municipio + verba_escolas
    
    def to_dict(self):
        "Retorna os dados da classe em formato de dicionário."
        return {
            "nome": self._nome,
            "id_municipio": self._id_municipio,
            "estado": self._estado,
            "verba_disponivel_municipio": self._verba_disponivel_municipio
        }
    
    def __str__(self):
        return f"Município: {self._nome} - {self._estado} (ID: {self._id_municipio})"