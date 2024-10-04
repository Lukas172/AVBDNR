import pymongo
from datetime import datetime, timedelta

url =  "mongodb+srv://luser:dbps@cluster0.7wjux.mongodb.net/"

client = pymongo.MongoClient(url)

def adicionar_livro():
    
    try:
        ISBN = input("Insira o código de identificação único do livro: ")
        titulo = input("Insira o nome do livro: ")
        autor = input("Insira o autor do livro: ")
        genero = input("Insira o gênero do livro: ")
        ano = int(input("Insira o ano de publicação do livro: "))
        quantidade = int(input("Insira a quantidade de exemplares disponíveis do livro: "))  # Convertendo para int

        livro = {
            'ISBN': ISBN,
            'titulo': titulo,
            'autor': autor,
            'genero': genero,
            'ano': ano,
            'quantidade': quantidade 
        }

        db = client["avbdnr"]

        livros = db["livros"]

        livros.insert_one(livro)

        print("Livro adicionado com sucesso")
        
    except ValueError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def consultar_livro():

    lp = input("Digite o ISBN do livro procurado: ")

    consulta = {"ISBN": lp}

    db = client["avbdnr"]

    livros = db["livros"]

    livro_encontrado = livros.find_one(consulta)

    print(f"Livro encontrado: {livro_encontrado}")

def excluir_livro():

    le = input("Digite o ISBN do livro que deseja excluir: ")

    excluir = {"ISBN": le}

    db = client["avbdnr"]

    livros = db["livros"]

    livros.delete_one(excluir)

    print("Livro deletado com sucessso")

def atualizar_livro():

    try:
        ISBN = input("Insira o código de identificação único do livro que deseja atualizar: ")

        filtro = {"ISBN": ISBN}

        # Busca o livro para garantir que ele existe antes de atualizar
        db = client["avbdnr"]
        livros = db["livros"]
        livro_encontrado = livros.find_one(filtro)

        if livro_encontrado:
            print(f"Livro encontrado: {livro_encontrado}")
            
            # Solicita os novos dados que o usuário deseja atualizar
            novo_titulo = input("Insira o novo nome do livro: ")
            novo_autor = input("Insira o novo autor do livro: ")
            novo_genero = input("Insira o novo gênero do livro: ")
            novo_ano = input("Insira o novo ano de publicação: ")
            nova_quantidade = input("Insira a nova quantidade de exemplares disponíveis: ")

            # Cria o dicionário de atualização com apenas os campos que foram preenchidos
            novos_valores = {}

            if novo_titulo:
                novos_valores['titulo'] = novo_titulo
            if novo_autor:
                novos_valores['autor'] = novo_autor
            if novo_genero:
                novos_valores['genero'] = novo_genero
            if novo_ano:
                try:
                    novos_valores['ano'] = int(novo_ano)
                except ValueError:
                    print("Ano inválido, mantendo o ano atual.")
            if nova_quantidade:
                try:
                    novos_valores['quantidade'] = int(nova_quantidade)
                except ValueError:
                    print("Quantidade inválida, mantendo a quantidade atual.")

            if novos_valores:
                # Cria o dicionário de atualização
                novo_valor = {"$set": novos_valores}

                # Realiza a atualização
                resultado_atualizacao = livros.update_one(filtro, novo_valor)

                if resultado_atualizacao.modified_count > 0:
                    print("Livro atualizado com sucesso.")
                else:
                    print("Nenhum campo foi alterado.")
            else:
                print("Nenhum dado foi atualizado.")
        else:
            print("Nenhum livro encontrado com esse ISBN.")
            
    except Exception as e:
        print(f"Ocorreu um erro ao atualizar o livro: {e}")

def menu_livros():
    print("")
    print("1 - Adicionar novo livro")
    print("2 - Consultar livro")
    print("3 - Editar livro")
    print("4 - Excluir livro")
    print("5 - Sair")
    print("")

    try:
        opi = int(input("Selecione a opção desejada: ").strip()) 
        if opi == 1:
            adicionar_livro() 
        elif opi == 2:
            consultar_livro()
        elif opi == 3:
            atualizar_livro()
        elif opi == 4:
            excluir_livro()
        elif opi == 5:
            print("Retornando ao menu principal.")
            return
        else:
            print("Opção inválida! Escolha um número entre 1 e 5.")
    except ValueError:
        print("Erro: Você precisa digitar um número válido.")
    finally:
        print("Fim da execução.")

#....................................................................................................

def validar_cpf(cpf: str) -> bool:
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se o CPF possui 11 dígitos
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    
    primeiro_digito = 11 - (soma % 11)
    primeiro_digito = 0 if primeiro_digito > 9 else primeiro_digito
    
    if primeiro_digito != int(cpf[9]):
        return False

    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    
    segundo_digito = 11 - (soma % 11)
    segundo_digito = 0 if segundo_digito > 9 else segundo_digito
    
    return segundo_digito == int(cpf[10])

def adicionar_usuario():
    try:
        nome = input("Insira o nome do usuário: ")
        email = input("Insira o e-mail do usuário: ")
        
        # Solicita CPF e valida
        while True:
            cpf = input("Insira o CPF do usuário (somente números): ")
            if validar_cpf(cpf):
                break
            else:
                print("CPF inválido. Tente novamente.")
        
        data_nascimento = input("Insira a data de nascimento do usuário (YYYY-MM-DD): ")

        usuario = {
            'nome': nome,
            'email': email,
            'cpf': cpf,
            'data_nascimento': data_nascimento,
            'situacao': 'ativo'  # Adiciona campo 'situacao' como 'ativo'
        }

        db = client["avbdnr"]
        usuarios = db["usuario"]

        usuarios.insert_one(usuario)

        print("Usuário adicionado com sucesso")
    
    except Exception as e:
        print(f"Ocorreu um erro ao adicionar o usuário: {e}")
                                    
def consultar_usuario():
    try:
        cpf = input("Digite o CPF do usuário procurado: ")

        consulta = {"cpf": cpf}
        db = client["avbdnr"]
        usuarios = db["usuario"]

        usuario_encontrado = usuarios.find_one(consulta)

        if usuario_encontrado:
            # Converte a data de nascimento para string formatada
            data_nascimento = usuario_encontrado['data_nascimento'].strftime("%d/%m/%Y")

            # Exibe todas as informações do usuário encontrado
            print(f"\nUsuário encontrado:")
            print(f"Nome: {usuario_encontrado['nome']}")
            print(f"E-mail: {usuario_encontrado['email']}")
            print(f"Data de Nascimento: {data_nascimento}")
            print(f"CPF: {usuario_encontrado['cpf']}\n")
        else:
            print("Nenhum usuário encontrado com esse CPF.")
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def excluir_usuario():
    try:
        cpf = input("Digite o CPF do usuário que deseja excluir: ")

        excluir = {"cpf": cpf}
        db = client["avbdnr"]
        usuarios = db["usuario"]

        resultado = usuarios.delete_one(excluir)

        if resultado.deleted_count > 0:
            print("Usuário excluído com sucesso.")
        else:
            print("Nenhum usuário encontrado com esse CPF.")
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def atualizar_usuario():
    try:
        cpf = input("Insira o CPF do usuário que deseja atualizar: ")

        filtro = {"cpf": cpf}

        # Busca o usuário para garantir que ele existe antes de atualizar
        db = client["avbdnr"]
        usuarios = db["usuario"]
        usuario_encontrado = usuarios.find_one(filtro)

        if usuario_encontrado:
            data_nascimento = usuario_encontrado['data_nascimento'].strftime("%d/%m/%Y")
            print(f"\nUsuário encontrado:")
            print(f"Nome: {usuario_encontrado['nome']}")
            print(f"E-mail: {usuario_encontrado['email']}")
            print(f"Data de Nascimento: {data_nascimento}")
            print(f"CPF: {usuario_encontrado['cpf']}\n")
            
            # Solicita os novos dados que o usuário deseja atualizar
            novo_nome = input("Insira o novo nome do usuário: ")
            novo_email = input("Insira o novo e-mail do usuário: ")
            nova_data_nascimento = input("Insira a nova data de nascimento (DD/MM/AAAA): ")

            # Cria o dicionário de atualização com apenas os campos que foram preenchidos
            novos_valores = {}

            if novo_nome:
                novos_valores['nome'] = novo_nome
            if novo_email:
                novos_valores['email'] = novo_email
            if nova_data_nascimento:
                try:
                    # Converte a nova data de nascimento para o tipo datetime
                    nova_data_nascimento_dt = datetime.strptime(nova_data_nascimento, "%d/%m/%Y")
                    novos_valores['data_nascimento'] = nova_data_nascimento_dt
                except ValueError:
                    print("Formato de data inválido, mantendo a data de nascimento atual.")

            if novos_valores:
                # Cria o dicionário de atualização
                novo_valor = {"$set": novos_valores}

                # Realiza a atualização
                resultado_atualizacao = usuarios.update_one(filtro, novo_valor)

                if resultado_atualizacao.modified_count > 0:
                    print("Usuário atualizado com sucesso.")
                else:
                    print("Nenhum campo foi alterado.")
            else:
                print("Nenhum dado foi atualizado.")
        else:
            print("Nenhum usuário encontrado com esse CPF.")
            
    except Exception as e:
        print(f"Ocorreu um erro ao atualizar o usuário: {e}")

def menu_usuarios():
    print("")
    print("1 - Adicionar novo usuário")
    print("2 - Consultar usuário")
    print("3 - Editar usuário")
    print("4 - Excluir usuário")
    print("5 - Sair")
    print("")

    try:
        op = int(input("Selecione a opção desejada: "))
        
        if op == 1:
            adicionar_usuario()
        elif op == 2:
            consultar_usuario()
        elif op == 3:
            atualizar_usuario()
        elif op == 4:
            excluir_usuario()
        elif op == 5:
            print("Saindo do menu de usuários.")
            return
        else:
            print("Opção inválida! Escolha um número entre 1 e 5.")
            
    except ValueError:
        print("Erro: Você precisa digitar um número válido.")
    
    finally:
        print("Fim da execução do menu de usuários.")

#....................................................................................................

def menu_consultas():
    print("")
    print("1 - Listar livros disponíveis para empréstimo")
    print("2 - Consultar os empréstimos em aberto de um usuário específico")
    print("3 - Consultar usuários com empréstimos vencidos")
    print("4 - Sair")
    print("")

    try:
        op = int(input("Selecione a opção desejada: "))
        
        if op == 1:
            livros_disponiveis()
        elif op == 2:
            consultar_emprestimo()
        elif op == 3:
            consultar_emprestimos_vencidos()
        elif op == 4:
            return
        else:
            print("Opção inválida! Escolha um número entre 1 e 4.")
            
    except ValueError:
        print("Erro: Você precisa digitar um número válido.")
    
    finally:
        print("Fim da execução do menu de consultas.")

def livros_disponiveis():

    db = client["avbdnr"]

    livros = db["livros"]   

    query = {"quantidade": {"$gt": 1}}
    livros_disp = livros.find(query, {"ISBN": 1, "titulo": 1, "autor": 1, "genero": 1, "ano": 1, "quantidade": 1, "_id": 0})
    print("")
    print("Livros que estão disponiveis para empréstimo: ")
    print("")
    for livro in livros_disp:
        print(f"ISNB: {livro['ISBN']}")
        print(f"Titulo: {livro['titulo']}")
        print(f"Autor: {livro['autor']}")
        print(f"Genêro: {livro['genero']}")
        print(f"Ano: {livro['ano']}")
        print(f"Quantidade: {livro['quantidade']}")
        print("")

def consultar_emprestimo():
    try:
        cpf = input("Insira o CPF do usuário que deseja consultar os empréstimos: ")

        # Definir a consulta para encontrar empréstimos ativos do usuário
        query = {
            "cpf_usuario": cpf,
            "situacao": "ativo"
        }
        
        db = client["avbdnr"]
        emprestimos = db["emprestimos"]
        
        # Buscar os empréstimos em aberto
        emprestimos_abertos = list(emprestimos.find(query))

        # Verifica se encontrou algum empréstimo
        if len(emprestimos_abertos) == 0:
            print("Nenhum empréstimo em aberto encontrado para este usuário.")
            return

        # Exibe os empréstimos em aberto
        print("Empréstimos em aberto:")
        for emprestimo in emprestimos_abertos:
            # Exibe as informações do empréstimo no formato desejado
            data_emprestimo = emprestimo['data_emprestimo']
            data_prevista_devolucao = emprestimo['data_prevista_devolucao']

            # Converte as datas do formato MongoDB para o formato legível
            data_emprestimo_formatada = data_emprestimo.strftime('%d/%m/%Y')
            data_prevista_devolucao_formatada = data_prevista_devolucao.strftime('%d/%m/%Y')

            # Verifica se o empréstimo está vencido
            data_atual = datetime.now()

            if data_atual > data_prevista_devolucao:
                situacao_devolucao = "Vencido"
            else:
                situacao_devolucao = "No prazo"
            
            # Exibe as informações do empréstimo e da situação
            print(f"\nEmpréstimo encontrado:")
            print(f"ISBN: {emprestimo['ISBN']}")
            print(f"Data do Empréstimo: {data_emprestimo_formatada}")
            print(f"Data Prevista de Devolução: {data_prevista_devolucao_formatada}")
            print(f"Situação do Empréstimo: {situacao_devolucao}\n")

        input("Pressione Enter para voltar ao menu principal...")

    except Exception as e:
        print(f"Ocorreu um erro ao consultar os empréstimos: {e}")
        input("Pressione Enter para voltar ao menu principal...")

def consultar_emprestimos_vencidos():
    try:
        db = client["avbdnr"]
        emprestimos = db["emprestimos"]
        usuarios = db["usuario"]

        data_atual = datetime.now()

        query = {
            "data_prevista_devolucao": {"$lt": data_atual},
            "situacao": "ativo"
        }

        emprestimos_vencidos = list(emprestimos.find(query))

        if len(emprestimos_vencidos) == 0:
            print("Nenhum empréstimo vencido encontrado.")
            return

        print("Empréstimos vencidos encontrados:")
        for emprestimo in emprestimos_vencidos:
            usuario = usuarios.find_one({"cpf": emprestimo["cpf_usuario"]})
            if usuario:
                print(f"\nUsuário encontrado:")
                print(f"Nome: {usuario['nome']}")

                data_emprestimo_formatada = emprestimo['data_emprestimo'].strftime('%d/%m/%Y')
                data_prevista_devolucao_formatada = emprestimo['data_prevista_devolucao'].strftime('%d/%m/%Y')

                print(f"\nEmpréstimo encontrado:")
                print(f"ISBN: {emprestimo['ISBN']}")
                print(f"Data do Empréstimo: {data_emprestimo_formatada}")
                print(f"Data Prevista de Devolução: {data_prevista_devolucao_formatada}")
                print(f"Situação do Empréstimo: Vencido\n")

        input("Pressione Enter para voltar ao menu principal...")
    
    except Exception as e:
        print(f"Ocorreu um erro ao consultar os empréstimos vencidos: {e}")
        input("Pressione Enter para voltar ao menu principal...")

#....................................................................................................

def menu_relatorios():
    print("")
    print("1 - Gerar relatório de todos os livros cadastrados")
    print("2 - Gerar relatório de todos os usuários cadastrados")
    print("3 - Gerar relatório de todos os empréstimos realizados em um período de tempo específico")
    print("4 - Sair")
    print("")

    try:
        op = int(input("Selecione a opção desejada: "))
        
        if op == 1:
            livros_cadastrados()
        elif op == 2:
            usuario_cadastrados()
        elif op == 3:
            emprestimos_periodo()
        elif op == 4:
            print("Saindo do menu de relatórios.")
        else:
            print("Opção inválida! Escolha um número entre 1 e 4.")
            
    except ValueError:
        print("Erro: Você precisa digitar um número válido.")
    
    finally:
        print("Fim da execução do menu de relatórios.")

def livros_cadastrados():

    db = client["avbdnr"]

    livros = db["livros"]   

    livros_disp = livros.find()
    print("")
    print("Livros cadastrados: ")
    print("")
    for livro in livros_disp:
        print(f"ISNB: {livro['ISBN']}")
        print(f"Titulo: {livro['titulo']}")
        print(f"Autor: {livro['autor']}")
        print(f"Genêro: {livro['genero']}")
        print(f"Ano: {livro['ano']}")
        print(f"Quantidade: {livro['quantidade']}")
        print("")

def usuario_cadastrados():

    db = client["avbdnr"]

    usuarios = db["usuario"]   

    usuarios_encontrados = usuarios.find()
    print("")
    print("Usuarios cadastrados: ")
    print("")
    for usuario in usuarios_encontrados:
        data_nascimento = usuario['data_nascimento'].strftime("%d/%m/%Y")
        print(f"Nome: {usuario['nome']}")
        print(f"E-mail: {usuario['email']}")
        print(f"Data de Nascimento: {data_nascimento}")
        print(f"CPF: {usuario['cpf']}")
        print("")

def emprestimos_periodo():
    try:
        # Solicitar ao usuário as datas de início e fim
        data_inicio_str = input("Insira a data de início (DD/MM/AAAA): ")
        data_fim_str = input("Insira a data de fim (DD/MM/AAAA): ")

        # Converter as strings de data para objetos datetime
        data_inicio = datetime.strptime(data_inicio_str, '%d/%m/%Y')
        data_fim = datetime.strptime(data_fim_str, '%d/%m/%Y')

        # Verificar se a data de início é anterior à data de fim
        if data_inicio > data_fim:
            print("A data de início deve ser anterior à data de fim.")
            return

        db = client["avbdnr"]
        emprestimos = db["emprestimos"]
        usuarios = db["usuario"]

        # Consulta os empréstimos realizados no intervalo de datas
        query = {
            "data_emprestimo": {
                "$gte": data_inicio,  # Maior ou igual à data de início
                "$lte": data_fim      # Menor ou igual à data de fim
            }
        }

        # Busca os empréstimos
        emprestimos_encontrados = list(emprestimos.find(query))

        if not emprestimos_encontrados:
            print("Nenhum empréstimo encontrado nesse período.")
            return

        print("\nRelatório de Empréstimos:")
        for emprestimo in emprestimos_encontrados:
            usuario = usuarios.find_one({"cpf": emprestimo["cpf_usuario"]})
            if usuario:
                print(f"\nUsuário:")
                print(f"Nome: {usuario['nome']}")

                data_emprestimo_formatada = emprestimo['data_emprestimo'].strftime('%d/%m/%Y')
                data_prevista_devolucao_formatada = emprestimo['data_prevista_devolucao'].strftime('%d/%m/%Y')

                print(f"\nEmpréstimo:")
                print(f"ISBN: {emprestimo['ISBN']}")
                print(f"Data do Empréstimo: {data_emprestimo_formatada}")
                print(f"Data Prevista de Devolução: {data_prevista_devolucao_formatada}")
                print(f"Situação do Empréstimo: {emprestimo['situacao']}\n")

        input("Pressione Enter para voltar ao menu principal...")
    
    except ValueError as ve:
        print(f"Erro na conversão de data: {ve}")
        input("Pressione Enter para voltar ao menu principal...")
    except Exception as e:
        print(f"Ocorreu um erro ao gerar o relatório: {e}")
        input("Pressione Enter para voltar ao menu principal...")

#....................................................................................................

def menu_emprestimos_devolucoes():
    print("")
    print("1 - Registrar novo empréstimo")
    print("2 - Registrar devolução de livro")
    print("3 - Sair")
    print("")

    try:
        op = int(input("Selecione a opção desejada: "))
        
        if op == 1:
            registrar_emprestimo()
        elif op == 2:
            devolver_emprestimo()
        elif op == 3:
            print("Saindo do menu de empréstimos e devoluções.")
        else:
            print("Opção inválida! Escolha um número entre 1 e 3.")
            
    except ValueError:
        print("Erro: Você precisa digitar um número válido.")
    
    finally:
        print("Fim da execução do menu de empréstimos e devoluções.")

def registrar_emprestimo():
    try:
        db = client["avbdnr"]

        # Coleção de livros, usuários e empréstimos
        livros = db["livros"]
        emprestimos = db["emprestimos"]
        usuarios = db["usuario"]

        # Solicitar CPF do usuário e verificar se ele existe
        cpf_usuario = input("Insira o CPF do usuário: ")
        usuario = usuarios.find_one({"cpf": cpf_usuario})
        if not usuario:
            print("Usuário não encontrado.")
            return
        
        # Solicitar o ISBN do livro e verificar se existe e se há exemplares disponíveis
        ISBN = input("Insira o ISBN do livro: ")
        livro = livros.find_one({"ISBN": ISBN})
        if not livro:
            print("Livro não encontrado.")
            return
        if livro["quantidade"] <= 0:
            print("Não há exemplares disponíveis para empréstimo.")
            return
        
        # Registrar o empréstimo com o título do livro
        data_emprestimo = datetime.now()
        data_prevista_devolucao = data_emprestimo + timedelta(days=14)
        
        emprestimo = {
            "cpf_usuario": cpf_usuario,
            "ISBN": ISBN,
            "titulo_livro": livro["titulo"],  # Adicionando o título do livro
            "data_emprestimo": data_emprestimo,
            "data_prevista_devolucao": data_prevista_devolucao
        }
        
        emprestimos.insert_one(emprestimo)
        
        # Atualizar a quantidade de exemplares disponíveis
        nova_quantidade = livro["quantidade"] - 1
        livros.update_one({"ISBN": ISBN}, {"$set": {"quantidade": nova_quantidade}})
        
        # Atualizar a quantidade de empréstimos ativos do usuário
        emprestimos_ativos = usuario.get("emprestimos_ativos", 0) + 1
        usuarios.update_one({"cpf": cpf_usuario}, {"$set": {"emprestimos_ativos": emprestimos_ativos}})
        
        print(f"Empréstimo registrado com sucesso. Data prevista de devolução: {data_prevista_devolucao.strftime('%d/%m/%Y')}")
    
    except Exception as e:
        print(f"Ocorreu um erro ao registrar o empréstimo: {e}")

def devolver_emprestimo():
    try:
        db = client["avbdnr"]

        # Coleção de livros, usuários e empréstimos
        livros = db["livros"]
        emprestimos = db["emprestimos"]
        usuarios = db["usuario"]

        # Solicitar o CPF do usuário
        cpf_usuario = input("Insira o CPF do usuário: ")
        emprestimo = emprestimos.find_one({"cpf_usuario": cpf_usuario, "situacao": "ativo"})
        
        if not emprestimo:
            print("Nenhum empréstimo ativo encontrado para este usuário.")
            return
        
        # Solicitar o ISBN do livro e verificar se o empréstimo é válido
        ISBN = emprestimo["ISBN"]
        livro = livros.find_one({"ISBN": ISBN})
        if not livro:
            print("Livro não encontrado no banco de dados.")
            return

        # Registrar a devolução
        data_devolucao = datetime.now()
        
        # Atualizar a situação do empréstimo para inativo e registrar a data de devolução
        emprestimos.update_one(
            {"cpf_usuario": cpf_usuario, "situacao": "ativo"},
            {"$set": {
                "situacao": "inativo",
                "data_devolucao": data_devolucao
            }}
        )

        # Atualizar a quantidade de exemplares disponíveis
        nova_quantidade = livro["quantidade"] + 1
        livros.update_one({"ISBN": ISBN}, {"$set": {"quantidade": nova_quantidade}})

        # Atualizar a quantidade de empréstimos ativos do usuário
        usuario = usuarios.find_one({"cpf": cpf_usuario})
        emprestimos_ativos = usuario.get("emprestimos_ativos", 0) - 1
        if emprestimos_ativos < 0:
            emprestimos_ativos = 0  # Garantir que não fique negativo
        
        usuarios.update_one({"cpf": cpf_usuario}, {"$set": {"emprestimos_ativos": emprestimos_ativos}})
        
        print(f"Empréstimo devolvido com sucesso. Data de devolução: {data_devolucao.strftime('%d/%m/%Y')}")
    
    except Exception as e:
        print(f"Ocorreu um erro ao atualizar o empréstimo: {e}")

    
#....................................................................................................

while True:
    print("\nBem vindo ao sistema gerenciador de biblioteca")
    print("")
    print("1 - Operações com Livro")
    print("2 - Operações com Usuário")
    print("3 - Empréstimos e Devoluções")
    print("4 - Consultas")
    print("5 - Relatórios")
    print("6 - Sair")
    print("")
    
    try:
        op = int(input("Selecione uma opção: "))
        
        if op == 1:
            menu_livros()
            input("Pressione Enter para voltar ao menu principal...") 
        
        elif op == 2:
            # Operações com Usuário
            menu_usuarios()
            input("Pressione Enter para voltar ao menu principal...") 
        
        elif op == 3:
            # Empréstimos e Devoluções
            menu_emprestimos_devolucoes()
            input("Pressione Enter para voltar ao menu principal...")  
        
        elif op == 4:
            # Consultas
            menu_consultas()
            input("Pressione Enter para voltar ao menu principal...") 
        
        elif op == 5:
            # Relatórios
            menu_relatorios()
            input("Pressione Enter para voltar ao menu principal...") 
        elif op == 6:
            # Sair
            print("Encerrando o programa...")
            break 
        
        else:
            print("Opção inválida! Escolha um número entre 1 e 6.")
            
    except ValueError:
        print("Erro: Você precisa digitar um número válido.")
    
    finally:
        print("")

