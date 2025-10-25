from core.prepare import get_dataframe, DATA_DIR
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, models

def get_figure_amount():
    # Получение дата-сета
    df = get_dataframe()
    print(df.head())

    # Разделение дата-сета: 80% на обучение, 10% на валидацию, 10% на тест
    train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42)
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)
    print(f"Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")

    # Очень большие проблемы с памятью на моем железе - 128х128 край
    IMG_SIZE = (128, 128)

    # Генератор изображений с нормализацией
    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=10,      # случайные повороты до 10°
        width_shift_range=0.1,  # сдвиг по ширине
        height_shift_range=0.1, # сдвиг по высоте
        zoom_range=0.1,         # зум
        horizontal_flip=True    # случайное отражение по горизонтали
    )

    train_gen = datagen.flow_from_dataframe(
        dataframe=train_df,
        directory=DATA_DIR,
        x_col='filename',
        y_col='num_pieces',
        target_size=IMG_SIZE,
        class_mode='raw',
        batch_size=32,
        shuffle=True
    )

    val_gen = datagen.flow_from_dataframe(
        dataframe=val_df,
        directory=DATA_DIR,
        x_col='filename',
        y_col='num_pieces',
        target_size=IMG_SIZE,
        class_mode='raw',
        batch_size=32,
        shuffle=False
    )


    model = models.Sequential([
        # Поиск простых визуальных признаков (линии)
        layers.Conv2D(32, (3,3), activation='relu', input_shape=(128,128,3)),
        layers.MaxPooling2D((2,2)),

        # Поиск более сложных признаков (очертания фигур, клетки доски)
        layers.Conv2D(64, (3,3), activation='relu'),
        layers.MaxPooling2D((2,2)),

        # Поиск более высокоуровневых паттернов (комбинации фигур, группы клеток)
        layers.Conv2D(128, (3,3), activation='relu'),
        layers.MaxPooling2D((2,2)),

        # Получение вектора чисел из карты признаков
        layers.Flatten(),

        # 128 нейронов учатся выявлять связь между найденными признаками и целевым числом.
        layers.Dense(128, activation='relu'),

        # Выходной слой — один нейрон, т.к. регрессия.
        layers.Dense(1, activation='linear')
    ])

    model.summary()

    model.compile(
        optimizer='adam',
        loss='mse',
        metrics=['mae']  # средняя абсолютная ошибка
    )

    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=10
    )


    plt.plot(history.history['loss'], label='train_loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.xlabel('Эпоха')
    plt.ylabel('MSE')
    plt.legend()
    plt.title('Ошибка (MSE) на обучении и валидации')
    plt.show()

    val_gen.reset()
    x_batch, y_true = next(val_gen)
    y_pred = model.predict(x_batch)
    for i in range(5):
        print(f"Истинное значение: {y_true[i]:.0f}, Предсказание: {y_pred[i][0]:.2f}")

def get_figure_color_difference():
    # Получение дата-сета
    df = get_dataframe()
    df['more_white'] = (df['white_count'] > df['black_count']).astype(int)
    df['more_white_str'] = df['more_white'].apply(lambda x: 'white' if x == 1 else 'black')

    print(df.head())

    # Разделение дата-сета: 80% на обучение, 10% на валидацию, 10% на тест
    train_df, temp_df = train_test_split(df, test_size=0.2, random_state=42)
    val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)
    print(f"Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}")

    # Очень большие проблемы с памятью на моем железе - 128х128 край
    IMG_SIZE = (128, 128)

    # Генератор изображений с нормализацией
    datagen = ImageDataGenerator(
        rescale=1. / 255,
        rotation_range=10,  # случайные повороты до 10°
        width_shift_range=0.1,  # сдвиг по ширине
        height_shift_range=0.1,  # сдвиг по высоте
        zoom_range=0.1,  # лёгкое приближение/удаление
        horizontal_flip=True  # случайное отражение по горизонтали
    )

    # ==========================
    # ГЕНЕРАТОР ДЛЯ ОБУЧЕНИЯ
    # ==========================
    train_gen = datagen.flow_from_dataframe(
        dataframe=train_df,
        directory=DATA_DIR,
        x_col='filename',
        y_col='more_white_str',
        target_size=IMG_SIZE,
        class_mode='binary',  # 'raw' — значит, что выходом будет не класс, а число (регрессия)
        batch_size=32,  # сколько изображений подавать в модель за один шаг
        shuffle=True  # перемешивать данные перед каждой эпохой
    )

    # ==========================
    # ГЕНЕРАТОР ДЛЯ ВАЛИДАЦИИ
    # ==========================
    val_gen = datagen.flow_from_dataframe(
        dataframe=val_df,
        directory=DATA_DIR,
        x_col='filename',
        y_col='more_white_str',
        target_size=IMG_SIZE,
        class_mode='binary',  # 'raw' — значит, что выходом будет не класс, а число (регрессия)
        batch_size=32,  # сколько изображений подавать в модель за один шаг
        shuffle=False  # порядок должен сохраняться для сравнения результатов
    )

    # -------------------------------
    #  ПОСТРОЕНИЕ ПРОСТОЙ СВЁРТОЧНОЙ НЕЙРОСЕТИ (CNN)
    # -------------------------------
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),

        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),

        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(1, activation='sigmoid')  # бинарная классификация
    ])

    model.summary()

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=10
    )

    plt.plot(history.history['loss'], label='train_loss')
    plt.plot(history.history['val_loss'], label='val_loss')
    plt.xlabel('Эпоха')
    plt.ylabel('MSE')
    plt.legend()
    plt.title('Ошибка (MSE) на обучении и валидации')
    plt.show()

    val_gen.reset()
    x_batch, y_true = next(val_gen)
    y_pred = model.predict(x_batch)
    for i in range(5):
        label = "Белых больше" if y_pred[i][0] > 0.5 else "Чёрных больше/равно"
        print(f"Истинное: {y_true[i]}, Предсказание: {y_pred[i][0]:.2f} → {label}")

get_figure_amount()
# get_figure_color_difference()