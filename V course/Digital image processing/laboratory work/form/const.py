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
    'get_smooth_corrected': "✅ Сглаженное изображение успешно получено! ✅",
    'get_smooth_failed': "⚠️ Ошибка при получении сглаженного изображения! ⚠️",
}

# Кнопки и их обработчики для вкладки "Изображение"
IMAGE_COMBO_MAP = {
    'Изображение': None,

    'Загрузить': {
        'type': 'btn',
        'action': lambda self: self.load_image(),
        'menu_params': None,
    },

    'Сохранить': {
        'type': 'btn',
        'action': lambda self: self.save_image(),
        'menu_params': None,
    },

    'Конвертировать в серый': {
        'type': 'btn',
        'action': lambda self: self.apply_grayscale(),
        'menu_params': None,
    },

    'Конвертировать в байты': {
        'type': 'btn',
        'action': lambda self: self.convert_to_bytes(),
        'menu_params': None,
    },

    'Конвертировать из байтов': {
        'type': 'btn',
        'action': lambda self: self.convert_from_bytes(),
        'menu_params': None,
    },

    'Статистика изображения': {
        'type': 'btn',
        'action': lambda self: self.compute_stats(self.current_array, border_only=False),
        'menu_params': None,
    },

    'Статистика границы изоб.': {
        'type': 'btn',
        'action': lambda self: self.compute_stats(self.current_array, border_only=True),
        'menu_params': None,
    },

    'Гистограмма изображения': {
        'type': 'btn',
        'action': lambda self: self.compute_hist(self.current_array, border_only=False),
        'menu_params': None,
    },


    'Гистограмма границы изоб.': {
        'type': 'btn',
        'action': lambda self: self.compute_hist(self.current_array, border_only=True),
        'menu_params': None,
    },


    'Линейное контрастирование': {
        'type': 'btn',
        'action': lambda self: self.compute_contrast(self.current_array),
        'menu_params': None,
    },

    'Сглаживание амплитуд': {
        'type': 'menu',
        'action': None,
        'menu_params': {
            'label': 'Выберите радиус',
            'items': [
                {'label': 'R = 1', 'action': lambda self: self.compute_smooth(self.current_array, 1)},
                {'label': 'R = 3', 'action': lambda self: self.compute_smooth(self.current_array, 3)},
                {'label': 'R = 5', 'action': lambda self: self.compute_smooth(self.current_array, 5)},
                {'label': 'R = 7', 'action': lambda self: self.compute_smooth(self.current_array, 7)},
            ],
        },
    },

}

# Кнопки и их обработчики для вкладки "ROI"
ROI_COMBO_MAP = {
    "Работа с ROI": None ,

    'Статистика ROI': {
        'type': 'btn',
        'action': lambda self: self.compute_stats(self.current_roi_array, border_only=False),
        'menu_params': None,
    },

    'Статистика границы ROI': {
        'type': 'btn',
        'action': lambda self: self.compute_stats(self.current_roi_array, border_only=True),
        'menu_params': None,
    },

    'Гистограмма ROI': {
        'type': 'btn',
        'action': lambda self: self.compute_hist(self.current_roi_array, border_only=False),
        'menu_params': None,
    },

    'Гистограмма границы ROI': {
        'type': 'btn',
        'action': lambda self: self.compute_hist(self.current_roi_array, border_only=True),
        'menu_params': None,
    },

    'Линейное контрастирование': {
        'type': 'btn',
        'action': lambda self: self.compute_contrast(self.current_roi_array),
        'menu_params': None,
    },

    'Сглаживание амплитуд': {
        'type': 'menu',
        'action': None,
        'menu_params': {
            'label': 'Выберите радиус',
            'items': [
                {'label': 'R = 1', 'action': lambda self: self.compute_smooth(self.current_roi_array, 1)},
                {'label': 'R = 3', 'action': lambda self: self.compute_smooth(self.current_roi_array, 3)},
                {'label': 'R = 5', 'action': lambda self: self.compute_smooth(self.current_roi_array, 5)},
                {'label': 'R = 7', 'action': lambda self: self.compute_smooth(self.current_roi_array, 7)},
            ],
        },
    },

    "Отменить ROI": {
        'type': 'btn',
        'action': lambda self: self.clear_roi(),
        'menu_params': None,
    },

}

# Обработчики для форматирования информации
FORMAT_DATA_MAP = {
    'stat': lambda self, stats: self.format_stat_img(stats),
    'hist': lambda self, hist: self.format_hist_img(hist),
    'contrast': lambda self, contrast: self.format_contrast_img(contrast),
    'smooth': lambda self, smooth: self.format_smooth_img(smooth),
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
    "compute_smooth": {
        "success": "Сглаживание амплитуд изображения выполнено.",
        "warning": "Не удалось выполнить сглаживание амплитуд.",
        "error": "Ошибка при сглаживании амплитуд изображения: "
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

BUTTON_STYLE = """
    QPushButton {
        border: 1px solid #aaa;
        border-radius: 4px;
        padding: 4px 8px;
        background-color: #f0f0f0;
        text-align: left;
    }
    QPushButton::menu-indicator {
        image: none;
    }
    QPushButton:hover {
        background-color: #e0e0e0;
    }
"""