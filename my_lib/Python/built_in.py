class list(list):
    """Обычный и привычный список, но с новыми функциями!"""
    def to_str(self, slicer: str = ' ') -> str:
        """Данная функция позволяет превратить список (list) в строку (str)."""
        return str(self).replace('[', '').replace(']', '').replace(', ', slicer).replace("'", '')
class str(str):
    """Обычная и привычная строка, но с новыми функциями!
    И да, я не блещу оригинальностью надписей..."""
    def remove(self, string: str):
        '''Данный метод удаляет подстроку из родительской строки.'''
        return str(self.replace(string, ''))