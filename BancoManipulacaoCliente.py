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
# irá receber como argumento o cpf (que será utilizado na criação da sessão do usuário que tem como objetivo, evitar que as ações de um
# usuário prejudiquem outros) e a senha.
def tela_login_cliente(cpf, senha):
   
   # Irá inspecionar o bloco de código com o objetivo de capturar possiveis erros.
    try:
        
        # Ira realizar a conexão com o banco de dados. 
        conexao = conectar()
        
        # Ira realizar a comunicação com o servidor (envio de requisições)
        cursor = conexao.cursor()
        
        # Ira selecionar a senha do cpf informado pelo cliente (comando
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


# Função que irá realizar consultas no banco de dados com o objetivo de 
# exibir os livros disponíveis no sistema.
def exibir_livros_disponiveis():
    
    # Ira inspecionar o bloco de código com o objetivo de capturar possiveis
    # erros de execução do trecho de código.
    try:
         
        # Ira chamar a função que nos conecta ao servidor
        conexao = conectar()
        
        # Será responsável por enviar requisições ao servidor (a requisição
        # GET no caso)
        cursor = conexao.cursor()
        
        # Ira conter o comando que seleciona todas as informações dos livros
        # cadastrados
        selecao = "SELECT * FROM livros"
        
        # Ira executar a ci=onsulta e enviar a requisição ao servidor
        cursor.execute(selecao)
        
        # Ira armazenar o valor de todas as linhas da tabela de livro
        livros = cursor.fetchall()
        
        # A diferença entre fetchall e fetchone:
        # fetchall: Pega todas as linhas encontradas pela busca de uma vez
        # fetchone: Pega apenas uma única linha (a próxima da fila)
        
        # Ira verificar se há tabela possui valores, ou seja, se a tabela possui livros cadastrados. 
        if len(livros) > 0:
            
            # Se houver livros cadastrados, iremos percorrer a variável
            # livro que contém os resultados armazenados com o objetivo de
            # imprimir as informações na tela.
            for livro in livros:

                print(livro)
                print("---------------------------------------------------------------")
                

        else:
            
            # Mensagem que será impressa caso a tabela não tenha livros cadastrados.
            print("Não há livros disponíveis no momento")

    except pymysql.ProgrammingError as erro:
        
        # Ira tratar erros de lógica ou sintaxe     
        print("Erro de sintaxe ou lógica: ", erro)
    
    except pymysql.OperationalError as erro:
        
        # Ira tratar erros de comunicação com o servidor
        print("Falha na comunicação com o servidor: ", erro)
    
    finally:
        
        # Irá encerrar a conexão com o objetivo de evitar vazamento de dados.
        conexao.close()


# Função que possibilitara o cliente alugue livros no sistema usando como
# argumento o cpf do usuário logado no sistema e o isbn do livro que será
# alugado.
def criarAluguel(cpf_logado, isbn):
    
    # Irá inspecionar o bloco de código com o objetivo de capturar possiveis
    # erros.
    try:
        
        # Irá conectar o usuário ao servidor.
        conexao = conectar()
        
        # Irá enviar as requisições ao servidor.
        cursor = conexao.cursor()
        
        # Ira consultar o isbn solicitado pelo usuário com o objetivo
        # de verificar a existência do livro no sistema.
        selecao_isbn = "SELECT isbn FROM livros WHERE isbn = %s"
        
        # Ira enviar a consulta ao servidor.
        cursor.execute(selecao_isbn, (isbn))
        
        # Ira armazenar apenas uma linha do banco (Linha que contém o isbn informado).        
        resultado = cursor.fetchone()
        
        if resultado is None:
            
            # Se o isbn não for encontrado vamos imprimir essa mensaegem.
            # e dar um return que encerrá a execução do bloco e evitar
            # a inserção do dado passado pelo usuário.
            print("Livro não encontrado")
            
            return

        # Comando que irá inserir dados no sistema.
        # CURDATE(): Ira pegar a data e a hora atual do sistema
        # INTERVAL 30 DAY: Irá calcular os 30 dias (baseado no dia
        # do aluguel)
        insercao_aluguel = "INSERT INTO alugueis (cpf_cliente, isbn_do_livro, data_devolucao) VALUES (%s, %s, CURDATE() + INTERVAL 30 DAY)"

        # Irá enviar a inserção para o servidor.
        cursor.execute(insercao_aluguel, (cpf_logado, isbn))
        
        # Irá atualizar o estoque de livros após o aluguel
        atualizar_estoque = "UPDATE livros SET quantidade = quantidade - 1 WHERE isbn = %s"
        
        # Irá enviar a atualização para o servidor.
        cursor.execute(atualizar_estoque, (isbn))

        # Irá gravar a inserção na base de dados.
        conexao.commit()

        # Mensagem de sucesso.
        print("Livro alugado com sucesso")
    
    except pymysql.ProgrammingError as erro:
        
        # Ira tratar erros de lógica ou sintaxe, como por exemplo,
        # a inserção de um dado que já existe.
        print("Erro de sintaxe ou lógica: ", erro)
    
    except pymysql.OperationalError as erro:
        
        # Ira tratar erros na comunicação com o servidor
        print("Falha na comunicação com o servidor: ", erro)
    
    finally:
        
        # Irá encerrar a conexão com o banco de dados com o intuito de
        # evitar o vazamento de dados.
        conexao.close()


# Função que tem como objetivo exibir os livros alugados pelo usuário
# usando como argumento o cpf do usuário logado.  
def exibir_livros_alugados(cpf_logado):
    
    # Irá inspecionar o bloco de código com o objetivo de capturar possiveis erros
    # de execução do bloco.
    try:
        
        # Irá conectar o usuário ao servidor.
        conexao = conectar()
        
        # Irá enviar as requisições ao servidor.
        cursor = conexao.cursor()
        
        # Irá consultar os livros alugados na tabela de aluguéis
        selecao_livro_alugado = "SELECT * FROM alugueis WHERE cpf_cliente = %s"
        
        # Irá enviar a consulta ao servidor.
        cursor.execute(selecao_livro_alugado, (cpf_logado,))
        
        # Ira armazenar todas as linhas do banco
        resultados = cursor.fetchall()
        
        # Observação: Vamos usar o len na verificação por conta da diferença
        # de retorno entre o fetchone e o fetchall. 
        
        # Fetchone: Se o fetchone não encontrar nada, ele retorna None. Por 
        # isso, o  if resultado is None funciona perfeitamente para verificar a existência de um determinado dado
        
        # Fetchall: Já o fetchall retorna uma lista vázia caso a tabela não
        # tenha os dados consultados. Por isso, é mais eficiente verificar
        # o tamanho da lista para descobrir a existência dos dados.
        if  len(resultados) == 0:
            
            # Se o usuário não tiver livros alugados, iremos imprimir essa mensagem
            print("Não há livros alugados no momento")
        
        else:
            
            # Se o usuário tiver livros alugados, iremos imprimir essa mensagem
            print("Livros alugados: ")
            
            # Após a impressão da mensagem, vamos percorrer a variável resultados
            # (que contém a lista de valores encontrados) com o objetivo de mostra-los
            # na tela.
            for livros in resultados:
                
                print(livros)
    
    except pymysql.ProgrammingError as erro:
        
        # Ira tratar erros relacionados a sintaxe ou lógica
        print("Erro de sintaxe ou lógica: ", erro)
    
    except pymysql.OperationalError as erro:
        
        # Ira tratar erros na comunicação com o servidor
        print("Falha na comunicação com o servidor: ", erro)
    
    finally:
        
        # Ira encerrar a conexão com o banco para evitar vazamento de dados.
        conexao.close()

# Ira atualizar os dados cadastrais do usuário usando como  argumento o nome,
# o telefone, o email e o cpf logado no sistema.
def atualizar_dados( nome, telefone, email, cpf_logado):
    
    try:
        
        # Ira conectar o usuário com o banco de dados.
        conexao = conectar()
        
        # Ira enviar as requisições ao servidor.
        cursor = conexao.cursor()
        
        # Ira conter o comando de atualização dos dados (de forma segura).
        consulta = "UPDATE clientes SET nome = %s, telefone = %s, email =  %s WHERE cpf = %s"
        
        # Irá atualizar os dados no servidor.
        cursor.execute(consulta, (nome, telefone, email, cpf_logado))
        
        # Ira gravar a atualização no servidor
        conexao.commit()
        
        # Mensagem de sucesso.
        print("Dados atualizados com sucesso")
        
    except pymysql.ProgrammingError as erro:
        
        # Ira tratar erros de sintaxe ou lógica
        print("Erro de sintaxe ou lógica: ", erro)
    
    except pymysql.OperationalError as erro:
        
        # Ira tratar erros relacionados a comunicação com o servidor      
        print("Falha na comunicação com o servidor: ", erro)
    
    finally:
        
        # Ira fechar a conexão para evitar vazamento de dados
        conexao.close()
        
        

# Função que irá atualizar a senha do usuário usando como argumento 
# a senha nova e o cpf do cliente logado
def atualizar_senha(senha_nova, cpf_logado):

    try:
        
        # Ira conectar o usuário ao servidor
        conexao = conectar()
        
        # Ira enviar as requisições ao servidor
        cursor = conexao.cursor()
        
        # O salt é uma sequência aleatória de bytes exclusiva que
        # é misturada a senha antes do hash. O argumento rounds=12
        # define o número de iterações, aumentando a segurança e o tempo de processamento.
        sequencia_aleatoria_de_bytes = bcrypt.gensalt(rounds=12)  
        
        # Codificação: O bcycrypt (assim como a maioria das funções 
        # criptografadas) só trabalha com bytes (dados binários), não
        # com strings de texto comuns. Esta linha converte a senha de 
        # texto para o formato de bytes, usando a codificação universal utf-8
        senha_bytes = senha_nova.encode('utf-8')
        
        # Hashing: Esta é a etapa principal, o bcrypt pega senha (em bytes) e a sequencia aleatória de bytes (salt) e as mistura,
        # aplicando o algoritmo de hashing. O resultado é o hash final,
        # que é unidirecional (não pode ser revertido).
        senha_hash = bcrypt.hashpw(senha_bytes, sequencia_aleatoria_de_bytes)
        
        # Armazenamento: O resultado do bcrypt.hashpw é um objeto
        # bytes. Como a coluna do nosso banco de dados (senha) é do
        # tipo varchar, esta linha converte o hash de volta para uma
        # string de texto.
        senha_hash_string = senha_hash.decode('utf-8')
       
       # Comando que irá atualizar a senha do usuário 
        update_senha = "UPDATE clientes SET senha = %s WHERE cpf = %s"
        
        # Irá enviar a requisição ao servidor
        cursor.execute(update_senha, (senha_hash_string, cpf_logado))
        
        # Irá gravar a atualização no servidor.
        conexao.commit()
        
        # Mensagem de sucesso.
        print("Senha atualizada com sucesso")
        
    except pymysql.ProgrammingError as erro:
        
        # Ira tratar erros de lógica ou sintaxe
        print("Erro de sintaxe ou lógica: ", erro)
    
    except pymysql.OperationalError as erro:
        
        # Ira tratar erros na comunicação com o servidor.
        print("Falha na comunicação com o servidor: ", erro)
    
    finally:
        
        # Irá encerrar a conexão com o objetivo de evitar vazamento de dados.
        conexao.close()

# Função que irá excluir a conta do usuário usando o cpf e a senha
def excluir_conta(cpf_logado, senha):
    
    # Irá inspecionar o bloco de código com o objetivo de capturar
    # possiveis erros de execução do bloco.
    try:
        
        # Ira conectar o usuário ao servidor.
        conexao = conectar()
       
       # Irá enviar requisições ao servidor         
        cursor = conexao.cursor()
        
        # Irá conter o comando que irá consultar se a senha informada
        # existe no sistema (de forma segura)
        consulta_senha = "SELECT senha FROM clientes WHERE cpf = %s"
        
        # Irá enviar a consulta ao servidor
        cursor.execute(consulta_senha, (cpf_logado))
        
        # irá conter o resultado da consulta (O hash da senha ou o  None caso a senha não exista). o fetchone irá armazenar apenas a linha
        # que contém o hash da senha.
        resultado_senha = cursor.fetchone()
        
        # Ira armzenar a senha criptografada encontrada no servidor
        senha_criptografada = resultado_senha[0]
        
        # Ira transformar senha informada e a senha criptografa em um conjunto de bytes (núemeros binários) com o objetivo de 
        # tornar as 2 senhas iguais (em relação ao tipo do dado). 
        senha_informada = senha.encode('utf-8')
            
        hash_bytes = senha_criptografada.encode('utf-8')
        
        # Após transformar as senhas em um conjunto de bytes,
        # vamos usar a função checkpw da biblioteca bcrypt
        # que irá verificar se as senhas são iguais (até onde
        # entendi, ele vai verificar se os valores em bytes
        # das senhas são iguais).
        if bcrypt.checkpw(senha_informada, hash_bytes):

                # Se a senha existir, vamos iniciar o processo de
                # exclusão da conta. Como o cpf do cliente é chave
                # estrangeira da tabela de alugueis (que contém os
                # alugueis dos clientes), é necessário excluir não
                # só a conta, como também os alugueis do cliente 
                # que solicitou a exclusão.
                
                # Ira conter o comando que irá excluir os alugueis
                # do cliente.
                exclusao_alugueis = "DELETE FROM alugueis WHERE cpf_cliente = %s"
                
                # Irá enviar a requisição de exclusão ao servidor
                # (exclusão dos aluguéis)
                cursor.execute(exclusao_alugueis, (cpf_logado))
                
                # Irá conter o comando de exclusão dos dados do cliente
                exclusao_cliente = "DELETE FROM clientes WHERE cpf = %s"
                
                # Ira enviar a requisição de exclusão ao servidor
                # (exclusão do cliente).
                cursor.execute(exclusao_cliente, (cpf_logado))
                
                # Ira gravar a exclusão no servidor
                conexao.commit()
                      
                # Mensagem de sucesso.          
                print("Conta excluída com sucesso")
            
        else:
                # Mensagem que será impressa se a senha informada
                # não existir.
                print("Senha incorreta, tente novamente")
    
    except pymysql.ProgrammingError as erro:
        
        # Ira tratar erros relacionados a sintaxe ou lógica
        print("Erro de sintaxe ou lógica: ", erro)
    
    except pymysql.OperationalError as erro:
        
        # Ira tratar erros na comunicação com o servidor
        print("Falha na comunicação com o servidor: ", erro)
    
    finally:
        
        # Ira encerrar a conexão com o banco de dados
        conexao.close()
    
        
        

        
    
    