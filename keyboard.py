from telebot import types

ADMINS = [407764903, 885172912]


class NewKeyboard(types.ReplyKeyboardMarkup):
    def __init__(self, *args,  row_width=1):
        super().__init__(
            row_width=row_width, resize_keyboard=True)
        for button in args:
            if isinstance(button, list):
                self.add(*[types.KeyboardButton(but) for but in button])
            else:
                self.add(types.KeyboardButton(button))


# Основная клавиатура
MainKeyboard = NewKeyboard('Новый лист', 'Продолжить лист')
