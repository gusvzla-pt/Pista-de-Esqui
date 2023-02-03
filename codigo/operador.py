import datetime
import pandas as pd
import random
import qrcode
import math
import matplotlib.pyplot as plt
import ctypes; kernel32 = ctypes.WinDLL('kernel32'); hStdOut = kernel32.GetStdHandle(-11); mode = ctypes.c_ulong(); kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode)); mode.value |= 4; kernel32.SetConsoleMode(hStdOut, mode)

print("1 - Adicionar\n2 - Alterar Estado\n3 - Bilhetes\n4 - Ver Mapa")
opcaoInicial = input("\033[34m\033[1mEscolha uma opção: \033[0m ")

def menuInicial(opcao):

    if opcao == "1":
        menuAdicionar()
    elif opcao == "2":
        menuAlterarEstado()
    elif opcao == "3":
        menuBilhete()
    elif opcao == "4":
        dibujarMapa()
        menuInicial('v')
    elif opcao == "v":
        print("1 - Adicionar\n2 - Alterar Estado\n3 - Bilhetes\n4 - Ver Mapa")
        opcao = input("\033[34m\033[1mEscolha uma opção: \033[0m")
        menuInicial(opcao)
    else:
        print("\033[31mEscolha uma opção válida\033[0m")
        print("1 - Adicionar\n2 - Alterar Estado\n3 - Bilhetes\n4 - Ver Mapa")
        opcao = input("\033[34m\033[1mEscolha uma opção: \033[0m")
        menuInicial(opcao)

def menuAdicionar():

    print("1 - Pista\n2 - Secção\n3 - Zonas E Comodidades\n4 - Meio Mecánico\n0 - Voltar ao menu inicial")
    opcao = input("\033[34m\033[1mEscolha uma opção: \033[0m") 
   
    if opcao == "1":
        adicionarPista()
        menuAdicionar()
    elif opcao ==  "2":
        adicionarSeccao()
        print("\033[32m\033[1mA operação foi concluída com sucesso!!\033[0m")
        menuAdicionar()
    elif opcao == "3":
        adicaoZonaEComodidades()
        print("\033[32m\033[1mA operação foi concluída com sucesso!!\033[0m")
        menuAdicionar()
    elif opcao == "4":
        adicaoMeioMecanico()
        menuAdicionar()
    elif opcao == "0":
        menuInicial("v")
    else:
        print("\033[31mEscolha uma opção válida\033[0m")
        menuAdicionar()

def gerarCodigo():

  letras = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
  codigo = ''.join(random.sample(letras, 4))

  return codigo

def adicionarPista():

    df = pd.read_csv("dados/tabela_pistas.txt")
    dfZonas = pd.read_csv("dados/tabela_zonas.txt")
    dfZonasCodigoENome = dfZonas[["CodigoZona", "Nome"]]
    codigosZonas = dfZonas["CodigoZona"].tolist()
    
    if len(codigosZonas) < 2:
        print("\033[31mPara criar uma pista deve haver pelo menos 2 zonas existentes, actualmente não há nenhuma zona. Por favor crie uma zona\033[0m")
        menuAdicionar()
    else:
        
        while True:
            nomePista = input("0 - Voltar ao menu\n\033[34m\033[1mIntroduza o nome da pista: \033[0m")
            if nomePista == "0":
                menuAdicionar()
            else:
                if nomePista in dfZonas['Nome'].values: 
                    print('\033[31mO nome da pista já existe, deve introduzir um nome único\033[0m')
                else:
                    break
        
        while True:
            if nomePista == "":
                print("\033[31mDeve introduzir o nome da pista\033[0m")
                nomePista = input("\033[34m\033[1mIntroduza o nome da pista: \033[0m")
            else:
                break

        while True:
            print("Estas são as zonas existentes (com o seu código)")
            print(dfZonasCodigoENome.to_string(index=False))

            zonaInicial = input("0 - Voltar ao menu\n\033[34m\033[1mZona Inicial (Deve introduzir o código da zona (XXXX)): \033[0m")
            if zonaInicial == "0":
                menuAdicionar()
            else:
                if zonaInicial in codigosZonas:
                    break
                else:
                    print("\033[31m O código que introduziu não se encontra na tabela de zonas. Por favor, introduza um código válido\033[0m")

        while True:
            zonaFinal = input("0 - Voltar ao menu\n\033[34m\033[1mZona Final: (Deve introduzir o código da zona (XXXX)) \033[0m")
            if zonaFinal == "0":
                menuAdicionar()
            else:
                if zonaFinal in codigosZonas:
                    break
                else:
                    print("\033[31m O código que introduziu não se encontra na tabela de zonas. Por favor, introduza um código válido\033[0m")

        
        while True:
            dificuldade = input("Dificuldade:\n1- Fácil\n2- Intermédia\n3- Difícil\n4- Muito difícil\n\033[34m\033[1m Escolha uma opção: \033[0m")
            if dificuldade == "1":
                dificuldade = "Facil"
                break
            elif dificuldade == "2":
                dificuldade = "Intermedia"
                break
            elif dificuldade == "3":
                dificuldade = "Dificil"
                break
            elif dificuldade == "4":
                dificuldade = "Muy dificil"
                break
            else:
                print("\033[31mEscolha uma opção válida\033[0m")

        while True:
            estado = input("Estado Atual:\n1- Aberta\n2- Fechada\n\033[34m\033[1mEscolha uma opção: \033[0m")
            if estado == "1":
                estado = "Aberta"
                break
            elif estado == "2":
                estado = "Fechada"
                break
            else:
                print("\033[31mEscolha uma opção válida\033[0m")

        novaPista = {
            "CodigoPista": gerarCodigo(),
            "Nome": nomePista,
            "ZonaInicial": zonaInicial,
            "ZonaFinal": zonaFinal,
            "Dificuldade": dificuldade,
            "Estado": estado
        }

        dfPistaCreada = pd.DataFrame([novaPista])
        df = pd.concat([df, dfPistaCreada], ignore_index=True)
        df.to_csv("dados/tabela_pistas.txt", index=False)
        print("\033[32m\033[1mA operação foi concluída com sucesso!!\033[0m")

    
def adicionarSeccao():
    df = pd.read_csv("dados/tabela_seccoes.txt")
    dfZonas = pd.read_csv("dados/tabela_zonas.txt")
    dfZonasCodigoENome = dfZonas[["CodigoZona", "Nome"]]
    codigosZonas = dfZonas["CodigoZona"].tolist()

    dfPistas = pd.read_csv("dados/tabela_pistas.txt")
    dfPistasCodigoENome = dfPistas[["CodigoPista", "Nome"]]
    codigosPistas = dfPistas["CodigoPista"].tolist()

    if dfZonas.empty or dfPistas.empty or len(codigosZonas) < 2:
        print("\033[31mPara adicionar uma secção deve haver pelo menos 2 zonas e 1 pista existente\033[0m")
        menuAdicionar()
    else:
        print("Estas são as zonas existentes (Com o seu código)")
        print(dfPistasCodigoENome.to_string(index=False))  

        while True:
            codigoPista = input("0 - Voltar ao menu\n\033[34m\033[1mCódigo da pista associada (Debe introducir o código da pista (XXXX)): \033[0m")
            if codigoPista == "0":
                menuAdicionar()
            else:
                if codigoPista in codigosPistas:
                    break
                else:
                    print("\033[31mO código de pista não se encuentra na tabela de pistas. Por favor, introduza un código válido\033[0m")

        if dfZonas.empty:
            print("\033[31mPara adicionar uma secção deve haver pelo menos 2 zonas existente, actualmente não há 2 zonas\033[0m")
            menuAdicionar()
        else:
            print("Estas são as zonas existentes (Com o seu código)")
            print(dfZonasCodigoENome.to_string(index=False))

            while True:
                zonaInicial = input("0 - Voltar ao menu\n\033[34m\033[1mZona Inicial (Deve introduzir o código da zona (XXXX)): \033[0m")
                if zonaInicial == "0":
                    menuAdicionar()
                else:
                    if zonaInicial in codigosZonas:
                        break
                    else:
                        print("\033[31mO código que introduziu não se encontra na tabela de zonas. Por favor, introduza um código válido\033[0m")

            while True:
                zonaFinal = input("0 - Voltar ao menu\n\033[34m\033[1mZona Final: (Deve introduzir o código da zona (XXXX)) \033[0m")
                if zonaFinal == "0":
                    menuAdicionar()
                else:
                    if zonaFinal in codigosZonas:
                        break
                    else:
                        print("\033[31mO código que introduziu não se encontra na tabela de zonas. Por favor, introduza um código válido\033[0m")      
            
            codigoSeccao = zonaInicial + '-' + zonaFinal

            # Obtenemos las coordenadas de la ZonaInicio y ZonaFim
            
            start = dfZonas[dfZonas['CodigoZona'] == zonaInicial][['Longitude', 'Latitude']].values[0]
            end = dfZonas[dfZonas['CodigoZona'] == zonaFinal][['Longitude', 'Latitude']].values[0]

            # Calculamos la distancia entre los puntos
            x1, y1 = start
            x2, y2 = end
            distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

            
            novaSeccao = {
                "CodigoSecção": codigoSeccao,
                "ZonaInicio": zonaInicial,
                "ZonaFim": zonaFinal,
                "Distancia": round(distancia),
            }
            
            dfSeccaoCreada = pd.DataFrame([novaSeccao])
            df = pd.concat([df, dfSeccaoCreada], ignore_index=True)
            df.to_csv("dados/tabela_seccoes.txt", index=False)

            dfSeccoesPista = pd.read_csv("dados/tabelas_seccoes_pistas.txt")
            novaSeccaoPista = {
            "PistaAssociada": codigoPista,
            "SecçãoAssociada": codigoSeccao,
            }

            dfNovaSeccaoPista = pd.DataFrame([novaSeccaoPista])
            dfSeccoesPista = pd.concat([dfSeccoesPista, dfNovaSeccaoPista], ignore_index=True)
            dfSeccoesPista.to_csv("dados/tabelas_seccoes_pistas.txt", index=False)
    
def adicaoZonaEComodidades():

    # Criação da zona

    df = pd.read_csv("dados/tabela_zonas.txt")

    while True:
        nome = input("0 - Voltar ao menu\n\033[34m\033[1mIntroduz o nome da zona: \033[0m")
        if nome == "":
            print("\033[31mPor favor, introduza o nome\033[0m")
        else:
            if nome == "0":
                menuAdicionar()
            else:
                break

    while True:
        try:
            latitude = float(input("\033[34m\033[1mIntroduza a latitude da pista: \033[0m"))
            break
        except ValueError:
            print("\033[31mPor favor, introduza uma latitude válida\033[0m")
    while True:
            try:
                longitude = float(input("\033[34m\033[1mIntroduza a longitude da pista: \033[0m"))
                break
            except ValueError:
                print("\033[31mPor favor, introduza uma longitude válida\033[0m")
    while True:
            try:
                altitude = float(input("\033[34m\033[1mintroduza a altitude da pista: \033[0m"))
                break
            except ValueError:
                print("\033[31mPor favor, introduza uma altitude válida\033[0m")

        
    descricao = input("\033[34m\033[1mIntroduza a descrição da zona: \033[0m")

    CodigoZona = gerarCodigo()

    novaZona = {
        "CodigoZona": CodigoZona,
        "Nome": nome,
        "Latitude": latitude,
        "Longitude": longitude,
        "Altitude": altitude,
        "Descrição": descricao
    }

    dfZonaCreada = pd.DataFrame([novaZona])

    df = pd.concat([df, dfZonaCreada], ignore_index=True)
    
    df.to_csv("dados/tabela_zonas.txt", index=False)

    #Criação da/s comodidad/es

    dfComodidade = pd.read_csv("dados/tabela_comodidades.txt")

    descricaoComodide = input("\033[34m\033[1mIntroduza as comodidades que deseja que a zona tenha (WC/Restaurante/Snowpark...): \033[0m")
    nomeComodidade = input("\033[34m\033[1mIntroduza como quer chamar às comodidades: \033[0m")
    

    ComodidadeNova = {
        "Nome": nomeComodidade,
        "ZonaAssociada": CodigoZona,
        "Descrição": descricaoComodide
    }

    dfComodidadeCreada = pd.DataFrame([ComodidadeNova])

    dfComodidade = pd.concat([dfComodidade,dfComodidadeCreada], ignore_index=True)

    dfComodidade.to_csv("dados/tabela_comodidades.txt", index=False) 

def adicaoMeioMecanico():
    df = pd.read_csv("dados/tabela_meios_mecanicos.txt")
    dfZonas = pd.read_csv("dados/tabela_zonas.txt")
    dfZonasCodigoENome = dfZonas[["CodigoZona", "Nome"]]
    codigosZonas = dfZonas["CodigoZona"].tolist()

    if dfZonas.empty:
        print("\033[31mPara adicionar um meio mecanico deve haver pelo menos 2 zonas existente, actualmente não há 2 zonas\033[0m")
        menuAdicionar()
    else:
        
        while True:
            nome = input("\033[34m\033[1mNome do meio mecánico: \033[0m")
            if nome == "":
                print("\033[31mPor favor, introduza o nome\033[0m")
            else:
                break

        while True:
            print("Estas são as zonas existentes (com o seu código)")
            print(dfZonasCodigoENome.to_string(index=False))
            zonaPartida = input("0 - Voltar ao inicio\n\033[34m\033[1mZona Inicial (Deve introduzir o código da zona (XXXX)): \033[0m")
            if zonaPartida == "0":
                menuAdicionar()
            else:
                if zonaPartida in codigosZonas:
                    break
                else: 
                    print("\033[31mO código que introduziu não se encontra na tabela de zonas. Por favor, introduza um código válido\033[0m")

        while True:
            zonaChegada = input("0 - Voltar ao inicio\n\033[34m\033[1mZona Final: (Deve introduzir o código da zona (XXXX)) \033[0m")
            if zonaChegada == "0":
                menuAdicionar()
            else:
                if zonaChegada in codigosZonas:
                    break
                else:
                    print("\033[31mO código que introduziu não se encontra na tabela de zonas. Por favor, introduza um código válido\033[0m")
                
        

        while True:
            
            estado = input("Estado: \n1 - Aberto\n2 - Fechado\n\033[34m\033[1mEscolha uma opção: \033[0m")
            if estado == '1':
                estado = 'Aberta'
                break
            elif estado == '2':
                estado = 'Fechada'
                break
            else:
                print("\033[31mEscolha uma opção válida\033[0m")


        while True:
            tipo = input("Tipo de meio mecánico: \n1 - Uni-direccional\n2 - Bi-direccional\n\033[34m\033[1mEscolha uma opção: \033[0m")
            if tipo == '1':
                tipo = 'Uni-direccional'
                break
            elif tipo == '2':
                tipo = 'Bi-direccional'
                break
            else:
                print("\033[31mEscolha uma opção válida\033[0m")
    

        novoMeioMecanico = {
            "Nome": nome,
            "ZonaPartida": zonaPartida,
            "ZonaChegada": zonaChegada,
            "Estado": estado,
            "Tipo": tipo
        }

        dfMeioMecanicoCreada = pd.DataFrame([novoMeioMecanico])
        df = pd.concat([df, dfMeioMecanicoCreada], ignore_index=True)
        df.to_csv("dados/tabela_meios_mecanicos.txt", index=False)
        print("\033[32m\033[1mA operação foi concluída com sucesso!!\033[0m")


def menuAlterarEstado():
    print("1 - Pista\n2 - Meio mecánico\n0 - Voltar ao menu inicial")
    opcao = input("\033[34m\033[1mEscolha uma opção: \033[0m")
    
    if opcao == "1":
        alterarEstadoPistas()
        print("\033[32m\033[1mA operação foi concluída com sucesso!!\033[0m")
        menuAlterarEstado()
    elif opcao == "2":
        alterarEstadoMeioMecanico()
        print("\033[32m\033[1mA operação foi concluída com sucesso!!\033[0m")
        menuAlterarEstado()
    elif opcao == "0":
        menuInicial("v")
    else:
        print("\033[31mEscolha uma opção válida\033[0m")
        menuAlterarEstado()

def alterarEstadoPistas():

    df = pd.read_csv("dados/tabela_pistas.txt")
    dfNomeEEstado = df[["Nome", "Estado"]]

    if dfNomeEEstado.empty:
        print("\033[31mPara alterar o estado de uma pista deve haver pelo menos 1 pista existente, actualmente não há nenhuma pista\033[0m")
        menuAlterarEstado()
    else:
        print("Estas são as zonas existentes e o seu estado:")
        print(dfNomeEEstado.to_string(index=False))

        while True:
            nomePista = input("\033[34m\033[1mNome da pista: \033[0m")
            if nomePista not in df['Nome'].values:
                print('\033[31mEssa pista não existe, por favor escolha uma pista que exista\033[0m')
            else:
                break

        novoEstado = input("Novo estado: \n1 - Aberta\n2 - Fechada\n\033[34m\033[1mEscolha uma opção: \033[0m")
        
        while True:
        
            if novoEstado == '1':
                novoEstado = 'Aberta'
                break
            elif novoEstado == '2':
                novoEstado = 'Fechada'
                break
            else:
                print("\033[31mEscolha uma opção válida\033[0m")
                novoEstado = input("Novo estado: \n1 - Aberta\n2 - Fechada\n\033[34m\033[1mEscolha uma opção: \033[0m")
        

        # Seleccionar la fila con el nombre de pista que se desea alterar
        df_fila_selec = df.loc[df["Nome"] == nomePista]
        
        # Asignar el nuevo estado a la columna "Estado" de la fila seleccionada
        df_fila_selec.at[df_fila_selec.index[0], "Estado"] = novoEstado
        
        df.update(df_fila_selec)
        
        df.to_csv("dados/tabela_pistas.txt", index=False)

def alterarEstadoMeioMecanico():

    df = pd.read_csv("dados/tabela_meios_mecanicos.txt")
    dfNomeEEstado = df[["Nome", "Estado"]]

    if dfNomeEEstado.empty:
        print("\033[31mPara alterar o estado de um meio mecanico deve haver pelo menos 1 meio mecanico existente, actualmente não há nenhum\033[0m")
        menuAlterarEstado()
    else:
        print("Estas são os meios mecánicos existentes e o seu estado:")
        print(dfNomeEEstado.to_string(index=False))
        while True:
            nomeMeio = input("\033[34m\033[1mmNome do meio mecánico a alterar: \033[0m")
            if nomeMeio not in df['Nome'].values:
                print('\033[31mEsse meio mecánico não existe, por favor escolha um meio mecánico que exista\033[0m')
            else:
                break
        
        novoEstado = input("Novo estado: \n1 - Aberto\n2 - Fechado\n\033[34m\033[1mEscolha uma opção: \033[0m")

        while True:
            if novoEstado == '1':
                novoEstado = 'Aberto'
                break
            elif novoEstado == '2':
                novoEstado = 'Fechado'
                break
            else:
                print("\033[31mEscolha uma opção válida\033[0m")
                novoEstado = input("Novo estado: \n1 - Aberto\n2 - Fechado\n\033[34m\033[1mEscolha uma opção: \033[0m")    

        df_fila_selec = df.loc[df["Nome"] == nomeMeio]
        
        # Asignar el nuevo estado a la columna "Estado" de la fila seleccionada
        df_fila_selec.at[df_fila_selec.index[0], "Estado"] = novoEstado
        
        # Actualizar la fila seleccionada en el dataframe original
        df.update(df_fila_selec)
        
        df.to_csv("dados/tabela_meios_mecanicos.txt", index=False)

        print("\033[32m\033[1mA operação foi concluída com sucesso!!\033[0m")


def menuBilhete():
    print("1 - Emissão de bilhete\n2 - Listagem de Bilhetes\n3 - Listagem de Bilhetes para um Dia\n4 - Listagem de Bilhetes por Periodo\n5 - Procura de Bilhete por Referência\n0 - Voltar ao menu inicial")
    opcao = input("\033[34m\033[1mEscolha uma opção: \033[0m")
    if opcao == "1":
        emitirBilhete()
        print("\033[32m\033[1mA operação foi concluída com sucesso!!\033[0m")
        menuBilhete()
    elif opcao == "2":
        verListagemBilhetesEmitidos()
        menuBilhete()
    elif opcao == "3":
        procurarBilhetePorDia()
        menuBilhete()
    elif opcao == "4":
        procurarBilhetePorRango()
        menuBilhete()
    elif opcao == "5":
        procuraBilheteEmitidoPorReferencia()
        menuBilhete()
    elif opcao == "0":
        menuInicial("v")
    else:
        print("\033[31mEscolha uma opção válida\033[0m")
        menuBilhete() 

def calcularDuracaoBilhete(tipoBilhete):
    df = pd.read_csv('dados/tabela_tipo_bilhetes.txt')  # Leemos el archivo y almacenamos los datos en un DataFrame
    duration = df[df['Nome'] == tipoBilhete]['Duração'].values[0]  # Seleccionamos la duración del billete solicitado
    return eval(duration)

def emitirBilhete():

    df = pd.read_csv("dados/tabela_bilhetes.txt")

    while True:
        nomePessoa = input("\033[34m\033[1mIntroduza o nome titular do bilhete: \033[0m")
        if nomePessoa == "":
            print("\033[31mPor favor, introduza o nome\033[0m")
        else:
            break
    while True:
        nacionalidade = input("\033[34m\033[1mIntroduza a nacionalidade: \033[0m")
        if nacionalidade == "":
            print("\033[31mPor favor, introduza a nacionalidade\033[0m")
        else:
            break

    while True:
        tipoBilhete = input("Tipos de Bilhetes:\n1 - Diário\n2 - Semanal\n3 - Mensal\n4 - Anual\033[34m\033[1m\nEscolha o tipo de bilhete: \033[0m") 
        if tipoBilhete == '1':
            tipoBilhete = 'diario'
            break
        elif tipoBilhete == '2':
            tipoBilhete = 'semanal'
            break
        elif tipoBilhete == '3':
            tipoBilhete = 'mensal'
            break
        elif tipoBilhete == '4':
            tipoBilhete = 'anual'
            break
        else:
            print("\033[31mEscolha uma opção válida\033[0m")

    # Generar una referencia única para el bilhete
    if df["ReferênciaBilhete"].notnull().any():
        referencia = df["ReferênciaBilhete"].max() + 1
    else:
        referencia = 1
    
    inicio = datetime.datetime.today()

    vencimento = inicio + calcularDuracaoBilhete(tipoBilhete)

    nova_linha = {
        "ReferênciaBilhete": int(referencia),
        "NomePessoa": nomePessoa,
        "Nacionalidade": nacionalidade,
        "TipoBilhete": tipoBilhete,
        "DiaInicio": inicio.day,
        "MêsInicio": inicio.month,
        "AnoInicio": inicio.year,
        "DiaFim": vencimento.day,
        "MêsFim": vencimento.month,
        "AnoFim": vencimento.year,
    }

    # Puse esto porque la columna de AnoFim se mostraba como float
    df["AnoFim"] = df["AnoFim"].astype(int)

    df_nova_linha = pd.DataFrame([nova_linha])

    # Concatenar el dataframe de la nueva fila al dataframe de bilhetes existentes
    df = pd.concat([df, df_nova_linha], ignore_index=True)

    df.to_csv("dados/tabela_bilhetes.txt", index=False)

    # Creacao do Codigo QR
    billete_info = "Ref: {0}\nNome: {1} \nVencimiento: {2}/{3}/{4}".format(
        nova_linha["ReferênciaBilhete"],
        nova_linha["NomePessoa"],
        nova_linha["DiaFim"],
        nova_linha["MêsFim"],
        nova_linha["AnoFim"],
    )

    # Crear una instancia de QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Añadir la información del billete al QR
    qr.add_data(billete_info)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Guardar la imagen del QR en un archivo con el nombre de la referencia del billete
    nome_arquivo = "{0}.png".format(nova_linha["ReferênciaBilhete"])
    img.save("codigo/qr/" + nome_arquivo)

def verListagemBilhetesEmitidos():
    df = pd.read_csv("dados/tabela_bilhetes.txt")
    if df.empty:
        print("\033[31mActualmente não existem bilhetes no sistema\033[0m")
        menuBilhete()
    else:
        print(df.to_string(index=False))
        print("\033[32m\033[1mA operação foi concluída com sucesso!!\033[0m")


def procurarBilhetePorDia():
    df = pd.read_csv("dados/tabela_bilhetes.txt")

    if df.empty:
        print("\033[31mActualmente não existem bilhetes no sistema\033[0m")
        menuBilhete()
    else:
        df = df.rename(columns={'DiaInicio': 'day', 'MêsInicio': 'month', 'AnoInicio': 'year'})

        # Convertir las columnas de fechas a objetos datetime
        df['FechaInicio'] = pd.to_datetime(df[['year', 'month', 'day']])

        df = df.drop(columns=['year', 'month', 'day'])

        df = df.rename(columns={'DiaFim': 'day', 'MêsFim': 'month', 'AnoFim': 'year'})

        df['FechaFin'] = pd.to_datetime(df[['year', 'month', 'day']])

        df = df.drop(columns=['year', 'month', 'day'])

        while True:
            try:
                ano_inicio = int(input('\033[34m\033[1mAno de inicio: \033[0m'))            

                while True:
                    try:
                        mes_inicio = int(input('\033[34m\033[1mMês de inicio: \033[0m'))
                        
                        if mes_inicio < 1 or mes_inicio > 12:
                            raise ValueError
                        
                        break
                    except ValueError:
                        print('\033[31mPor favor, introduza um mês válido\033[0m')
                while True:
                    try:
                        dia_inicio = int(input('\033[34m\033[1mDia de inicio: \033[0m'))
                        
                        if dia_inicio < 1 or dia_inicio > 31:
                            raise ValueError
                        
                        # Comprobar si el mes ingresado tiene el número correcto de días
                        if mes_inicio in (4, 6, 9, 11) and dia_inicio > 30:
                            raise ValueError
                        elif mes_inicio == 2 and dia_inicio > 28:
                            raise ValueError
                        
                        break
                    except ValueError:
                        print('\033[31mPor favor, introduza um dia válido para o mês seleccionado\033[0m')
                break  
            except ValueError:
                print('\033[31mPor favor, introduza un número válido\033[0m')   

        data = datetime.datetime(ano_inicio, mes_inicio, dia_inicio)

        df_filtrado = df.query('FechaInicio == "{}"'.format(data))

        if df_filtrado.empty:
            print("\033[31mNão foram encontrados bilhetes com os dias especificados\033[0m")
        else:
            print(df_filtrado.to_string(index=False))
            print("\033[32m\033[1mA operação foi concluída com sucesso!!\033[0m")


def procurarBilhetePorRango():
    df = pd.read_csv("dados/tabela_bilhetes.txt")
    if df.empty:
        print("\033[31mActualmente não existem bilhetes no sistema\033[0m")
        menuBilhete()
    else:
        df = df.rename(columns={'DiaInicio': 'day', 'MêsInicio': 'month', 'AnoInicio': 'year'})

        # Convertir las columnas de fechas a objetos datetime
        df['FechaInicio'] = pd.to_datetime(df[['year', 'month', 'day']])

        df = df.drop(columns=['year', 'month', 'day'])

        df = df.rename(columns={'DiaFim': 'day', 'MêsFim': 'month', 'AnoFim': 'year'})

        df['FechaFin'] = pd.to_datetime(df[['year', 'month', 'day']])

        df = df.drop(columns=['year', 'month', 'day'])

        # Solicitar al usuario que introduzca el rango de fechas
        while True:
            try:
                while True:
                    ano_inicio = int(input('Ano de inicio: '))
                    ano_fim = int(input('Ano de fim: '))
                    if ano_inicio <= ano_fim and ano_inicio >= 1678 and ano_inicio <= 2262 and ano_fim >= 1678 and ano_fim <= 2262:
                        break
                    print('Los años de inicio y fin deben ser valores mayores o iguales a 1678 y menores o iguales a 2262.')

                while True:
                    try:
                        mes_inicio = int(input('Mes de inicio: '))
                        mes_fin = int(input('Mes de fim: '))
                        if mes_inicio < 1 or mes_inicio > 12 or mes_fin < 1 or mes_fin > 12:
                            raise ValueError
                        break
                    except ValueError:
                        print('Por favor, ingresa números entre 1 y 12 para ambos meses.')
                while True:
                    try:
                        dia_inicio = int(input('Dia de inicio: '))
                        dia_fin = int(input('Dia de fim: '))
                        if dia_inicio < 1 or dia_inicio > 31 or dia_fin < 1 or dia_fin > 31:
                            raise ValueError
                        break
                    except ValueError:
                        print('Por favor, ingresa números entre 1 y 31 para ambos días.')

                fecha_inicio = datetime.datetime(ano_inicio, mes_inicio, dia_inicio)
                fecha_fin = datetime.datetime(ano_fim, mes_fin, dia_fin)

                if fecha_inicio > fecha_fin:
                    print('La fecha de inicio debe ser menor o igual a la fecha de fin.')
                    continue

                break
            except ValueError:
                print('Por favor, ingresa un numero valido')

        # Crear el rango de fechas a partir de los valores introducidos por el usuario
        rango_fechas = pd.date_range(start=pd.datetime(ano_inicio, mes_inicio, dia_inicio), end=pd.datetime(ano_fim, mes_fin, dia_fin))

        df_filtrado = df[df['FechaInicio'].isin(rango_fechas) & df['FechaFin'].isin(rango_fechas)]

        if df_filtrado.empty:
            print("\033[31mNenhum bilhete com a referência especificada encontrado\033[0m")
        else:
            print(df_filtrado.to_string(index=False))
            print("\033[32m\033[1mA operação foi concluída com sucesso!!\033[0m")


def procuraBilheteEmitidoPorReferencia():
    df = pd.read_csv("dados/tabela_bilhetes.txt")
    if df.empty:
        print("\033[31mActualmente não existem bilhetes no sistema\033[0m")
    else:
        dfReferenciasBilhetes = df["ReferênciaBilhete"]

        print("Estas são todas as referências dos bilhete existentes")
        print(dfReferenciasBilhetes.to_string(index=False))

        while True:
            try:
                referencia = int(input("\033[34m\033[1mintroduza a referência do bilhete que procura: \033[0m"))
                break
            except ValueError:
                print("\033[31mPor favor, introduza um número (as referências são apenas por número\033[0m")

        # tem que ser int(referencia) porque na tabela esta en forma int
        df = df.loc[df["ReferênciaBilhete"] == referencia]
        if df.empty:
            print("\033[31mNenhum bilhete com a referência especificada encontrado\033[0m")
            menuBilhete()
        else:
            print(df.to_string(index=False))
            print("\033[32m\033[1mA operação foi concluída com sucesso!!\033[0m")

def dibujarMapa():
    df_points = pd.read_csv('dados/tabela_zonas.txt', sep=',')
    df_sections = pd.read_csv('dados/tabela_seccoes.txt', sep=',')

    if df_points.empty or df_sections.empty:
       print("\033[31mTabelas vacia\033[0m")
    else:
        # Leemos la tabla de puntos y la almacenamos en un diccionario
        points = {}
        
        for _, row in df_points.iterrows():
            points[row['CodigoZona']] = (row['Longitude'], row['Latitude'])

        # Leemos la tabla de secciones y dibujamos las líneas
        
        for _, row in df_sections.iterrows():
            start = points[row['ZonaInicio']]
            end = points[row['ZonaFim']]
            plt.plot([start[0], end[0]], [start[1], end[1]], 'k-')

        # Graficamos los puntos y las etiquetas con sus nombres
        plt.scatter(df_points['Longitude'], df_points['Latitude'])
        for label, x_coord, y_coord in zip(df_points['CodigoZona'], df_points['Longitude'], df_points['Latitude']):
            plt.annotate(label, (x_coord, y_coord))

        plt.show()

menuInicial(opcaoInicial)


