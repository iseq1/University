import cv2
from sklearn.model_selection import train_test_split

from src.plugins.classification.custom_rule_based import RuleClassifier
from src.plugins.classification.ml import MLClassifier
from src.plugins.ocr.easy import EasyOCRWrapper
from src.plugins.ocr.rapid import RapidOCRWrapper
from src.plugins.structurer.temp import SimpleStructurer
from src.plugins.pipeline.pipeline import Pipeline
from src.utils.data_load import load_dataset
from src.utils.image_processor import Preprocessor


def run_experiment():
    # 1. обучаем ML на текстовом датасете
    texts, labels = load_dataset("data/new_dataset.csv")

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.3, random_state=42
    )

    ml = MLClassifier()
    ml.train(X_train, y_train)

    structurer = SimpleStructurer()
    preprocessor = Preprocessor()

    # 2. OCR модели
    ocr_models = {
        "Rapid": RapidOCRWrapper(),
        "EasyOCR": EasyOCRWrapper(),
    }

    # 3. тестовые изображения
    test_images = []

    for type_ in ['food', 'transport', 'shopping']:
        for j in range(1,6):
            test_images.append((f"data/{type_}_sample/{type_}_{j}.jpg", f"{type_}"))

    print(test_images)

    results = {
        "RAW": {},
        "PREPROCESSING": {}
    }

    for mode in ["RAW", "PREPROCESSING"]:
        print(f"\n\n===== MODE: {mode} =====")

        for ocr_name, ocr in ocr_models.items():
            correct = 0

            print(f"\n=== {ocr_name} ({mode}) ===")

            for path, true_label in test_images:
                image = cv2.imread(path)

                # 🔥 KEY CHANGE HERE
                if mode == "PREPROCESSING":
                    image = preprocessor.process(image)

                text = ocr.extract_text(image)
                doc = structurer.structure(text)
                pred = ml.classify(doc)

                print(f"\nImage: {path}")
                print(f"Predicted: {pred} | True: {true_label}")

                if pred == true_label:
                    correct += 1

            acc = correct / len(test_images)

            if ocr_name not in results[mode]:
                results[mode][ocr_name] = acc

            print(f"\n{ocr_name} {mode} accuracy: {acc}")

    return results


def main():
    # 1. Загружаем датасет
    texts, labels = load_dataset("data/new_dataset.csv")

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.3, random_state=42
    )

    # 2. Обучаем ML классификатор
    ml_classifier = MLClassifier()
    ml_classifier.train(X_train, y_train)

    structurer = SimpleStructurer()
    preds = []

    for text in X_test:
        document = structurer.structure(text)  # важно!
        pred = ml_classifier.classify(document)
        preds.append(pred)

    accuracy = sum([1 for p, t in zip(preds, y_test) if p == t]) / len(y_test)

    print("ML accuracy:", accuracy)

    # 3. Инициализация компонентов
    ocr = EasyOCRWrapper()
    structurer = SimpleStructurer()
    rule_classifier = RuleClassifier()

    # 4. Создаем pipeline для двух вариантов
    pipeline_rule = Pipeline(ocr, structurer, rule_classifier)
    pipeline_ml = Pipeline(ocr, structurer, ml_classifier)

    # 5. Тестовое изображение
    image = cv2.imread("data/food_sample/food_1.jpg")

    # 6. Запуск
    result_rule = pipeline_rule.run(image)
    result_ml = pipeline_ml.run(image)

    print("=== Rule-based ===")
    print(result_rule)

    print("\n=== ML ===")
    print(result_ml)




if __name__ == "__main__":
    main()

    results = run_experiment()

    print("\n=== FINAL RESULTS ===")

    for mode, res in results.items():
        print(f"\n--- {mode} ---")
        for k, v in res.items():
            print(f"{k}: {v}")