import matplotlib.pyplot as plt
import pandas as pd
import json
import os

DATA_DIR = 'D:\\project under development\\University\\V course\\Neural networks\\II lab\\dataset'

def get_dataframe():
    """Получение датафрейма"""
    json_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]

    value_map = {'pawn':1, 'knight':3, 'bishop':3, 'rook':5, 'queen':9, 'king':0}

    extended_records = []

    for jf in json_files:
        json_path = os.path.join(DATA_DIR, jf)
        with open(json_path, 'r') as f:
            data = json.load(f)
        config = data.get('config', {})
        img_name = jf.replace('.json', '.jpg')
        if not os.path.exists(os.path.join(DATA_DIR, img_name)):
            continue

        white_count = 0
        black_count = 0
        white_value = 0
        black_value = 0

        for cell, piece in config.items():
            if '_' not in piece:
                continue
            name, color = piece.split('_')
            val = value_map.get(name.lower(), 0)
            if color == 'w':
                white_count += 1
                white_value += val
            elif color == 'b':
                black_count += 1
                black_value += val

        extended_records.append({
            'filename': img_name,
            'num_pieces': len(config),
            'white_count': white_count,
            'black_count': black_count,
            'white_value': white_value,
            'black_value': black_value
        })

    df_ext = pd.DataFrame(extended_records)
    # print(df_ext.head())
    plot_figures_distribution(df_ext)
    return df_ext


def plot_figures_distribution(df):
    """Визуализация распределения кол-ва фигур"""
    fig, ax = plt.subplots()
    plt.hist(df['num_pieces'], bins=20, edgecolor='black')
    plt.xlabel('Количество фигур на доске')
    plt.ylabel('Количество примеров')
    plt.title('Распределение количества фигур')
    plt.show()

