# Лабораторная работа №2 — Реализация модели seq2seq

## О проекте

В рамках лабораторной работы реализована архитектура Seq2Seq для задачи классификации жанров видеоигр по текстовому описанию.

Модель построена полностью на PyTorch с использованием:
* кастомной реализации LSTM
* кастомной реализации Attention
* Embedding слоя
* Encoder-Decoder архитектуры

### Жанровая классификация на основе Seq2Seq 

- Корпус: синтетический датасет описаний игр в стиле Steam  
- Архитектура: Seq2Seq (Encoder–Decoder)  
- Encoder: кастомная реализация LSTM  
- Decoder: кастомная реализация LSTM + Attention  
- Embeddings и FC-слой: `PyTorch nn.Embedding` и `nn.Linear`  
- Attention: реализован вручную (dot-product attention)  
- Framework: PyTorch  
- Задача: генерация жанра игры по текстовому описанию  

## Пример

Вход:

```text
fast paced competitive game with online multiplayer battles
```

Выход:
```text
first person shooter
```
