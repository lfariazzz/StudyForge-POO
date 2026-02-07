from abc import ABC, abstractmethod
import re
from datetime import datetime
import json
import os

"""
Representa a entidade base para todos os usuários do sistema StudyForge. 
Esta é uma classe abstrata (ABC) que define os atributos e métodos comuns 
a todos os perfis (Professor, Aluno, Gestor e Secretario). Não deve ser 
instanciada diretamente.
"""
class Usuario(ABC):
    def __init__(self, nome, cpf, email, senha, telefone, data_nascimento, status=True):
        self._id = None 
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.data_nascimento = data_nascimento
        self.status = status

    #-----------------
    #GETTERS E SETTERS
    #-----------------

    @property
    def id(self):
        """Permite ler o ID, mas sem altera-lo diretamente"""
        return self._id
    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str):
            raise TypeError("Erro: Nome deve ser uma string!")
        padrao_nome = r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$'

        if not re.match(padrao_nome, valor):
            raise ValueError("Erro: Nome inválido! Use apenas letras.")
        else:
            self._nome = valor.strip().title()
            
    @property
    def cpf(self):
        return self._cpf
    
    @cpf.setter
    def cpf(self, valor):
        if not isinstance(valor, str):
            raise TypeError("Erro: O cpf deve ser uma string!")
        
        cpf_limpo = valor.replace(".", "").replace("-", "")

        if not cpf_limpo.isdigit():
            raise ValueError("Erro: O cpf só pode conter números!")
        if len(cpf_limpo) != 11:
            raise ValueError("Erro: O cpf tem que conter 11 dígitos!")
        else:
            self._cpf = cpf_limpo

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, valor):
        if not isinstance(valor, str):
            raise TypeError("Erro: O email deve ser uma string!")

        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(padrao, valor):
            raise ValueError("Erro: Formato de email inválido!")
        
        else:
            self._email = valor.lower().strip()

    @property
    def senha(self):
        return self._senha
    
    @senha.setter
    def senha(self, valor):
        if not isinstance(valor, str):
            raise TypeError("Erro: A senha deve ser uma string!")
        
        senha_limpa = valor.strip()

        if len(senha_limpa) < 8:
            raise ValueError("Erro: A senha deve ter no mínimo 8 caracteres!")
        if senha_limpa.isalpha():
            raise ValueError("Erro: A senha deve conter pelo menos um número ou caractere especial!")
        else:
            self._senha = senha_limpa

    @property
    def telefone(self):
        t = self._telefone
        if len(t) == 11:
            return f"({t[:2]}) {t[2:7]}-{t[7:]}"
        return f"({t[:2]}) {t[2:6]}-{t[6:]}"
    
    @telefone.setter
    def telefone(self, valor):
        if not isinstance(valor, str):
            raise TypeError("Erro: O telefone deve ser uma string!")
        
        tel_limpo = valor.replace("(", "").replace(")", "").replace("-", "").replace(" ", "").replace("-", "")

        if not tel_limpo.isdigit():
            raise ValueError("Erro: O telefone deve conter apenas números!")
        if len(tel_limpo) not in [10, 11]:
            raise ValueError("Erro: O telefone deve conter 10 ou 11 dígitos!")
        else:
            self._telefone = tel_limpo
    
    @property
    def data_nascimento(self):
        return self._data_nascimento.strftime("%d/%m/%Y")
    
    @data_nascimento.setter
    def data_nascimento(self, valor):
        if not isinstance(valor, str):
            raise TypeError("Erro: A data deve ser uma string no formato DD/MM/AAAA!")
        
        try:
            data_convertida = datetime.strptime(valor, "%d/%m/%Y")

            if data_convertida > datetime.now():
                raise ValueError("Erro: Data de nascimento inválida!")
            self._data_nascimento = data_convertida
        
        except ValueError:
            raise ValueError("Erro: Data inválida! Use o formato DD/MM/AAAA (ex: 02/08/2003).") 
        
    @property
    def status(self):
        return "Ativo" if self._status else "Inativo"
    
    @status.setter
    def status(self, valor):
        if not isinstance(valor, bool):
            raise TypeError("Erro: Status deve ser um bool (True ou False)!")
        else:
            self._status = valor

    #-------
    #MÉTODOS
    #-------

    @abstractmethod
    def get_permissao(self):
        """Método abstrato: cada subclasse (Aluno, Professor) 
        retornará sua própria string ou lista de permissões.
        """
        pass

    def exibir_perfil(self):
        """Exibe as informações básicas do Usuário"""
        print(f"\n--- Perfil do Usuário [{self.status}]")
        print(f"ID: {self.id}")
        print(f"Nome: {self.nome}")
        print(f"CPF: {self.cpf}")
        print(f"Email: {self.email}")
        print(f"Telefone: {self.telefone}")
        print(f"Data de Nascimento: {self.data_nascimento}")

    def autenticar(self, senha_tentativa):
        """Verifica se a senha coincide com a senha privada, True para Correta e False para Errada"""
        return self._senha == senha_tentativa.strip()

    def encerrar_sessao(self):
        """Lógica para log de saída do Sistema"""
        print(f"Sessão do usuário {self.nome} encerrada com sucesso.")

    def abrir_configuraçoes(self):
        """Simulação de abertura de menu de configurações."""
        print(f"Abrindo painel de configurações para: {self._email}...")

    def to_dict(self):
        return {
            "tipo": self.__class__.__name__,
            "id": self._id, 
            "nome": self._nome,
            "cpf": self._cpf,
            "email": self._email,
            "senha": self._senha,
            "telefone": self._telefone,
            "data_nascimento": self.data_nascimento,
            "status": self._status
        }

    def salvar_json(self):
        nome_base = f"{self.__class__.__name__.lower()}s.json"
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_db = os.path.join(diretorio_atual, "..", "database", nome_base)

        dados_lista = []

        if os.path.exists(caminho_db):
            try: 
                with open(caminho_db, "r", encoding="utf-8") as arq:
                    dados_lista = json.load(arq)
            except (json.JSONDecodeError, IOError):
                dados_lista = []

        usuario_existente = next((u for u in dados_lista if u.get("cpf") == self._cpf), None)

        if usuario_existente:

            self._id = usuario_existente["id"]
        else:

            if dados_lista:
                maior_id = max(u.get("id", 0) for u in dados_lista)
                self._id = maior_id + 1
            else:

                self._id = 1

        dados_atualizados = self.to_dict()
        encontrado = False
        for i, usuario_no_arquivo in enumerate(dados_lista):
            if usuario_no_arquivo.get("cpf") == self._cpf:
                dados_lista[i] = dados_atualizados
                encontrado = True
                break
        
        if not encontrado:
            dados_lista.append(dados_atualizados)

        try:
            with open(caminho_db, "w", encoding="utf-8") as arq:
                json.dump(dados_lista, arq, indent=4, ensure_ascii=False)
            print(f"✅ Sucesso: {self.nome} (ID: {self._id}) salvo em 'database/{nome_base}'.")
        except Exception as e:
            print(f"❌ Erro ao escrever no arquivo {caminho_db}: {e}")