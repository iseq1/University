"""
Константы, мапперы и прочее
"""

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
}

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
}

ROI_COMBO_MAP = {
    "Работа с ROI": None ,
    "Статистика ROI": lambda self: self.compute_stats(self.current_roi_array, border_only=False),
    "Статистика границы ROI": lambda self: self.compute_stats(self.current_roi_array, border_only=True),
    "Гистограмма ROI": lambda self: self.compute_hist(self.current_roi_array, border_only=False),
    "Гистограмма границы ROI": lambda self: self.compute_hist(self.current_roi_array, border_only=True),
    "Отменить ROI": lambda self: self.clear_roi(),
}

FORMAT_DATA_MAP = {
    'stat': lambda self, stats: self.format_stat_img(stats),
    'hist': lambda self, hist: self.format_hist_img(hist),
}