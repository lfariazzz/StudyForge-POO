from __future__ import annotations
from src.models.usuario import Usuario
import re
"""
Representa a entidade Aluno conforme o diagrama UML.
Herda atributos base de Usuario e gerencia sua vida acadêmica.
"""

class Aluno(Usuario):
    def __init__(self, nome, cpf, email, senha, telefone, data_nascimento,
                id_matricula, turma_associada = None, status=True):
        super().__init__(nome, cpf, email, senha, telefone, data_nascimento, status)

        self.id_matricula = id_matricula
        self.turma_associada = turma_associada 
        self._notas = {}

    # -----------------
    # GETTERS E SETTERS
    # -----------------

    @property
    def id_matricula(self):
        """Retorna a matrícula única do aluno."""
        return self._id_matricula
    
    @id_matricula.setter
    def id_matricula(self, valor):
        if not isinstance(valor, str):
            raise TypeError("Erro: O id da matrícula deve ser uma string!")
        
        matricula_limpa = valor.strip().upper()

        padrao_matricula = r'^MAT-\d{4}-\d{4}$'

        if not re.match(padrao_matricula, matricula_limpa):
            raise ValueError("Erro: Matrícula inválida! Use o padrão MAT-ANO-0000 (Ex: MAT-2026-0001).")
        
        else:
            self._id_matricula = matricula_limpa

    @property
    def turma_associada(self):
        """Retorna o objeto ou identificador da turma do aluno."""
        return self._turma_associada
    
    @turma_associada.setter
    def turma_associada(self, valor):
        if hasattr(valor, 'id_turma'):
            self._turma_associada = valor
        elif isinstance(valor, str):
            self._turma_associada = valor
        elif valor is None:
            self._turma_associada = None
        else:
            raise ValueError("Erro: turma_associada deve ser um objeto Turma ou uma string identificadora.")
        
    # -------
    # MÉTODOS
    # -------

    def get_permissao(self):
        """Retorna as permissões específicas do aluno no sistema."""
        return "Aluno: Acesso a materiais didáticos, consulta de notas e horários."
    
    def exibir_perfil(self):
        """Exibe o perfil formatado do aluno."""
        print("\n" + "="*35)
        print(f"🎓 PERFIL DO ALUNO: {self.nome}")
        print("="*35)
        print(f"Matrícula: {self.id_matricula}")
        print(f"Turma:     {self.turma_associada}")
        print(f"E-mail:    {self.email}")
        print(f"Status:    {self.status}")
        print("="*35 + "\n")

    def ver_frequencia(self):
        """Simula a visualização da frequência escolar."""
        print(f"📊 Frequência de {self.nome}: 92% de presença confirmada.")

    def ver_horario(self):
        """Simula a visualização da grade horária da turma."""
        nome_t = self.turma_associada.nome if hasattr(self.turma_associada, 'nome') else self.turma_associada
        print(f"📅 Horário da Turma {nome_t}: Segunda a Sexta, 08:00 - 12:00.")   

    def ver_noticias(self):
        """Visualiza avisos gerais da escola."""
        print(f"🔔 Notícia: A feira de ciências StudyForge será no próximo mês!")

    def baixar_material(self, material):
        """Simula o download de um conteúdo enviado pelo professor."""
        titulo = material.titulo if hasattr(material, 'titulo') else material
        print(f"⬇️ Iniciando download do material: '{titulo}'...")

    def to_dict(self):
        """Sobrescreve o to_dict para incluir dados específicos de Aluno."""
        dados = super().to_dict()
        
        id_t = self.turma_associada.id_turma if hasattr(self.turma_associada, 'id_turma') else self.turma_associada
        
        dados.update({
            "id_matricula": self.id_matricula,
            "id_turma": id_t,
            "notas": self._notas 
        })
        return dados