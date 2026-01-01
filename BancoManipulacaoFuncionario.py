

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



# Função que irá realizar o login de funcionarios usando como argumento
# o id e a senha do funcionário.
def tela_login_funcionario(id, senha):
    
    # Irá inspecionar o bloco de código com o objetivo de capturar possiveis erros de execução do código.
    try:
        
        # Ira chamar a conexão com o servidor
        conexao = conectar()
        
        # Irá enviar requisições ao servidor 
        cursor = conexao.cursor()
        
        # Ira selecionar a senha no banco com base no id informado
        # pelo usuário. (de forma segura)
        selecao = "SELECT senha FROM funcionarios WHERE id = %s"
        
        # Ira executar o comando usando o id informado pelo usuário
        cursor.execute(selecao, (id))
        
        # Ira armazenar a senha selecionada ou o None (caso
        # o id informado não exista no sistema)
        resultado = cursor.fetchone()
        
        if resultado is None:
            
            # Se o resultado for none, ou seja, se o id informado
            # não existir no sistema, vamos imprimir essa mensagem e 
            # retorna o valor None
            print("O id informado não existe no sistema")
            
            return None
        
        # Ira armazenar o valor da variável resultado 
        senha_criptografada = resultado[0]
        
        # Ira transformar a senha informada e a senha criptografada
        # em um conjunto de bytes (dados binarios) com o objetivo
        # de padronizar as senhas e realizar a verificação
        senha_informada = senha.encode('utf-8')
        
        hash_bytes = senha_criptografada.encode('utf-8')
        
        # Ira verificar o o resultado da função checkpw da biblioteca bcrypt que tem como objetivo verificar se a senha informada é
        # igual a senha criptografada.
        if bcrypt.checkpw(senha_informada, hash_bytes):
            
            # Se o resultado da função for verdadeiro vamos
            # imprimir essa mensagem e retornar o id do usuário
            # para a criação da sessão do funcionário
            print("Login realizado com sucesso")
            
            return id
        
        else:
            
            # Se a senha estiver incorreta, vamos imprimir essa mensagem
            # e retornar o valor None que tem impedira a criação da
            # sessão.
            print("Senha incorreta, tente novamente")
            
            return None
    
    except pymysql.ProgrammingError as erro:
        
        # Irá lidar com erros relacionados a lógica ou sintaxe
        print("Falha na realização do login: ", erro)
    
    except pymysql.OperationalError as erro:
        
        # Ira lidar com erros na comunicação do servidor
        print("Falha na comunicação com o servidor: ", erro)
    
    finally:
        
        # Ira fechar a conexão com o objetivo de evitar o vazamento de
        # dados
        conexao.close()


# Função que irá possibilitar que funcionários cadastrem livros no sistema usando os argumentos isbn, titulo, autor, ano de publicação e quantidade     
def cadastrarLivro(isbn, titulo, autor, ano_publicacao, quantidade):
    
    # Irá inspcionar o bloco de código com o objetivo de capturar 
    # possiveis erros. 
    try:
        
        # Ira chamar a função que conecta o python ao banco de dados
        conexao = conectar()
        
        # Sera responsável por enviar os comandos sql (requisições)
        # ao servidor.
        cursor = conexao.cursor()
        
        # Ira conter o comando de inserção do mysql (de forma segura)
        insercao = "INSERT INTO livros (isbn, titulo, autor, ano_publicacao, quantidade) VALUES (%s, %s, %s, %s, %s)"
        
        # Ira executar (enviar a requisição) o comando sql 
        cursor.execute(insercao, (isbn, titulo, autor, ano_publicacao, quantidade))

        # Ira gravar a inserção no servidor.
        conexao.commit()
        
        # Mensagem de sucesso da inserção
        print("Livro cadastrado com sucesso")
    
    except pymysql.ProgrammingError as erro:
        
        # Irá tratar erros relacionados a sintaxe ou lógica, como por exemplo,
        # inserção de dados que já existem no sistema
        print("Erro ao cadastrar o livro: ", erro)
    
    except pymysql.OperationalError as erro:
        
        # Ira tratar os erros relacionados a comunicação com o servidor.
        print("Falha na comunicação com o servidor: ", erro)
    
    finally:
        
        # Ira encerrar a conexão com o objetivo de evitar vazamento de dados.
        conexao.close()
    


# Ira atualizar o estoque de livros cadastrados no sistema. A função
# irá receber como argumento o isbn do livro e a quantidade de novos
# produtos no estoque
def atualiza_estoque_livro(isbn, quantidade):
    
    # Irá inspecionar o bloco de código com o objetivo de capturar possiveis
    # erros de execução.
    try:
        
        # Ira conectar o usuário com o servidor do sistema
        conexao = conectar()
        
        # Sera responsável por enviar requisições ao servidor
        cursor = conexao.cursor()
        
        # Ira selecionar a quantidade do isbn (livro) solicitado. (de
        # forma segura).
        selecao = "SELECT quantidade FROM livros WHERE isbn = %s"
        
        # Ira enviar a requisição ao servidor
        cursor.execute(selecao, (isbn))
        
        # Ira armazenar o valor da quantidade atual de livros no
        # estoques.
        resultado = cursor.fetchone()
        
        if resultado is None:
            
            # Se o isbn nao for encontrado iremos imprimir essa mensagem
            # e dar um return que irá encerrar a execução do bloco.
            print("Livro não encontrado")
            
            return
        
        # Ira acessar a quantidade atual de estoques do livro solicitado
        resultado = resultado[0]
        
        # Comando que irá atualizar os dados no banco de dados (de forma
        # segura).
        atualizacao_estoque = "UPDATE livros SET quantidade = %s + %s WHERE isbn = %s"
        
        # Ira executar (enviar a requisição) o comando de atualização de
        # estoque
        cursor.execute(atualizacao_estoque, (resultado, quantidade, isbn))
        
        # Ira gravar a atualização no servidor
        conexao.commit()
        
        # Mensagem de sucesso.
        print("Estoque atualizado com sucesso")
        
    except pymysql.ProgrammingError as erro:
        
        # Ira tratar erros relacionados a lógica ou sintaxe
        print("Erro ao atualizar o estoque: ", erro)
    
    except pymysql.OperationalError as erro:
        
        # Ira tratar falhas na comunicação com o servidor
        print("Falha na comunicação com o servidor: ", erro)
        
    finally:
        
        # Ira encerrar a conexão com o objetivo de evitar o vazamento
        # de dados.
        conexao.close()


# Função que irá excluir livros do sistema usando como argumento o isbn.
def excluirLivro(isbn):
    
    # Irá inspecionar o bloco com o objetivo de capturar possiveis
    # erros.
    try:
        
        # Ira conectar o usuário com o servidor.
        conexao = conectar()
        
        # Irá enviar as requisições ao servidor.
        cursor = conexao.cursor()
        
        # Ira selecionar o livro solicitado usando o isbn (de forma
        # segura usando o '%s').
        selecao = "SELECT isbn FROM livros WHERE isbn = %s"
        
        # Ira enviar seleçao para o servidor.
        cursor.execute(selecao, (isbn))
        
        # Ira armazenar o valor da selecão (o isbn ou o None, caso o
        # valor não exista).
        resultado = cursor.fetchone()
        
        if resultado is None:
            
            # Se o resultado for None, ou seja, se o isbn não for
            # encontrado, vamos imprimir essa mensagem e dar um return
            # que encerra a execução do bloco de código.
            print("Livro não encontrado")
            
            return
        
        # Comando que irá executar a exclusão do livro solicitado
        exclusao = "DELETE FROM livros WHERE isbn = %s"
        
        # Ira enviar a exclusão para o servidor
        cursor.execute(exclusao, (isbn))
        
        # Ira gravar a exclusão do livro no servidor.
        conexao.commit()
        
        # Mensagem de sucesso.
        print("Livro excluido com sucesso")
        
    except pymysql.ProgrammingError as erro:
        
        # Ira tratar erros relacionados a lógica ou sintaxe
        print("Erro ao excluir o livro: ", erro)
    
    except pymysql.OperationalError as erro:
        
        # Ira tratar erros relacionados a comunicação do servidor
        print("Falha na comunicação com o servidor: ", erro)
    
    finally:
        
        # Irá encerrar a conexão com o banco de dados com o objetivo
        # de evitar o vazamento de dados.
        conexao.close()
    
def atualizar_senha(senha_nova, id_logado):
    
    #Irá inspecionar o bloco com o objetivo de capturar possiveis erros.
    try:
        
        # Ira conectar o usuário ao servidor.
        conexao = conectar()
        
        # Ira enviar as requisições ao servidor.
        cursor = conexao.cursor()
        
        # Ira criar uma sequência aleatória de bytes (numeros 
        # binários) que serão utilizados na criptografia da
        # senha. O round define a quantidade de vezes que o gensalt
        # irá ser executado com o objetivo de dificultar o processamento
        # do computador de um hacker caso ele tente "adivinhar" as senhas.
        sequencia_aleatoria_de_bytes = bcrypt.gensalt(rounds=12)  
        
        # Ira transformar a senha em bytes (numeros binários)
        senha_bytes = senha_nova.encode('utf-8')
        
        # Ira criptografar a senha usando os bytes da sequência aleatória
        # e o bytes da senha informada. 
        senha_hash = bcrypt.hashpw(senha_bytes, sequencia_aleatoria_de_bytes)
        
        # Ira transformar a senha criptografada em string, dessa maneira,
        # poderemos armazenar a senha no banco de dados.
        senha_hash_string = senha_hash.decode('utf-8')
        
        # Ira conter o comando que atualizara a senha do funcionário
        update_senha = "UPDATE funcionarios SET senha = %s WHERE id = %s"
        
        # Ira enviar a atualização ao servidor.
        cursor.execute(update_senha, (senha_hash_string, id_logado))
        
        # Ira gravar a atualização no servidor.
        conexao.commit()
        
        # Mensagem de sucesso.
        print("Senha atualizada com sucesso")
    
    
    except pymysql.ProgrammingError as erro:
        
        # Ira tratar erros de sintaxe ou lógica
        print("Erro de lógica ou sintaxe: ", erro)  
    
    except pymysql.OperationalError as erro:
        
        # Ira tratar falhas na comunicação com o servidor.
        print("Falha na comunicação com o servidor: ", erro)
    
        
        
    
   