class AutomatoFinito:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_finais, deterministico=True):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais
        self.deterministico = deterministico

    def verificarDeterministico(self):
        for estado in self.estados:
            for simbolo in self.alfabeto:
                # verifica se há mais de um estado de destino para o mesmo símbolo
                if estado in self.transicoes and simbolo in self.transicoes[estado]:
                    if len(self.transicoes[estado][simbolo]) > 1:
                        return False
                # verifica se há transições ε 
                if estado in self.transicoes and '' in self.transicoes[estado]:
                    return False
        return True

    def __str__(self):
        resultado = f"M = ({self.alfabeto}, {self.estados}, δ, {self.estado_inicial}, {self.estados_finais})\n"
        resultado += "Transições:\n"
        for estado, transicoes in self.transicoes.items():
            for simbolo, proximos_estados in transicoes.items():
                resultado += f"  δ({estado}, {simbolo}) -> {', '.join(proximos_estados)}\n"
        return resultado

class GramaticaRegular:
    def __init__(self, automato):
        self.nao_terminais = automato.estados | {"S"}
        self.terminais = automato.alfabeto
        self.simbolo_inicial = "S"
        self.producoes = self.gerarProducoes(automato)

    def gerarProducoes(self, automato):
        producoes = {estado: [] for estado in automato.estados}
        producoes["S"] = [f"{automato.estado_inicial}"]
       
        for estado, transicoes in automato.transicoes.items():
            for simbolo, proximos_estados in transicoes.items():
                for proximo_estado in proximos_estados:
                    producoes[estado].append(f"{simbolo}{proximo_estado}")
       
        for estado_final in automato.estados_finais:
            producoes[estado_final].append("ε")

        return producoes

    def __str__(self):
        resultado = f"G = ({self.nao_terminais}, {self.terminais}, P, {self.simbolo_inicial})\n"
        resultado += "Produções:\n"
        for nao_terminal, regras in self.producoes.items():
            resultado += f"  {nao_terminal} -> " + " | ".join(regras) + "\n"
        return resultado

def lerArquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
   
    estados = set(linhas[0].strip().split())
    alfabeto = set(linhas[1].strip().split())
   
    transicoes = {}
    for linha in linhas[2:]:
        if linha.strip() == "":
            break
        partes = linha.strip().split()
        estado = partes[0]
        simbolo = partes[1]
        proximos_estados = set(partes[2:])
       
        if estado not in transicoes:
            transicoes[estado] = {}
        transicoes[estado][simbolo] = proximos_estados
   
    estado_inicial = linhas[-2].strip()
    estados_finais = set(linhas[-1].strip().split())
   
    # verificacoes
    if not estados:
        raise ValueError("Erro: O arquivo não contém estados.")
    if not alfabeto:
        raise ValueError("Erro: O arquivo não contém um alfabeto.")
    if not estado_inicial:
        raise ValueError("Erro: O arquivo não contém um estado inicial.")
    if not estados_finais:
        raise ValueError("Erro: O arquivo não contém estados finais.")
    if estado_inicial not in estados:
        raise ValueError("Erro: O estado inicial não está entre os estados do autômato.")
    if '' in alfabeto:
        raise ValueError("Erro: O alfabeto não pode conter o terminal vazio (ε).")
    if not estados_finais.issubset(estados):
        raise ValueError("Erro: Um ou mais estados finais não estão no conjunto de estados do autômato.")

    # verifica se os símbolos das transições estão no alfabeto
    for estado, transicoes_por_estado in transicoes.items():
        for simbolo in transicoes_por_estado.keys():
            if simbolo not in alfabeto:
                raise ValueError(f"Erro: O símbolo '{simbolo}' usado nas transições não está no alfabeto.")

    return AutomatoFinito(estados, alfabeto, transicoes, estado_inicial, estados_finais, deterministico=False)

def escreverArquivo(automato, gramatica, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        arquivo.write("Informações do Autômato:\n")
        arquivo.write(str(automato))
        
        # verifica se o automato é deterministico ou não deterministico
        if automato.verificarDeterministico():
            arquivo.write("\nO autômato é um AFD (Autômato Finito Determinístico).\n")
        else:
            arquivo.write("\nO autômato é um AFND (Autômato Finito Não Determinístico).\n")
        
        arquivo.write("\n\nInformações da Gramática Regular:\n")
        arquivo.write(str(gramatica))

def gerarArquivo(entrada, saida):
    try:
        automato = lerArquivo(entrada)
        gramatica = GramaticaRegular(automato)
        escreverArquivo(automato, gramatica, saida)
    except ValueError as e:
        with open(saida, 'w', encoding='utf-8') as arquivo:
            arquivo.write(f"Erro: {str(e)}\n")
        

arquivoEntrada = 'automato.txt'
arquivoSaida = 'saida.txt'
gerarArquivo(arquivoEntrada, arquivoSaida)