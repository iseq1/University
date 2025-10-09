"""
Константы, мапперы и прочее
"""

# Сообщения для статусбара
STATUS_BAR_MSG = {
    'no_image': "❌ Нет изображения! ❌",
    'no_roi': "❌ Не выбран ROI! ❌",
    'undo_corrected': "✅ Последнее действие успешно отменено! ✅",
    'undo_failed': "⚠️ Нет истории для \"Отмены\" ⚠️",
    'load_corrected': "✅ Изображение успешно загружено в форму! ✅",
    'load_failed': "⚠️ Ошибка при загрузке изображения! ⚠️",
    'save_corrected': "✅ Изображение успешно сохранено на диске! ✅",
    'save_failed': "⚠️ Ошибка при сохранении изображения! ⚠️",
    'grayscale_corrected': "✅ Изображение успешно конвертировано в градациях серого! ✅",
    'grayscale_failed': "⚠️ Ошибка при применении градации серого! ⚠️",
    'convert_tb_failed': "⚠️ Ошибка при конвертации в массив байтов ⚠️",
    'convert_fb_failed': "⚠️ Ошибка при конвертации из массива байтов ⚠️",
    'no_update_display': "⚠️ Текущее состояние — массив байтов ⚠️",
    'update_display_failed': "⚠️ Ошибка при обновлении дисплея ⚠️",
    'clear_roi_corrected': "✅ ROI успешно отменена! ✅",
    'set_roi_corrected': "✅ ROI успешно установлена! ✅",
    'get_stat_corrected': "✅ Статистика успешно получена! ✅",
    'get_stat_failed': "⚠️ Ошибка при получении статистики! ⚠️",
    'get_hist_corrected': "✅ Гистограмма успешно получена! ✅",
    'get_hist_failed': "⚠️ Ошибка при получении гистограммы! ⚠️",
    'get_contrast_corrected': "✅ Контрастное изображение успешно получено! ✅",
    'get_contrast_failed': "⚠️ Ошибка при получении контрастного изображения! ⚠️",
}

# Кнопки и их обработчики для вкладки "Изображение"
IMAGE_COMBO_MAP = {
    'Изображение': None,
    'Загрузить': lambda self: self.load_image(),
    'Сохранить': lambda self: self.save_image(),
    'Конвертировать в серый': lambda self: self.apply_grayscale(),
    'Конвертировать в байты': lambda self: self.convert_to_bytes(),
    'Конвертировать из байтов': lambda self: self.convert_from_bytes(),
    'Статистика изображения': lambda self: self.compute_stats(self.current_array, border_only=False),
    'Статистика границы изоб.': lambda self: self.compute_stats(self.current_array, border_only=True),
    'Гистограмма изображения': lambda self: self.compute_hist(self.current_array, border_only=False),
    'Гистограмма границы изоб.': lambda self: self.compute_hist(self.current_array, border_only=True),
    'Линейное контрастирование': lambda self: self.compute_contrast(self.current_array),
}

# Кнопки и их обработчики для вкладки "ROI"
ROI_COMBO_MAP = {
    "Работа с ROI": None ,
    "Статистика ROI": lambda self: self.compute_stats(self.current_roi_array, border_only=False),
    "Статистика границы ROI": lambda self: self.compute_stats(self.current_roi_array, border_only=True),
    "Гистограмма ROI": lambda self: self.compute_hist(self.current_roi_array, border_only=False),
    "Гистограмма границы ROI": lambda self: self.compute_hist(self.current_roi_array, border_only=True),
    "Линейное контрастирование": lambda self: self.compute_contrast(self.current_roi_array),
    "Отменить ROI": lambda self: self.clear_roi(),
}

# Обработчики для форматирования информации
FORMAT_DATA_MAP = {
    'stat': lambda self, stats: self.format_stat_img(stats),
    'hist': lambda self, hist: self.format_hist_img(hist),
    'contrast': lambda self, contrast: self.format_contrast_img(contrast),
}

# Сообщения для логера
LOGGER_MSG_MAP = {
    "load_image": {
        "success": "Изображение успешно загружено.",
        "error": "Ошибка при загрузке изображения: "
    },
    "save_image": {
        "success": "Изображение сохранено.",
        "error": "Ошибка при сохранении изображения: "
    },
    "apply_grayscale": {
        "success": "Изображение конвертировано в градациях серого.",
        "error": "Ошибка при конвертировании в градациях серого: "
    },
    "convert_to_bytes": {
        "success": "Изображение конвертировано в массив байтов.",
        "warning": "Не удалось конвертировать в массив байтов.",
        "error": "Ошибка при конвертации в массив байтов: "
    },
    "convert_from_bytes": {
        "success": "Изображение конвертировано из массива байтов.",
        "warning": "Не удалось конвертировать из массива байтов.",
        "error": "Ошибка при конвертации из массива байтов: "
    },
    "compute_stats": {
        "success": "Статистика изображения рассчитана.\n",
        "warning": "Не удалось рассчитать статистику изображения.",
        "error": "Ошибка при расчете статистики: "
    },
    "compute_hist": {
        "success": "Гистограмма изображения рассчитана.",
        "warning": "Не удалось рассчитать гистограмму изображения.",
        "error": "Ошибка при расчете гистограммы: "
    },
    "compute_contrast": {
        "success": "Линейное контрастирование изображения рассчитано.",
        "warning": "Не удалось рассчитать линейное контрастирование.",
        "error": "Ошибка при расчете линейного контрастирования: "
    },
    "update_display": {
        "error": "Ошибка при обновлении дисплея: "
    },
    "format_data": {
        "error": "Ошибка при форматировании данных для визуализации: "
    },
    "_img_action_selected": {
        "error": "Ошибка при выборе действия над изображением: "
    },
    "_roi_action_selected": {
        "error": "Ошибка при выборе действия над ROI: "
    },
    "on_mouse_move": {
        "error": "Ошибка при отслеживании координат курсора: "
    },
    "handle_roi_selection": {
        "error": "Ошибка выборе ROI: "
    },
    "clear_roi": {
        "error": "Ошибка при очистке ROI: "
    },
    "push_history": {
        "error": "Ошибка при добавлении в буфер в форме: "
    },
    "undo": {
        "error": "Ошибка при отмене последнего действия из буфера: "
    },
}