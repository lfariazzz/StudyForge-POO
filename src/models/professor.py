from __future__ import annotations
from src.models.usuario import Usuario
import re

"""
Representa a entidade Professor conforme o diagrama UML.
Herda atributos base de Usuario e adiciona dados funcionais e acadêmicos.
"""
class Professor(Usuario):
    def __init__(self, nome, cpf, email, senha, telefone, data_nascimento,
                 registro_funcional, escola_associada, titulacao, area_atuacao, 
                 salario, status=True):
        super().__init__(nome, cpf, email, senha, telefone, data_nascimento, status)

        self.registro_funcional = registro_funcional
        self.escola_associada = escola_associada
        self.titulacao = titulacao
        self.area_atuacao = area_atuacao
        self.salario = salario
        self.turmas_associadas: list[Turma] = []

    #-----------------
    #GETTERS E SETTERS
    #-----------------

    @property
    def registro_funcional(self):
        """Retorna o registro funcional (RF) do professor."""
        return self._registro_funcional
    
    @registro_funcional.setter
    def registro_funcional(self, valor):
        if not isinstance(valor, str):
            raise TypeError("Erro: Registro Funcional deve ser uma string!")
        
        valor = valor.strip().upper()

        padrao_rf = r'^RF-\d{4}-\d{4}$'

        if not re.match(padrao_rf, valor):
            raise ValueError("Erro: RF inválido! Use o padrão RF-ANO-SEQUENCIAL (Ex: RF-2026-0001).")
        
        self._registro_funcional = valor

    @property
    def escola_associada(self):
        """Retorna o nome da escola onde o professor leciona."""
        return self._escola_associada
    
    @escola_associada.setter
    def escola_associada(self, valor):
        if hasattr(valor, 'id_escola'):
            self._escola_associada = valor
        elif isinstance(valor, str):
            self._escola_associada = valor
        else:
            raise TypeError("Erro: escola_associada deve ser um objeto da classe Escola.")
        
    @property
    def titulacao(self):
        """Retorna o grau acadêmico do professor."""
        return self._titulacao
    
    @titulacao.setter
    def titulacao(self, valor):
        if not isinstance(valor, str):
            raise TypeError("Erro: A titulação deve ser uma string!")
        
        tit_formatado = valor.strip().title()

        titulacoes_validas = ["Graduado", "Especialista", "Mestre", "Doutor", "Pós-Doutor"]

        if tit_formatado not in titulacoes_validas:
            raise ValueError(f"Erro: Titulação inválida! Escolha entre: {', '.join(titulacoes_validas)}")
        
        else:
            self._titulacao = tit_formatado

    @property
    def area_atuacao(self):
        """Retorna a área de especialidade/lecionada pelo professor."""
        return self._area_atuacao
    
    @area_atuacao.setter
    def area_atuacao(self, valor):
        if not isinstance(valor, str):
            raise TypeError("Erro: A área de atuação deve ser uma string!")
        area_limpa = valor.strip().title()

        if len(area_limpa) < 3:
            raise ValueError("Erro: A área de atuação deve ter no mínimo 3 caracteres!")
        
        else: 
            self._area_atuacao = area_limpa

    @property
    def salario(self):
        """Retorna o salário do professor."""
        return self._salario
    
    @salario.setter
    def salario(self, valor):
        if not isinstance(valor, (int,float)):
            raise TypeError("Erro: O salario deve ser um valor numérico!")
        if valor < 0:
            raise ValueError("Erro: Salario não pode ser negativo!")
        
        salario_minimo = 1621.00
        if valor < salario_minimo:
            print(f"⚠️ Aviso: O salário informado (R$ {valor:.2f}) está abaixo do minimo nacional.")
        self._salario = float(valor)

    #-------
    #MÉTODOS
    #-------

    def get_permissao(self):
        """Retorna as permissões específicas do professor no sistema."""
        return "Professor: Acesso a diários de classe, frequências e materiais didáticos."
    
    def realizar_chamada(self, turma: Turma, data: str, presencas: list):
        """Registra a presença dos alunos em uma turma específica."""
        id_t = turma.id_turma if hasattr(turma, 'id_turma') else turma
        print(f"✅ Chamada registrada pelo(a) Prof. {self.nome} para a Turma {id_t} em {data}.")

    def enviar_material(self, turma: Turma, material: Material):
        """Associa um material didático a uma turma."""
        nome_m = material.titulo if hasattr(material, 'titulo') else material
        print(f"📚 Material '{nome_m}' enviado para a turma.")

    def to_dict(self):
        dados = super().to_dict() 
        
        id_esc = self.escola_associada.id_escola if hasattr(self.escola_associada, 'id_escola') else self.escola_associada
        
        dados.update({
            "registro_funcional": self.registro_funcional,
            "id_escola": id_esc,
            "titulacao": self.titulacao,
            "area_atuacao": self.area_atuacao,
            "salario": self.salario,
            "turmas_vinculadas": [t.id_turma if hasattr(t, 'id_turma') else t for t in self.turmas_associadas]
        })
        return dados
    
    def exibir_perfil(self):
        """Exibe os dados formatados do professor (Útil para verificar os Setters)."""
        print("\n" + "="*30)
        print(f"PERFIL DO PROFESSOR: {self.nome}")
        print("="*30)
        print(f"RF:         {self.registro_funcional}")
        print(f"Titulação:  {self.titulacao}")
        print(f"Área:       {self.area_atuacao}")
        print(f"E-mail:     {self.email}")
        print(f"Salário:    R$ {self.salario:.2f}")
        print(f"Status:     {'Ativo' if self.status else 'Inativo'}")
        print("="*30 + "\n")

    def enviar_mensagem(self, destinatario: Usuario, mensagem: str):
        """Envia uma mensagem para outro usuário do sistema."""
        nome_dest = destinatario.nome if hasattr(destinatario, 'nome') else "Usuário"
        print(f"✉️ Mensagem enviada de {self.nome} para {nome_dest}: {mensagem}")

    def enviar_solicitacao(self, gestor: Usuario, tipo_solicitacao: str):
        """Envia solicitações (ex: férias, material) para o Gestor/Secretário."""
        print(f"📝 Solicitação de '{tipo_solicitacao}' enviada pelo Prof. {self.nome} para análise.")

    def consultar_turmas(self) -> list:
        """Retorna a lista de turmas que o professor leciona."""
        if not self.turmas_associadas:
            print(f"ℹ️ O professor {self.nome} ainda não possui turmas vinculadas.")
            return []
        
        return [t.nome if hasattr(t, 'nome') else t for t in self.turmas_associadas]