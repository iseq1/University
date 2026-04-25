from plugins import TextClassifier, TextPreprocessor, DatasetPreprocessor, CBOW

if __name__ == '__name__':

    # 1

    classifier = TextClassifier.from_dataset()
    classifier.train()
    classifier.evaluate()

    # 2
    ds = TextPreprocessor.get_dataset()
    tokenized_texts = DatasetPreprocessor.get_tokens(dataset=ds)
    corpus = tokenized_texts[:10000]

    # Создание модели
    cbow_model = CBOW(corpus=corpus, window_size=2, embedding_dim=100, min_count=5)

    # Обучение
    cbow_model.train(epochs=5, lr=0.05, limit_pairs=100000)

    # Анализ векторов
    print("\n--- Similar words ---")
    print("game:", cbow_model.most_similar("game"))
    print("good:", cbow_model.most_similar("good"))

    print("\n--- Analogies ---")
    print("good - bad + terrible:", cbow_model.analogy("good", "bad", "terrible"))
    print("fun - boring + interesting:", cbow_model.analogy("fun", "boring", "interesting"))
    print("easy - hard + difficult:", cbow_model.analogy("easy", "hard", "difficult"))
    print("fast - slow + quick:", cbow_model.analogy("fast", "slow", "quick"))
    print("like - hate + love:", cbow_model.analogy("like", "hate", "love"))