# Cadastro de livros em python e mysql
Exercicio em python e mysql que tem como objetivo cadastrar clientes, funcionários e livros. Nesse projeto, iremos realizar 
apenas o back-end desse sistema, pois, o objetivo do projeto é por em prática os conhecimentos adquiridos nas aulas de
python com mysql

Linguagens utilizadas: python 3.12.10 e mysql 10.4.32


                        Estrutura das tabelas

-> Clientes: cpf(chave primária), nome, telefone, email, senha

-> Funcionários: nome, senha, id (chave primária)

-> Livro: ISBN (chave primária), Titulo, Autor, Ano de Publicação, quantidade, data de atualização de estoque

-> Alugúeis: id, cpf do cliente (chave estrangeira), isbn do livro(chave estrangeira), data do aluguel, data da
devolução.

Observação: A tabela aluguéis terá como objetivo utilizar as chaves estrangeiras para interligar as tabelas clientes e livros com o objetivo
de conseguirmos registrar todos os alugúeis feitos no sistema. 

                         Componentes do sistema

Tela de Login Para Clientes: Local onde os clientes irão realizar o seu 
login no sistema

Tela de login para funcionários: Tela onde os funcionarios poderão
realizar o seu login no sistema

Tela de cadastro de clientes: Tela onde os clientes irão criar cadastros
no sistema

Tela de cadastro de funcionários: Tela onde os funcionários irão criar
cadastros no sistema (somente funcionários podem cadastrar funcionários)

Tela de cadastro de livros: Tela onde apenas os funcionários poderão cadastrar livros

Tela de atualização de estoques de livros: Tela onde o funcionário poderá
atualizar a quantidade de estoques de livros.

Tela de exclusão de livros: Tela que o funcionário podera excluir livros.

Tela de livros disponiveis: Irá conter as informações de todos os livros
cadastrados pelos funcionários

Tela de livros alugados pelos clientes: irá conter as informações dos livros que o cliente logado
no sistema alugou.

Tela de atualização de cadastros de clientes: Tela que o usuário irá atualizar os dados (o telefone por exemplo)

Tela de atualização de senha de funcionários: Tela que o funcionário poderá atualizar a sua senha.

Tela de exclusão de funcionários: Onde funcionários podem excluir outros funcionários.


                            Regras do sistema

-> Um cliente pode alugar quantos livros ele quiser

-> Somente funcionários podem cadastrar outros funcionários

-> Somente funcionários podem excluir funcionários

-> Todos os clientes deverão ficar apenas 30 dias com os livros