# Arquivo que irá conter a criação e manipulação do banco de dados

# Criando a conexão com o banco de dados

# In[ ]:


# Import da biblioteca pymysql que tem como objetivo conectar o python 
# a um servidor mysql
import pymysql

# Import da biblioteca que implementa o algoritmo de hadhing
# que protege os dados com criptografia.
import bcrypt



# Função da biblioteca connect que irá conectar o python com o mysql
# usando a função connect que recebe como argumento:

# host: endereço do servidor que conterá o banco de dados criado no sistema.

# user: Nome do usuário que irá criar e utilizar o banco de dados (podemos
# ter mais de um user com privilégios diferentes).

# password: Senha de acesso ao servidor.

def conectar():
    
    conexao = pymysql.connect(
        
        host = 'localhost',
        
        user = 'root',
        
        password = '',
        
        database = 'livraria'
    )
    
    return conexao


# Função que irá cadastrar clientes no sistema da biblioteca usando os
# argumentos cpf, nome, telefone, email, senha
def cadastracliente(cpf, nome, telefone, email, senha):
    
    # Ira inspecionar o bloco de código com o objetivo de capturar
    # possiveis erros de execução do trecho de código
    try:
        
        # Ira conter a conexão com o banco de dados
        conexao = conectar()
        
        # Ira conter a função que envia requisições ao servidor.
        cursor = conexao.cursor()
        
        # O salt é uma sequência aleatória de bytes exclusiva que
        # é misturada a senha antes do hash. O argumento rounds=12
        # define o número de iterações, aumentando a segurança e o tempo de processamento.
        sequencia_aleatoria_de_bytes = bcrypt.gensalt(rounds=12)  
        
        # Codificação: O bcycrypt (assim como a maioria das funções 
        # criptografadas) só trabalha com bytes (dados binários), não
        # com strings de texto comuns. Esta linha converte a senha de 
        # texto para o formato de bytes, usando a codificação universal utf-8
        senha_bytes = senha.encode('utf-8')
        
        # Hashing: Esta é a etapa principal, o bcrypt pega senha (em bytes) e a sequencia aleatória de bytes (salt) e as mistura,
        # aplicando o algoritmo de hashing. O resultado é o hash final,
        # que é unidirecional (não pode ser revertido).
        senha_hash = bcrypt.hashpw(senha_bytes, sequencia_aleatoria_de_bytes)
        
        # Armazenamento: O resultado do bcrypt.hashpw é um objeto
        # bytes. Como a coluna do nosso banco de dados (senha) é do
        # tipo varchar, esta linha converte o hash de volta para uma
        # string de texto.

        senha_hash_string = senha_hash.decode('utf-8')
        
        # Ira conter o comando sql que insere dados no sistema (de maneira segura) usando 's%' que evitam
        # a injeção sql no banco de dados.
        sql_query = f"INSERT INTO clientes (cpf, nome, telefone, email, senha) VALUES(%s, %s, %s, %s, %s)"
        
        # Ira executar o comando usando os argumentos que irão substituir
        # os '%s'
        cursor.execute(sql_query, (cpf, nome, telefone, email, senha_hash_string))
        
        # Ira gravar a inserção no servidor
        conexao.commit()
        
        print("Cliente cadastrado com sucesso!")
        
    except pymysql.ProgrammingError as erro:
        
        # Ira tratar erros de lógica como inserção de dados que já existem
        print("Erro ao cadastrar o cliente, por favor verifique se o seu cadastro já existe no sistema: ", erro)
        
    
    except pymysql.OperationalError as erro:
        
        # Ira tratar erros de conexão com o servidor.
        print("Falha na comunicação com o servidor: ", erro)

    finally:
        
        # Bloco que será executado independente do resultado da execução
        # do trecho (bem ou mal sucedida)
        
        # Ira fechar a conexão com o servidor com o objetivo de evitar vazamento de dados
        conexao.close()
    

# Função que irá permitir que o usuário faça login no sistema. A função
# irá receber como argumento o cpf (que será utilizado na criação da sessão do usuáfrio que tem como objetivo, evitar que as ações de um
# usuário prejudiquem outros) e a senha.
def tela_login_cliente(cpf, senha):
   
   # Irá inspecionar o bloco de código com o objetivo de capturar possiveis erros.
    try:
        
        # Ira realizar a conexão com o banco de dados. 
        conexao = conectar()
        
        # Ira realizar a comunicação com o servidor (envio de requisições)
        cursor = conexao.cursor()
        
        # Ira selecionar a senha do cpf informado pelo cliente (comand
        # executado da maneira segura)
        selecao = "SELECT senha FROM clientes WHERE cpf = %s"
        
        # Ira executar o comando sql
        cursor.execute(selecao, (cpf))
        
        # Ira usar a função fetchone que armazena o valor selecionado
        # pelo cursor (no caso a senha do cpf informado)
        resultado = cursor.fetchone()
        
        # Se a variável não tiver nenhum resultado, ou seja, uma senha,
        # significa que o cpf informado não foi encontrado no sistema.
        if resultado is None:
            
            # Se essa condição for verdadeira, vamos imprimir
            # essa mensagem retornar o valor None (que impedirá
            # a criação da sessão)
            print("O cpf incorreto, tente novamente")
            
            return None
        
        # Após a validação do cpf (que irá atribuir a variável senha_criptografada o None ou a senha requisitada), vamos
        # acessar o valor selecionado (a senha ou o none) com o
        # objetivo de iniciar a verificação da senha. 
        senha_criptografada = resultado[0]
        
        # Irá transformar a senha informada e a senha criptograda
        # em uma sequência de bytes (números binários) com o objetivo
        # de padronizar os dados para a comparação no checkpw
        senha_informada = senha.encode('utf-8')
        
        hash_bytes = senha_criptografada.encode('utf-8')
        
        # Irá verificar se a senha informada é igual a senha
        # armazenada no banco de dados usando a função checkpw
        # da biblioteca bcrypt que retorna um valor booleano
        # onde True é que as senhas são iguais e False quando
        # a senha é diferente. A função recebe como argumento
        # a senha informada e a senha armazenada (senha criptografada
        # no sistema).
        if bcrypt.checkpw(senha_informada, hash_bytes):
            
            # Se a condição for verdadeira, vamos imprimir essa mensagem
            # e retornar o cpf informado pelo usuário para a criação da 
            # sessão.
            print("Login realizado com sucesso")
            
            return cpf
        
        else:
            
            # Caso contrário, mostraremos essa mensagem e retornaremos
            # o None que não criará a sessão do usuário.
            print("Senha incorreta, tente novamente")
            
            return None
        
        
                   
    except pymysql.ProgrammingError as erro:
        
        # Irá tratar erros relacionados a sintaxe ou lógica    
        print("Falha na realização do login: ", erro)
    
    except pymysql.OperationalError as erro:
        
        # Ira tratar erros na comunicação com o servidor
        print("Falha na comunicação com o servidor: ", erro)
    
    finally:
        
        # Ira encerrar a conexão com o objetivo de evitar o vazamento
        # de dados.
        conexao.close()
            