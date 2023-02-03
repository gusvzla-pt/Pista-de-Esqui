import pandas as pd

print("1 - Consultar Lista de Pistas\n2 - Consultar Meios Mecanicos\n3 - Consultar Zonas\n4 - Procurar Pistas\n5 - Procurar Meios Mecanicos")
opcaoInicial = input("\033[34m\033[1mEscolha uma opção: \033[0m")

def menuInicial(opcao):
        if opcao == '1':
            menuPista()
        elif opcao == '2':
            consultarMeiosMecanicos()
            menuInicial("v")
        elif opcao == '3':
            menuZona()
        elif opcao == '4':
            obterPistas()
            menuInicial("v")
        elif opcao == '5':
            procurarMeiosMecanicos()
            menuInicial("v")    
        elif opcao == 'v':
            print("1 - Consultar Pistas\n2 - Consultar Meios Mecanicos\n3 - Consultar Zonas\n4 - Procurar Pistas\n5 - Procurar Meios Mecanicos")
            opcao = input("\033[34m\033[1mEscolha uma opção: \033[0m")
            menuInicial(opcao)
        else:
            print("\033[31mEscolha uma opção válida\033[0m")
            opcaoNova = input("1 - Consultar Pistas\n2 - Consultar Meios Mecanicos\n3 - Consultar Zonas\n4 - Procurar Pistas\n5 - Procurar Meios Mecanicos\n\033[34m\033[1mEscolha uma opção: \033[0m")
            menuInicial(opcaoNova)

def menuPista():
    print("1 - Listar Pistas\n2 - Listar Pistas E Secções\n0 - Voltar ao Menu Inicial")
    opcao = input("\033[34m\033[1mEscolha uma opção: \033[0m")
    if opcao == '1':
        consultarPistas()
        menuPista()
    elif opcao == '2':
        consultarPistasComSeccoes()
        menuPista()
    elif opcao == '0':
        menuInicial('v')
    else:
        print("\033[31mEscolha uma opção válida\033[0m")
        menuPista()

def consultarPistas():
    df = pd.read_csv("dados/tabela_pistas.txt")
    if df.empty:
        print("\033[31mPara procurar uma pista deve haver pelo menos 1 pista existente, actualmente não há nenhuma\033[0m")
    else:
        # index=false serve para tirar a coluna de index  
        print(df.to_string(index=False))

def consultarPistasComSeccoes():
    df1 = pd.read_csv("dados/tabela_pistas.txt")
    df2 = pd.read_csv("dados/tabelas_seccoes_pistas.txt")

    if df1.empty:
        print("\033[31mPara procurar uma pista deve haver pelo menos 1 pista existente, actualmente não há nenhuma\033[0m")
    else:
        # Dar um novo nome no campo 'CodigoPista' no primeiro dataframe para este coincidir com o campo 'PistaAssociada' no segundo dataframe 
        df1 = df1.rename(columns={'CodigoPista': 'PistaAssociada'})

        # Usar merge para combinar ambos dataframes num só
        result = pd.merge(df1, df2, on='PistaAssociada')

        # Agrupar os dados de SecçãoAssociada por PistaAssociada y obter uma lista de todas as SecçãoAssociada para cada PistaAssociada
        result2 = result.groupby('PistaAssociada')['SecçãoAssociada'].apply(list).reset_index()

        # combinar os dois dataframe obtidos para que este mostre a informação junta
        result3= pd.merge(result, result2, on='PistaAssociada')

        #elimino uma coluna que se duplicou
        result3 = result3.drop(columns=['SecçãoAssociada_x'])

        # Mudo o nome da coluna duplicada que ficou
        result3 = result3.rename(columns={'SecçãoAssociada_y': 'SecçãoAssociada'})

        #elimino os duplicados filtrando por PistaAssociada
        result3 = result3.drop_duplicates(subset='PistaAssociada')

        # conversão da lista numa string
        result3['SecçãoAssociada'] = result3['SecçãoAssociada'].apply(', '.join)

        print(result3.to_string(index=False))

def consultarMeiosMecanicos():
    df = pd.read_csv("dados/tabela_meios_mecanicos.txt")

    if df.empty:
        print("\033[31mPara procurar um meio mecanico deve haver pelo menos 1 meios mecanico existente, actualmente não há nenhum\033[0m")
    else:
        print(df.to_string(index=False))

def menuZona():
    print("1 - Listar Zonas\n2 - Listar Zonas E Comodidades\n0 - Voltar ao Menu Inicial")
    opcao = input("\033[34m\033[1mEscolha uma opção: \033[0m") 
    if opcao == '1':
        consultarZonas()
        menuZona()
    elif opcao == '2':
        consultarZonasEmDetalhe()
        menuZona()
    elif opcao == '0':
        menuInicial('v')
    else:
        print("\033[31mEscolha uma opção válida\033[0m")
        menuZona()
            
def consultarZonas():
    df = pd.read_csv("dados/tabela_zonas.txt")
    if df.empty:
        print("\033[31mPara procurar uma zona deve haver pelo menos 1 zona existente, actualmente não há nenhuma\033[0m")
    else:
        print(df.to_string(index=False))

def consultarZonasEmDetalhe():
    df1 = pd.read_csv("dados/tabela_zonas.txt")
    df2 = pd.read_csv("dados/tabela_comodidades.txt")

    if df1.empty:
        print("\033[31mPara procurar uma zona deve haver pelo menos 1 zona existente, actualmente não há nenhuma\033[0m")
    else:
        # Renomear o campo 'CodigoZona' no primeiro dataframe para que coincida com o campo 'ZonaAssociada' no segundo dataframe
        df1 = df1.rename(columns={'CodigoZona': 'ZonaAssociada'})

        df2 = df2.rename(columns={'Descrição': 'Comodidades'})

        # Usar merge para combinar ambos dataframes em um só
        df_mesclado = pd.merge(df1, df2, on='ZonaAssociada')

        # Agrupar os dados de ZonaAssociada por Comodidades e obter uma lista de todas as Comodidades para cada ZonaAssociada
        df_agrupado = df_mesclado.groupby('ZonaAssociada')['Comodidades'].apply(list).reset_index()

        # combinar os dois dataframes obtidos para que mostre a informação junta
        df_final = pd.merge(df_mesclado, df_agrupado, on='ZonaAssociada')

        # eliminar uma coluna que se duplicou
        df_final = df_final.drop(columns=['Comodidades_y'])

        # mudar o nome da coluna duplicada que ficou
        df_final = df_final.rename(columns={'Nome_y': 'NomeComodidad'})
        df_final = df_final.rename(columns={'Nome_x': 'NomeZona'})
        df_final = df_final.rename(columns={'Comodidades_x': 'Comodidades'})

        # eliminar os duplicados filtrando por ZonaAssociada
        df_final = df_final.drop_duplicates(subset='ZonaAssociada')

        print(df_final.to_string(index=False))

def obterPistas():

  df = pd.read_csv("dados/tabela_pistas.txt")
  dfZonaInicial = df[["ZonaInicial", "Nome"]]
  
  if df.empty:
        print("\033[31mPara procurar uma pista deve haver pelo menos 1 pista existente, actualmente não há nenhuma\033[0m")
  else:
    print("Estes são os nomes das pistas existentes juntamente com os seus códigos iniciais")
    print(dfZonaInicial.to_string(index=False))

    while True:
        zonaInicial = input("Escreve 0 se nao pretende procurar por Zona Inicial\n\033[34m\033[1mEscreve a zona inicial: \033[0m")

        if zonaInicial == "0":
            zonaInicial = None
            break
        elif df['ZonaInicial'].isin([zonaInicial]).any():
            # La zonaInicial existe, sai do bucle
            break
        else:
            print("\033[31mA zona de partida nao existe\033[0m")

    print("Escreve 0 se nao pretende procurar por dificuldade\nSelecione a dificuldade:\n1- Fácil\n2- Intermédia\n3- Difícil\n4- Muito Difícil")

    while True:
        dificuldade = input("\033[34m\033[1mEscreve a dificultade: \033[0m")
        if dificuldade == '1':
            dificuldade = "Facil"
            break
        elif dificuldade == '2':
            dificuldade = "Intermedia"
            break
        elif dificuldade == '3':
            dificuldade = "Dificil"
            break
        elif dificuldade == '4':
            dificuldade = "Muito dificil"
            break
        elif dificuldade == '0':
            dificuldade = None
            break
        else:
            print("\033[31mEscolha uma opção válida\033[0m")
            print("Escreve 0 se nao pretende procurar por dificuldade\nSelecione a dificuldade:\n1- Fácil\n2- Intermédia\n3- Difícil\n4- Muito Difícil")

    print("Escreve 0 se nao pretende procurar por estado\nSelecione o estado da pista:\n1- Aberta\n2- Fechada")
    
    estado = input("\033[34m\033[1mEscreve o estado: \033[0m")
    while True:
        if estado == '1':
            estado = "Aberta"
            break
        elif estado == '2':
            estado = "Fechada"
            break
        elif estado == '0':
            estado = None
            break
        else:
            print("\033[31mEscolha uma opção válida\033[0m")
            estado = input("Selecione o estado da pista:\n1- Aberta\n2- Fechada\n\033[34m\033[1mEscreve o estado: \033[0m")

    if zonaInicial == None and dificuldade == None and estado == None:
        menuInicial('v')

    # criar a lista de filtros
    query = []
    if zonaInicial is not None:
        query.append('ZonaInicial == "{}"'.format(zonaInicial))
    if dificuldade is not None:
        query.append('Dificuldade == "{}"'.format(dificuldade))
    if estado is not None:
        query.append('Estado == "{}"'.format(estado))
    # Join the query elements with "and"
    query = " and ".join(query)

    dfQuery = df.query(query)

    # Verificar se o dataframe filtrado esta vazio
    if query == "" or dfQuery.empty:
        print("\033[31mNão foram encontradas pistas que cumpram os critérios especificados\033[0m")
    else:
        print(dfQuery.to_string(index=False))


def procurarMeiosMecanicos(): 
    
  df = pd.read_csv("dados/tabela_meios_mecanicos.txt")
  dfNomeECodigoPartida = df[["Nome","ZonaPartida"]]

  if dfNomeECodigoPartida.empty:
    print("\033[31mPara procurar um meio mecanico deve haver pelo menos 1 meios mecanico existente, actualmente não há nenhum\033[0m")
  else:
    print("Estes são os nomes dos meios mecânicos e os códigos da zona de partida")
    print(dfNomeECodigoPartida)
    # Bucle para solicitar ao usuario que introduz a ZonaPartida até que se introduz um valor válido
    while True:
        zona_partida = int(input("\033[34m\033[1mZona de partida: \033[0m"))
        if df['ZonaPartida'].isin([zona_partida]).any():
            # La ZonaPartida existe, sai do bucle
            break
        else:
            print("\033[31mLa zona de partida no existe\033[0m")

    # Filtrar a tabela pela ZonaPartida
    df_filtrada = df.query('ZonaPartida == {}'.format(zona_partida))

    print(df_filtrada.to_string(index=False))

menuInicial(opcaoInicial)