import pandas as pd
import ast
import matplotlib.pyplot as plt
from LeIA.leia import SentimentIntensityAnalyzer

PATHS = ['Datafolha_Primeiro_Turno',
         'Datafolha_Segundo_Turno',
         'Debate_Band_Primeiro_Turno',
         'Debate_Band_Segundo_Turno',
         'Debate_Globo_Primeiro_Turno',
         'Debate_Globo_Segundo_Turno',
         'Eleicao_Primero_Turno',
         'Eleicao_Segundo_Turno',
         'Entrevista_Bolsonaro_Globo',
         'Entrevista_Lula_Globo']


def separate_data(path):
    data_loaded = pd.read_csv(path + '.csv')
    print(data_loaded)

    result = {
        'lula_tt': [],
        'bolsonaro_tt': [],
        'lula_and_bolsonaro_tt': [],
        'no_candidato': []
    }

    for indice, linha in data_loaded.iterrows():
        candidato = ast.literal_eval(linha['Candidato'])
        tweet = linha['Tweet']

        if len(candidato) == 0:
            result['no_candidato'].append(tweet)
        elif len(candidato) == 1:
            if candidato[0] == 'Lula':
                result['lula_tt'].append(tweet)
            else:
                result['bolsonaro_tt'].append(tweet)
        else:
            result['lula_and_bolsonaro_tt'].append(tweet)

    return result


def show_data_numbers(data_collection, caminho_arquivo):
    quantidade_lula = len(data_collection['lula_tt'])
    quantidade_bolsonaro = len(data_collection['bolsonaro_tt'])
    quantidade_lula_bolsonaro = len(data_collection['lula_and_bolsonaro_tt'])
    quantidade_no_candidato = len(data_collection['no_candidato'])

    # Dados para o gráfico
    candidatos = ['Lula', 'Bolsonaro', 'Lula e Bolsonaro', 'Nenhum Candidato']
    quantidades = [quantidade_lula, quantidade_bolsonaro, quantidade_lula_bolsonaro, quantidade_no_candidato]

    # Criar um dicionário de mapeamento de cores para cada categoria
    cores = {'Lula': 'red', 'Bolsonaro': 'blue', 'Lula e Bolsonaro': 'green', 'Nenhum Candidato': 'gray'}

    # Extrair as cores correspondentes a cada categoria
    cores_barras = [cores[candidato] for candidato in candidatos]

    # Criar um gráfico de barras
    plt.figure(figsize=(8, 6))
    plt.bar(candidatos, quantidades, color=cores_barras)
    plt.xlabel('Candidato')
    plt.ylabel('Quantidade de Tweets')
    plt.title('Quantidade de Tweets por Candidato (' + caminho_arquivo + ')')
    plt.savefig('graficos_resultantes/' + caminho_arquivo + '.png')


def leia_scores(data):
    result = []
    s = SentimentIntensityAnalyzer()
    for text in data:
        scores = s.polarity_scores(text)
        result.append({"scores": scores, "text": text})
    return result


def leia_scores_graph(data, path):
    neg = 0
    neu = 0
    pos = 0
    for data_composed in data:
        score = data_composed['scores']['compound']
        if score < -0.05:
            neg += 1
        elif -0.05 <= score <= 0.05:
            neu += 1
        else:
            pos += 1

    labels = ['Negativo', 'Neutro', 'Positivo']
    quantidades = [neg, neu, pos]
    cores = {'Negativo': 'red', 'Neutro': 'gray', 'Positivo': 'green'}
    cores_barras = [cores[label] for label in labels]
    # Criar um gráfico de barras
    plt.figure(figsize=(8, 6))
    plt.bar(labels, quantidades, color=cores_barras)
    plt.xlabel('Pontuação')
    plt.ylabel('Quantidade de Tweets')
    plt.title(path)
    # plt.title('Quantidade de Tweets por Candidato (Debate BAND 1 turno)')
    plt.savefig('graficos_resultantes/' + path + '.png')


def main():
    separate_data('archive/' + PATHS[0])
    # for path in PATHS:
    #     data = separate_data('archive/' + path)
    #     show_data_numbers(data, path)
    #     for candidate in data:
    #         data_results = leia_scores(data[candidate])
    #         leia_scores_graph(data_results, path + '_' + candidate)
    # print(data[0])
    # df = pd.DataFrame(data)
    # # Divida a coluna 'scores' em várias colunas
    # scores_df = df['scores'].apply(pd.Series)
    #
    # # Combine o DataFrame original com o DataFrame de scores
    # resultados_com_scores = pd.concat([df, scores_df], axis=1)
    #
    # # Exporte o DataFrame para um arquivo CSV
    # resultados_com_scores.to_csv("resultados_com_scores.csv", index=False)


if __name__ == '__main__':
    main()
