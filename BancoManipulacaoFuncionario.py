

# Conexao com o banco de dados

# Biblioteca que irá realizar a comunicação do python com o mysql
import pymysql

# Biblioteca que tem como objetivo Criptografar as senhas que serão enviadas para 
# o banco de dados.
import bcrypt

# Função que irá conectar o pythin ao servidor mysql que conterá o nosso banco de dados.
def conectar():
    
    
    # Função da biblioteca pymysql que tem como objetivo realizar a conexão usando os
    # argumentos:
    # host: Endereço do servidor que contém o banco de dados
    # user: Usuário administrador do banco de dados
    # password: Senha de acesso do banco de dados.
    # database: Nome do banco de dados que será utilizado.
    conexao = pymysql.connect(
        
        host = 'localhost',
        
        user = 'root',
        
        password = '',
        
        database = 'livraria'
        
    )
    
    # Retorno da conexão com o banco de dados.
    return conexao


# Função que irá cadastrar funcionários no sistema de bibliotecas. A função 
# irá receber como argumento o nome e a senha do funcionário.
def cadastroFuncionario(nome, senha):
    
    
    # Irá inspecionar o bloco de código com o objetivo de capturar possiveis erros.
    try:
        
        # Ira conter a conexão com o banco de dados.
        conexao = conectar()
        
        # Será responsável por enviar requisições ao servidor.
        cursor = conexao.cursor()
        
        # Irá gerar uma sequência aleatória de bytes (numeros binários)
        # durante 12 iterações (valor do round) que irá executar esse 
        # trecho 12 vezes com o objetivo de gerar a melhor sequência aleatória
        # possível.
        sequencia_aleatoria_de_bytes = bcrypt.gensalt(rounds=12)
        
        # Ira transformar a senha informada em um conjunto de bytes (dados binários)
        senha_bytes = senha.encode('utf-8')
        
        # Ira misturar a senha informada (em bytes) com a sequência de bytes aleatórios
        # com o objetivo de criar a criptografia da senha.
        senha_hash = bcrypt.hashpw(senha_bytes, sequencia_aleatoria_de_bytes)
        
        # Ira transformar a senha criptografada em um valor do tipo string com o
        # objetivo de conseguirmos inserir o dado no campo de senha.
        senha_hash_string = senha_hash.decode('utf-8')
        
        # Ira conter o comando que irá inserir os dados do funcionário no sistema
        # (inserção de maneira segura)
        sql_query = "INSERT INTO funcionarios (nome, senha) VALUES(%s, %s)"
        
        # Ira executar o comando usando os argumentos da função que irão
        # substituir os '%s'
        cursor.execute(sql_query, (nome, senha_hash_string))
        
        # Ira gravar a inserção no servidor  
        conexao.commit()
        
        # Ira retornar o id do funcionário cadastrado.
        id_gerado = cursor.lastrowid
        
        # Mensagem de sucesso
        print("Funcionário cadastrado com sucesso")

        print("Seu id de login é: ", id_gerado)
        
    except pymysql.ProgrammingError as erro:
        
        # Ira lidar com erros relacionados a lógica ou sintaxe, como por exemplo, inserção de dados que já
        # existem no sistema
        print("Erro ao cadastrar o funcionário, por favor verifique se o seu cadastro já existe no sistema: ", erro)
    
    
    except pymysql.OperationalError as erro:
        
        # Irá lidar com erros relacionados a comunicação com o servidor (como falhas na conexão)
        print("Falha na comunicação com o servidor: ", erro)
    
    finally:
        
        # Ira encerrar a conexão com o objetivo de evitar o vazamento de dados
        conexao.close()




def tela_login_funcionario(id, senha):
    
    try:
        conexao = conectar()
        
        cursor = conexao.cursor()
        
        selecao = "SELECT senha FROM funcionarios WHERE id = %s"
        
        cursor.execute(selecao, (id))
        
        resultado = cursor.fetchone()
        
        if resultado is None:
            
            print("O id informado não existe no sistema")
            
            return None
        
        senha_criptografada = resultado[0]
        
        senha_informada = senha.encode('utf-8')
        
        hash_bytes = senha_criptografada.encode('utf-8')
        
        if bcrypt.checkpw(senha_informada, hash_bytes):
            
            print("Login realizado com sucesso")
            
            return id
        
        else:
            
            print("Senha incorreta, tente novamente")
            
            return None
    
    except pymysql.ProgrammingError as erro:
        
        print("Falha na realização do login: ", erro)
    
    except pymysql.OperationalError as erro:
        
        print("Falha na comunicação com o servidor: ", erro)
    
    finally:
        
        conexao.close()


    
    
    
    