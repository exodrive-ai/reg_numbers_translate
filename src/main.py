import streamlit as st
from pandas import read_excel, DataFrame, ExcelWriter
from io import BytesIO

st.write("""
# Приложение для замены кириллицы на латиницу в гос. номерах авто.
\nФормат файла - одна колонка без заголовков с госномерами на кириллице в верхнем регистре.
""")

def change_letters(reg_number: str) -> str:
    """ Поменять кириллицу в гос. номере авто на латиницу """
    # Check if input is a string
    if not isinstance(reg_number, str):
        return str(reg_number)  # Convert to string if not already
        
    replace_dict = {'У': 'Y', 'К': 'K', 'Е': 'E', 'Н': 'H', 'Х': 'X', 'В': 'B',
                    'А': 'A', 'Р': 'P', 'О': 'O', 'С': 'C', 'М': 'M', 'Т': 'T'}
    return ''.join(replace_dict.get(char, char) for char in reg_number)

def to_excel(df: DataFrame) -> bytes:
    """ Сохранить датафрейм, как бинарник экселя """
    output = BytesIO()
    try:
        with ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, header=False, index=False, sheet_name='Sheet1')
        output.seek(0)  # Reset pointer to beginning of file
        return output.getvalue()
    except Exception as e:
        st.error(f"Ошибка при создании Excel файла: {e}")
        return None

uploaded_file = st.file_uploader(label="Загрузите сюда ваш файл с расширением xlsx", type=['xlsx'])

if uploaded_file is not None:
    try:
        # Read the uploaded file directly
        df = read_excel(uploaded_file, header=None)
        
        # Validate that the dataframe has at least one column
        if df.shape[1] < 1:
            st.error("Файл должен содержать хотя бы одну колонку с данными.")
        else:
            # Apply the conversion function to the first column
            df[0] = df[0].apply(change_letters)
            
            # Convert to Excel
            df_xlsx = to_excel(df)
            
            if df_xlsx:
                st.download_button(
                    label='📥 Скачать результат',
                    data=df_xlsx,
                    file_name='reg_numbers.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
    except Exception as e:
        st.error(f"Произошла ошибка при обработке файла: {e}")
