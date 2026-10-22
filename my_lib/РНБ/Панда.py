try:
    import pandas as pd

    class Таблица (pd.DataFrame):
        def В_Excel (self, name: str):
            self.to_excel(name, index=False)
except: pass