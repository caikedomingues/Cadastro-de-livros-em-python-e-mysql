# Arquivo que irá conter a criação e manipulação do banco de dados

# Criando a conexão com o banco de dados

# In[ ]:


# Import da biblioteca pymysql que tem como objetivo conectar o python 
# a um servidor mysql
import pymysql

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



