import streamlit as st
from pandas import read_excel, DataFrame, ExcelWriter
from io import BytesIO

st.write("""
# Приложение для замены кириллицы на латиницу в гос. номерах авто.
\nФормат файла - одна колонка без заголовков с госномерами на кириллице в верхнем регистре.
""")


def change_letters(reg_number: str) -> str:
    """ Поменять кириллицу в гос. номере авто на латиницу """
    replace_dict = {'У': 'Y', 'К': 'K', 'Е': 'E', 'Н': 'H', 'Х': 'X', 'В': 'B',
                    'А': 'A', 'Р': 'P', 'О': 'O', 'С': 'C', 'М': 'M', 'Т': 'T'}
    return ''.join(replace_dict.get(char, char) for char in reg_number)


def to_excel(df: DataFrame) -> bytes:
    """ Сохранить датафрейм, как бинарник экселя """
    output = BytesIO()
    with ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, header=False, index=False, sheet_name='Sheet1')
    return output.getvalue()


uploaded_file = st.file_uploader(label="Загрузите сюда ваш файл с расширением xlsx", type=['xlsx'])

if uploaded_file is not None:
    data = BytesIO(uploaded_file.read())
    df = read_excel(io=data, header=None, converters={0: change_letters})
    df_xlsx = to_excel(df)
    st.download_button(label='📥 Скачать результат', data=df_xlsx, file_name='reg_numbers.xlsx')
