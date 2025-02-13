import os
import sys
import time
from datetime import datetime, timedelta
from winotify import Notification, audio
from threading import Thread

# Função para limpar a tela
def limpar_tela():
    # Verifica o sistema operacional
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Unix/Linux/Mac
        os.system('clear')

def gerar_nome_usuario(email):
    nome_base = email.split("@")[0]  # Pega a parte antes do "@" no e-mail
    nome_formatado = nome_base.split('.')[0].capitalize()  # Usa apenas a primeira parte e capitaliza
    return nome_formatado

def validar_email(email):
    email = email.strip()  # Remove espaços extras

    # Verifica se o e-mail contém "@" e termina com "@listainteligente.com"
    if "@" in email and email.endswith("@listainteligente.com"):
        parte_local = email.split("@")[0]  # Pega a parte antes do "@"
        
        # Verifica se a parte antes do "@" não está vazia
        if parte_local:
            return True
        else:
            print("A parte antes do '@listainteligente.com' não pode estar vazia!")
            return False
    else:
        print("E-mail inválido! Certifique-se de que o e-mail contém '@' e termina com '@listainteligente.com'.")
        return False

def solicitar_email():
    while True:
        email = input("Digite o seu email: ").strip()
        if email:  # Se o campo não for vazio
            # Verificar se o email é válido (já dentro da função)
            if validar_email(email):
                return email
            else:
                print("E-mail inválido! Certifique-se de que o e-mail contém '@' e um domínio válido.")
        else:
            print("O email não pode estar vazio! Tente novamente.")

def solicitar_senha():
    while True:
        senha = input("Digite a sua senha: ").strip()
        if senha:  # Se o campo não for vazio
            return senha  # Apenas retorna a senha, sem validação extra.

def redefinir_senha():
    global senha_usuario
    senha_padrao = "0123456"
    tentativas = 3

    while tentativas > 0:
        nova_senha = input(f"Favor redefina sua senha! (Tentativas restantes: {tentativas}): ").strip()

        if nova_senha == senha_padrao:
            print("Senha inválida! Não pode ser a senha padrão.")
        elif len(nova_senha) < 6:
            print("Senha inválida! Certifique-se de que tenha pelo menos 6 caracteres.")
        else:
            print("Senha redefinida com sucesso!")
            senha_usuario = nova_senha
            nome_usuario = gerar_nome_usuario(email)
            notificacao = Notification(
                app_id="Sistema Lista Inteligente",
                title="Saudações!",
                msg=f"Seja bem-vindo ao sistema Lista Inteligente, {nome_usuario}",
                duration="short"
            )
            notificacao.set_audio(audio.IM, loop=False)
            notificacao.show()
            limpar_tela()  # Limpa a tela após redefinir a senha
            return True  # Senha redefinida com sucesso

        tentativas -= 1

        if tentativas == 0:
            print("VOCÊ ATINGIU O NÚMERO MÁXIMO DE TENTATIVAS. FICARÁ 5 MINUTOS SUSPENSO!")
            suspensao_redefinir_senha()  # Chama a suspensão
            return False  # Retorna False se a senha não foi redefinida 

def suspensao_redefinir_senha():
    suspensao_tempo = 1 * 60  # 5 minutos convertidos para segundos
    # Loop para o contador
    while suspensao_tempo:
        mins, secs = divmod(suspensao_tempo, 60)  # Converte segundos em minutos e segundos
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(f"Tempo restante: {timer}", end="\r")  # O '\r' faz o texto sobrescrever a linha
        time.sleep(1)  # Aguarda 1 segundo
        suspensao_tempo -= 1  # Diminui 1 segundo a cada iteração
    # Exibe uma mensagem quando o tempo acabar
    print("Suspensão finalizada!\nVamos tentar novamente!")
    limpar_tela()  # Limpa a tela após a suspensão
    redefinir_senha()

def suspensao_login():
    suspensao_tempo = 1 * 60  # 5 minutos convertidos para segundos
    # Loop para o contador
    while suspensao_tempo:
        mins, secs = divmod(suspensao_tempo, 60)  # Converte segundos em minutos e segundos
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(f"Tempo restante: {timer}", end="\r")  # O '\r' faz o texto sobrescrever a linha
        time.sleep(1)  # Aguarda 1 segundo
        suspensao_tempo -= 1  # Diminui 1 segundo a cada iteração
    # Exibe uma mensagem quando o tempo acabar
    print("Suspensão finalizada!\nVamos tentar novamente!")
    limpar_tela()  # Limpa a tela após a suspensão
    return True # Retorna True indicando que o usuário pode tentar novamente

def login_usuario():
    senha_padrao = "0123456"
    tentativas = 3
    email = solicitar_email()  # Solicita o email uma vez

    while tentativas > 0:
        senha = solicitar_senha()  # Solicita a senha

        if senha == senha_padrao:
            print("A senha padrão não é válida! Por favor, tente novamente.")

        elif len(senha) < 6:
            print("Senha inválida! Certifique-se de que tenha pelo menos 6 caracteres.")
        
        else:
            print("Login realizado com sucesso!")
            nome_usuario = gerar_nome_usuario(email)
            notificacao = Notification(
                app_id="Sistema Lista Inteligente",
                title="Saudações!",
                msg=f"Seja bem-vindo ao sistema Lista Inteligente, {nome_usuario}",
                duration="short"
                )
            notificacao.set_audio(audio.Default, loop=False)
            notificacao.show()
            limpar_tela()  # Limpa a tela após o login
            exibir_menu(estoque)
            return 

        # Exibe mensagem antes de decrementar
        tentativas -= 1
        if tentativas > 0:
            print(f"Essa tentativa falhou. Você ainda tem mais {tentativas} tentativa(s).")
        else:
            print("Número máximo de tentativas atingido. Suspensão de 5 minutos...")
            suspensao_login()
            return

def verificar_item_estoque(estoque, nome, quantidade, categoria, unidade, validade):
    """
    Adiciona um novo lote de um item ao estoque.
    Se o item já existir, apenas adiciona um novo lote.
    """
    if nome not in estoque:
        estoque[nome] = []  # Cria uma lista vazia para o item

    # Adiciona um novo lote à lista
    estoque[nome].append({
        "informacoes": {
            "quantidade": quantidade,
            "unidade": unidade,
            "validade": validade,
            "categoria": categoria
        }
    })
    notificacao = Notification(
    app_id="Sistema Lista Inteligente",
    title="Item Adicionado",
    msg="O item {nome} foi adicinado ao estoque!",
    duration="short"
    )
    notificacao.set_audio("default", loop=False)
    notificacao.show()        

def adicionar_retirar(estoque):
    while True:
        opcao = input("\nOpções disponíveis:\n"
                      "1 - Adicionar unidades a um item já cadastrado\n"
                      "2 - Remover uma quantidade de um item\n"
                      "3 - Editar um item\n"
                      "4 - Remover um item completamente\n"
                      "5 - Remover um lote específico\n"
                      "6 - Sair\n"
                      "Escolha uma opção (1-6): ").strip().lower()

        if opcao == "1":  # Adicionar mais itens a um item já cadastrado
            item = input("Qual item você deseja adicionar mais unidades? ").strip().lower()
            
            if item in estoque:
                try:
                    quantidade = int(input("Quantas unidades deseja adicionar? "))
                    if quantidade > 0:
                        # Adiciona a quantidade ao primeiro lote (ou outro lote específico)
                        estoque[item][0]["informacoes"]["quantidade"] += quantidade
                                                
                        notificacao = Notification(
                            app_id="Sistema Lista Inteligente",
                            title="Estoque Atualizado",
                            msg=f"Foram adicionadas {quantidade} unidades ao item '{item}'.",
                            duration="short"
                        )
                        notificacao.set_audio(audio.Default, loop=False)
                        notificacao.show()
                    else:
                        print("A quantidade deve ser maior que zero.")
                except ValueError:
                    print("Por favor, insira um número válido.")
            else:
                print("Item não encontrado no estoque!")

        elif opcao == "2":  # Remover quantidade de um item
            item = input("Qual item você deseja remover? ").lower().strip()
            if item in estoque:
                print(f"Item encontrado! Listando os lotes disponíveis:")
                for i, lote in enumerate(estoque[item], start=1):
                    validade = lote['informacoes']['validade']
                    if not isinstance(validade, datetime):
                        validade = datetime.strptime(validade, "%d-%m-%Y")
                    print(f"Lote {i} - Validade: {validade.strftime('%d-%m-%Y')}, Quantidade: {lote['informacoes']['quantidade']} {lote['informacoes']['unidade']}")

                while True:
                    lote_escolhido_input = input("Informe o número do lote que deseja remover (ex: 1, 2...): ")
                    try:
                        lote_escolhido = int(lote_escolhido_input) - 1
                        if 0 <= lote_escolhido < len(estoque[item]):
                            break
                        else:
                            print("Número do lote inválido! Tente novamente.")
                    except ValueError:
                        print("Entrada inválida! Digite um número inteiro.")

                lote = estoque[item][lote_escolhido]
                quantidade_disponivel = lote["informacoes"]["quantidade"]
                while True:
                    quantidade_remover_input = input(f"Quantos {lote['informacoes']['unidade']} deseja remover? ")
                    try:
                        quantidade_remover = int(quantidade_remover_input)
                        if quantidade_remover <= 0:
                            print("A quantidade deve ser maior que zero. Tente novamente.")
                        elif quantidade_remover > quantidade_disponivel:
                            print("A quantidade em estoque é insuficiente para ser removida!")
                        else:
                            break
                    except ValueError:
                        print("Entrada inválida! Digite um número inteiro.")

                lote["informacoes"]["quantidade"] -= quantidade_remover
                print(f"Removidos {quantidade_remover} {lote['informacoes']['unidade']} do lote {lote_escolhido + 1}")
                if lote["informacoes"]["quantidade"] == 0:
                    estoque[item].pop(lote_escolhido)
                    print(f"O lote {lote_escolhido + 1} foi removido do estoque.")
                if not estoque[item]:
                    del estoque[item]
                    print(f"O item {item} foi completamente removido do estoque.")
            else:
                print("Item não encontrado!")

        elif opcao == "3":  # Editar item existente
            item = input("Qual item você deseja editar? ").strip().lower()
            
            if item in estoque:
                print(f"Item encontrado! Listando os lotes disponíveis:")
                for i, lote in enumerate(estoque[item], start=1):
                    validade = lote['informacoes']['validade']
                    if not isinstance(validade, datetime):
                        validade = datetime.strptime(validade, "%d-%m-%Y")
                    print(f"Lote {i} - Validade: {validade.strftime('%d-%m-%Y')}, Quantidade: {lote['informacoes']['quantidade']} {lote['informacoes']['unidade']}")

                while True:
                    lote_escolhido_input = input("Informe o número do lote que deseja editar (ex: 1, 2...): ")
                    try:
                        lote_escolhido = int(lote_escolhido_input) - 1
                        if 0 <= lote_escolhido < len(estoque[item]):
                            break
                        else:
                            print("Número do lote inválido! Tente novamente.")
                    except ValueError:
                        print("Entrada inválida! Digite um número inteiro.")

                lote = estoque[item][lote_escolhido]
                
                novo_nome = input("Digite o novo nome do item ou pressione Enter para manter o mesmo: ").strip().lower()
                if novo_nome and novo_nome != item:
                    estoque[novo_nome] = estoque.pop(item)
                    item = novo_nome
                
                try:
                    nova_quantidade = int(input(f"Digite a nova quantidade do item (atual: {lote['informacoes']['quantidade']}) ou pressione Enter para manter a atual: ") or lote['informacoes']['quantidade'])
                    nova_categoria = input(f"Digite a nova categoria do item (atual: {lote['informacoes']['categoria']}) ou pressione Enter para manter a atual: ").strip().lower() or lote['informacoes']['categoria']
                    nova_unidade = input(f"Digite a nova unidade do item (atual: {lote['informacoes']['unidade']}) ou pressione Enter para manter a atual: ").strip().lower() or lote['informacoes']['unidade']
                    
                    while True:
                        validade_input = input(f"Digite a nova validade do item (Formato: DD-MM-YYYY) (atual: {lote['informacoes']['validade'].strftime('%d-%m-%Y')}) ou pressione Enter para manter a atual: ").strip()
                        if not validade_input:
                            nova_validade = lote['informacoes']['validade']
                            break
                        try:
                            nova_validade = datetime.strptime(validade_input, "%d-%m-%Y")
                            break
                        except ValueError:
                            print("Formato da data errada, favor inserir corretamente (DD-MM-YYYY)")
                    
                    if nova_quantidade >= 0:
                        lote['informacoes']['quantidade'] = nova_quantidade
                        lote['informacoes']['categoria'] = nova_categoria
                        lote['informacoes']['validade'] = nova_validade
                        lote['informacoes']['unidade'] = nova_unidade
                        print(f"O item foi atualizado: {item} - {lote['informacoes']['quantidade']} {lote['informacoes']['unidade']}, Categoria: {lote['informacoes']['categoria']}, Validade: {lote['informacoes']['validade'].strftime('%d-%m-%Y')}.")
                        
                        notificacao = Notification(
                            app_id="Sistema Lista Inteligente",
                            title="Item Editado",
                            msg=f"O item '{item}' foi atualizado com sucesso!",
                            duration="short"
                        )
                        notificacao.set_audio(audio.Default, loop=False)
                        notificacao.show()
                    else:
                        print("A quantidade deve ser maior ou igual a zero.")
                except ValueError:
                    print("Por favor, insira um número válido.")
            else:
                print("Item não encontrado no estoque!")

        elif opcao == "4":  # Remover item completamente
            item = input("Qual item você deseja remover completamente? ").strip().lower()
            
            if item in estoque:
                del estoque[item]
                print(f"O item '{item}' foi removido completamente do estoque.")
                notificacao = Notification(
                    app_id="Sistema Lista Inteligente",
                    title="Item Removido",
                    msg=f"O item '{item}' foi removido com sucesso!",
                    duration="short"
                )
                notificacao.set_audio(audio.Default, loop=False)
                notificacao.show()
            else:
                print("Item não encontrado no estoque!")
        
        elif opcao == "5":  # Remover lote específico
            item = input("Qual item você deseja remover um lote? ").strip().lower()
            if item in estoque:
                print(f"Item encontrado! Listando os lotes disponíveis:")
                for i, lote in enumerate(estoque[item], start=1):
                    validade = lote['informacoes']['validade']
                    if not isinstance(validade, datetime):
                        validade = datetime.strptime(validade, "%d-%m-%Y")
                    print(f"Lote {i} - Validade: {validade.strftime('%d-%m-%Y')}, Quantidade: {lote['informacoes']['quantidade']} {lote['informacoes']['unidade']}")

                while True:
                    lote_escolhido_input = input("Informe o número do lote que deseja remover (ex: 1, 2...): ")
                    try:
                        lote_escolhido = int(lote_escolhido_input) - 1
                        if 0 <= lote_escolhido < len(estoque[item]):
                            break
                        else:
                            print("Número do lote inválido! Tente novamente.")
                    except ValueError:
                        print("Entrada inválida! Digite um número inteiro.")

                estoque[item].pop(lote_escolhido)
                print(f"O lote {lote_escolhido + 1} foi removido do estoque.")
                if not estoque[item]:
                    del estoque[item]
                    print(f"O item {item} foi completamente removido do estoque.")
            else:
                print("Item não encontrado!")
        
        elif opcao == "6":
            exibir_menu(estoque)
        else:
            print("Opção inválida, tente novamente!")

def estoque_vazio_ntf():
        notificacao_estoque_vazio = Notification(
            app_id="Sistema Lista Inteligente",
            title="Estoque Vazio!",
            msg=f"O estoque se encontra vazio, cadastre seu primeiro item",
            duration="long"
            )
        notificacao_estoque_vazio.set_audio(audio.SMS, loop=False)
        notificacao_estoque_vazio.show()

def captura_input():
    while True:
        nome = input("Digite o nome do item: ").strip().lower()
        categoria = input("Digite a categoria do item: ").strip().lower()

        # Validação da quantidade
        while True:
            quantidade_input = input("Digite a quantidade do item: ").strip()
            try:
                quantidade = int(quantidade_input)  
                if quantidade <= 0:
                    print("A quantidade deve ser maior que zero. Tente novamente.")
                else:
                    break
            except ValueError:
                print("Entrada inválida! Digite um número inteiro para a quantidade.")    

        unidade = input("Digite a unidade do item [KG,ML,L,PC,UN,Etc...]: ").strip().lower()

        # Validação da data
        while True:
            validade_input = input(f"Digite a validade do item ({nome}) (Formato: DD-MM-YYYY): ").strip()
            try:
                validade = datetime.strptime(validade_input, "%d-%m-%Y")
                break
            except ValueError:
                print("Formato da data errada, favor inserir corretamente (DD-MM-YYYY)")

        # Adiciona o item ao estoque corretamente no formato de lotes
        verificar_item_estoque(estoque, nome, quantidade, categoria, unidade, validade)

        # Pergunta ao usuário se deseja continuar adicionando
        continuar = input("Deseja adicionar outro item? (sim/não): ").strip().lower()
        if continuar != "sim":
            break  

    # Notificação após finalizar o cadastro
    notificacao = Notification(
        app_id="Sistema Lista Inteligente",
        title="Item Cadastrado",
        msg="Itens cadastrados com sucesso!",
        duration="short"
    )
    notificacao.set_audio("default", loop=False)
    notificacao.show()        

    limpar_tela()  # Limpa a tela após cadastrar item
    exibir_menu(estoque)  # Chama o menu para exibir opções novamente

def verificar_estoque_baixo(estoque, limite=5):
    # Verifica se algum item no estoque está com quantidade abaixo do limite definido.
    for nome_item, lotes in estoque.items():
        for i, lote in enumerate(lotes, start=1):
            quantidade = lote['informacoes']['quantidade']
            unidade = lote['informacoes']['unidade']  # Adiciona esta linha para acessar a unidade
            if quantidade < limite:
                notificacao = Notification(
                    app_id="Sistema Lista Inteligente",
                    title="Estoque Baixo",
                    msg=f"O item '{nome_item}' no Lote {i} está com apenas {quantidade} {unidade}!",
                    duration="long"
                )
                notificacao.set_audio(audio.SMS, loop=False)
                notificacao.show()

def verificar_validade_estoque(estoque):
    hoje = datetime.now().date()  # Considere apenas a data, sem horário
    for nome_item, lotes in estoque.items():
        for lote in lotes:
            validade = lote['informacoes']['validade'].date()
            dias_restantes = (validade - hoje).days
            
            if 0 < dias_restantes <= 7:
                notificacao = Notification(
                    app_id="Sistema Lista Inteligente",
                    title="Item Próximo do Vencimento",
                    msg=f"O item '{nome_item}' vencerá em {dias_restantes} dias!",
                    duration="long"
                )
                notificacao.set_audio(audio.SMS, loop=False)
                notificacao.show()
                
            elif dias_restantes == 0:
                notificacao_vencendo_hoje = Notification(
                    app_id="Sistema Lista Inteligente",
                    title="Item Vencendo Hoje",
                    msg=f"O item '{nome_item}' vence hoje!",
                    duration="long"
                )
                notificacao_vencendo_hoje.set_audio(audio.Mail, loop=False)
                notificacao_vencendo_hoje.show()

            elif dias_restantes < 0:
                notificacao_vencido = Notification(
                    app_id="Sistema Lista Inteligente",
                    title="Item Vencido",
                    msg=f"O item '{nome_item}' já venceu!",
                    duration="long"
                )
                notificacao_vencido.set_audio(audio.Reminder, loop=False)
                notificacao_vencido.show()

def iniciar_verificacoes(estoque):

    def thread_validade():
        verificar_validade_estoque(estoque)

    def thread_estoque_baixo():
        verificar_estoque_baixo(estoque)

    t1 = Thread(target=thread_validade)
    t2 = Thread(target=thread_estoque_baixo)

    t1.start()
    t2.start()

def sair():
    notificacao = Notification(
    app_id="Sistema Lista Inteligente",
    title="Saindo...",
    msg=f"Vejo você em breve!",
    duration="short"
    )
    notificacao.set_audio(audio.Default, loop=False)
    notificacao.show()
    time.sleep(3)
    exit()

def exibir_menu(estoque):

    iniciar_verificacoes(estoque) #Faz o programa enviar as notificações toda vez que o menu aparece

    if not estoque:
        estoque_vazio_ntf()
        
    while True:
        # Exibe o menu com opções
        print("\n------ Menu do Estoque ------")
        print("1 - Cadastrar item ao estoque")
        print("2 - Mostrar estoque")
        print("3 - Consultar estoque")
        print("4 - Consultar categoria")
        print("5 - Adicionar, remover ou editar itens já cadastrado")
        print("6 - Sair")
        
        # Recebe a escolha do usuário
        escolha = input("Escolha uma opção (1-6): ")
        
        # Executa a ação correspondente à escolha
        if escolha == "1":
            captura_input()
        elif escolha == "2":
            exibir_estoque(estoque)
        elif escolha == "3":
             consultar_estoque_itens_ja_cadastrado(estoque)
        elif escolha == "4":
            consultar_estoque_por_categoria(estoque)
        elif escolha == "5":
            adicionar_retirar(estoque)
        elif escolha == "6":
            sair()
        else:
            print("Escolha invalida,tente novamente!")
        time.sleep(2)
        limpar_tela()  # Limpa a tela após cada operação no menu

def exibir_estoque(dicionario, nivel=0):
    if not dicionario:  # Corrigido para verificar o argumento correto
        estoque_vazio_ntf()
        return  # Sai da função se o estoque estiver vazio

    for chave, valor in dicionario.items():
        indentacao = "  " * nivel
        print(f"{indentacao}{chave.capitalize()}:")
        
        # Exibir cada lote de um item separadamente
        for i, item in enumerate(valor, start=1):
            informacoes = item['informacoes']
            validade_formatada = informacoes['validade'].strftime("%d-%m-%Y")  # Formata a data
            print(f"{indentacao}  Lote {i}:")
            print(f"{indentacao}    Quantidade: {informacoes['quantidade']} {informacoes['unidade']}")
            print(f"{indentacao}    Validade: {validade_formatada}")
            print(f"{indentacao}    Categoria: {informacoes['categoria']}")
        print()  # Linha em branco para melhor legibilidade

    time.sleep(2)

    # Perguntar uma única vez após mostrar TODO o estoque
    while True:
        voltar_ao_menu = input("Deseja voltar ao menu ou encerrar? (voltar/encerrar): ").lower()
            
        if voltar_ao_menu == "voltar":
            return  # Retorna ao menu principal
        elif voltar_ao_menu == "encerrar":
            sair()
        else:
            print("Opção inválida. Digite 'voltar' ou 'encerrar'.")

def consultar_estoque_itens_ja_cadastrado(estoque):
    item_consulta = input("Qual item deseja consultar no estoque? ").strip().lower()  # Garante que o nome do item seja em minúsculas
    
    encontrou = False
    for nome_item, lotes in estoque.items():
        # Se o nome do item contém o que foi digitado pelo usuário
        if item_consulta in nome_item.lower():
            encontrou = True
            print(f"\nItem: {nome_item.capitalize()}(s)")
            
            for i, lote in enumerate(lotes, start=1):
                informacoes = lote['informacoes']
                validade_formatada = informacoes['validade'].strftime("%d-%m-%Y")
                print(f"  Lote {i}:")
                print(f"    Quantidade: {informacoes['quantidade']} {informacoes['unidade']}")
                print(f"    Validade: {validade_formatada}")
                print(f"    Categoria: {informacoes['categoria']}")
                print()  # Espaço entre lotes
            
            time.sleep(3)
            
            # Pergunta ao usuário se deseja voltar ao menu ou encerrar
            while True:
                voltar_ao_menu = input("Deseja voltar ao menu ou encerrar? (voltar/encerrar): ").lower()
                
                if voltar_ao_menu == "voltar":
                    return  # Retorna ao menu principal
                elif voltar_ao_menu == "encerrar":
                    sair()

                else:
                    print("Opção inválida. Digite 'voltar' ou 'encerrar'.")
    
    # Se nenhum item for encontrado
    if not encontrou:
        print(f"Nenhum item encontrado com o nome '{item_consulta}'.")
        while True:
            voltar_ao_menu = input("Deseja voltar ao menu ou encerrar? (voltar/encerrar): ").lower()
            
            if voltar_ao_menu == "voltar":
                return  # Retorna ao menu principal
            elif voltar_ao_menu == "encerrar":
                sair()

            else:
                print("Opção inválida. Digite 'voltar' ou 'encerrar'.")

def consultar_estoque_por_categoria(estoque):
    categoria_consulta = input("Qual categoria deseja consultar no estoque? ").strip().lower()  # Garante que a categoria seja comparada em minúsculas
    
    encontrou = False
    for nome_item, lotes in estoque.items():
        for lote in lotes:
            categoria = lote['informacoes']['categoria'].lower()  # Comparando a categoria em minúsculas
            if categoria_consulta == categoria:  # Verifica se a categoria digitada é igual à do lote
                encontrou = True
                informacoes = lote['informacoes']
                validade_formatada = informacoes['validade'].strftime("%d-%m-%Y")
                print(f"\nItem: {nome_item.capitalize()}(s)")
                print(f"  Quantidade: {informacoes['quantidade']} {informacoes['unidade']}")
                print(f"  Validade: {validade_formatada}")
                print(f"  Categoria: {informacoes['categoria']}")
    
    if not encontrou:
        print(f"Nenhum item encontrado na categoria {categoria_consulta}.")  
    time.sleep(3)
            
    # Pergunta ao usuário se deseja voltar ao menu ou encerrar
    while True:
        voltar_ao_menu = input("Deseja voltar ao menu ou encerrar? (voltar/encerrar): ").lower()
                
        if voltar_ao_menu == "voltar":
            return  # Retorna ao menu principal
        elif voltar_ao_menu == "encerrar":
            sair()

        else:
            print("Opção inválida. Digite 'voltar' ou 'encerrar'.")  

estoque = {}

#fluxo do codigo
print("\nSEJA BEM-VINDO AO SISTEMA LISTA INTELIGENTE")
time.sleep(2)

primeiro_acesso=input("É o seu  primeiro acesso(sim/não):? ").strip().lower()
if primeiro_acesso == "sim":
    while True:
        email = input("Digite o seu email: ").strip()
        # Valida se o e-mail fornecido é válido

        while not validar_email(email):
            print("E-mail inválido! Certifique-se de que o e-mail contém '@' e um domínio válido.")
            email = input("Digite o seu email novamente: ").strip()
        print("Verificando se seu email é válido...")
        time.sleep(2)
        print("Agora vamos redefinir sua senha!")
        if redefinir_senha():  # Verifica se a senha foi redefinida com sucesso
            exibir_menu(estoque)
            break
     
else:
   login_usuario()
   