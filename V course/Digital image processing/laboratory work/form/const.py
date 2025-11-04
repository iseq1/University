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
    'get_rotate_corrected': "✅ Поворот изображение успешно выполнен! ✅",
    'get_rotate_failed': "⚠️ Ошибка при повороте изображения! ⚠️",
    'get_scale_corrected': "✅ Масштабирование изображение успешно выполнено! ✅",
    'get_scale_failed': "⚠️ Ошибка при масштабировании изображения! ⚠️",
    'get_amplitude_corrected': "✅ Изменение амплитуды пикселей успешно выполнено! ✅",
    'get_amplitude_failed': "⚠️ Ошибка при изменении амплитуды пикселей! ⚠️",
    'get_piecewise_corrected': "✅ Построение карты изображения успешно выполнено! ✅",
    'get_piecewise_failed': "⚠️ Ошибка при построении карты изображения! ⚠️",
    'get_mia_corrected': "✅ Построение изображения с взаимно независимыми амплитудами успешно выполнено! ✅",
    'get_mia_failed': "⚠️ Ошибка при построении изображения с взаимно независимыми амплитудами! ⚠️",
}

#
GENERAL_COMBO_MAP = {
    'Общее': None,

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

    'Поворот вправо': {
        'type': 'btn',
        'action': lambda self: self.compute_rotate(self.current_array, angle=90),
        'menu_params': None,
    },

    'Поворот влево': {
        'type': 'btn',
        'action': lambda self: self.compute_rotate(self.current_array, angle=-90),
        'menu_params': None,
    },

    'Масштабирование': {
        'type': 'menu',
        'action': None,
        'menu_params': {
            'label': 'Выберите метод и масштаб',
            'items': [
                {'label': 'x2.0 - Выборкой', 'action': lambda self: self.compute_scale(self.current_array, 2.0, 2.0, 'nearest')},
                {'label': 'x2.0 - Б.И.', 'action': lambda self: self.compute_scale(self.current_array, 2.0, 2.0, 'bilinear')},
                {'label': 'x0.5 - Выборкой', 'action': lambda self: self.compute_scale(self.current_array, 0.5, 0.5, 'nearest')},
                {'label': 'x0.5 - Б.И.', 'action': lambda self: self.compute_scale(self.current_array, 0.5, 0.5, 'bilinear')},
            ],
        },
    },

    'Изменить амплитуды': {
        'type': 'btn',
        'action': lambda self: self.compute_amplitude(self.current_array),
        'menu_params': None,
    },

    'Построение изображения': {
        'type': 'menu',
        'action': None,
        'menu_params': {
            'label': 'Выберите метод',
            'items': [
                {'label': 'Взаимно независимые амплитуды',
                 'action': lambda self: self.compute_mia(mode='mia')},
            ],
        },
    },

    'Отменить': {
        'type': 'btn',
        'action': lambda self: self.undo(),
        'menu_params': None,
    },


}

# Кнопки и их обработчики для вкладки "Изображение"
IMAGE_COMBO_MAP = {
    'Изображение': None,

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

    'Построение карты': {
        'type': 'menu',
        'action': None,
        'menu_params': {
            'label': 'Выберите разиер блока',
            'items': [
                {'label': 'Блок 2x2',
                 'action': lambda self: self.compute_piecewise(self.current_array, 2)},
                {'label': 'Блок 4x4',
                 'action': lambda self: self.compute_piecewise(self.current_array, 4)},
                {'label': 'Блок 8x8',
                 'action': lambda self: self.compute_piecewise(self.current_array, 8)},
                {'label': 'Блок 16x16',
                 'action': lambda self: self.compute_piecewise(self.current_array, 16)},
                {'label': 'Блок 32x32',
                 'action': lambda self: self.compute_piecewise(self.current_array, 32)},
                {'label': 'Блок 64x64',
                 'action': lambda self: self.compute_piecewise(self.current_array, 64)},
                {'label': 'Блок 128x128',
                 'action': lambda self: self.compute_piecewise(self.current_array, 128)},
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

    'Построение карты': {
        'type': 'menu',
        'action': None,
        'menu_params': {
            'label': 'Выберите разиер блока',
            'items': [
                {'label': 'Блок 2x2',
                 'action': lambda self: self.compute_piecewise(self.current_roi_array, 2)},
                {'label': 'Блок 4x4',
                 'action': lambda self: self.compute_piecewise(self.current_roi_array, 4)},
                {'label': 'Блок 8x8',
                 'action': lambda self: self.compute_piecewise(self.current_roi_array, 8)},
                {'label': 'Блок 16x16',
                 'action': lambda self: self.compute_piecewise(self.current_roi_array, 16)},
                {'label': 'Блок 32x32',
                 'action': lambda self: self.compute_piecewise(self.current_roi_array, 32)},
                {'label': 'Блок 64x64',
                 'action': lambda self: self.compute_piecewise(self.current_roi_array, 64)},
                {'label': 'Блок 128x128',
                 'action': lambda self: self.compute_piecewise(self.current_roi_array, 128)},
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
    'piecewise': lambda self, piecewise: self.format_piecewise_img(piecewise),
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
    "compute_rotate": {
        "success": "Поворот изображения выполнен.",
        "warning": "Не удалось выполнить поворот изображения.",
        "error": "Ошибка при повороте изображения: "
    },
    "compute_scale": {
        "success": "Масштабирование изображения выполнено.",
        "warning": "Не удалось выполнить масштабирование изображения.",
        "error": "Ошибка при масштабировании изображения: "
    },
    "compute_amplitude": {
        "success": "Изменение амплитуды пикселей изображения выполнено.",
        "warning": "Не удалось изменить амплитуды пикселей изображения.",
        "error": "Ошибка при изменении амплитуды пикселей изображения: "
    },
    "compute_piecewise": {
        "success": "Построение изображения с кусочно-постоянными амплитудами выполнено.",
        "warning": "Не удалось построить изображение с кусочно-постоянными амплитудами.",
        "error": "Ошибка при построении изображения с кусочно-постоянными амплитудами: "
    },
    "compute_mia": {
        "success": "Построение изображения с взаимно независимыми амплитудами выполнено.",
        "warning": "Не удалось построить изображение с взаимно независимыми амплитудами.",
        "error": "Ошибка при построении изображения с взаимно независимыми амплитудами: "
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

CREATE_IMAGE_MODE = {
    "mia": lambda self, layout: self.inti_mia_img_ui(layout)
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