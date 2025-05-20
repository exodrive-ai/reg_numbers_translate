import streamlit as st
import pandas as pd
import io
import base64

st.set_page_config(page_title="Конвертер госномеров", page_icon="🚗")

st.write("""
# Приложение для замены кириллицы на латиницу в гос. номерах авто.
\nФормат файла - одна колонка без заголовков с госномерами на кириллице в верхнем регистре.
""")

def change_letters(reg_number):
    """ Поменять кириллицу в гос. номере авто на латиницу """
    if not isinstance(reg_number, str):
        reg_number = str(reg_number)
        
    replace_dict = {'У': 'Y', 'К': 'K', 'Е': 'E', 'Н': 'H', 'Х': 'X', 'В': 'B',
                    'А': 'A', 'Р': 'P', 'О': 'O', 'С': 'C', 'М': 'M', 'Т': 'T'}
    return ''.join(replace_dict.get(char, char) for char in reg_number)

# Add a file uploader widget
uploaded_file = st.file_uploader(
    "Загрузите Excel файл с госномерами", 
    type=["xlsx"],
    key="file_uploader_1",
    help="Файл должен содержать одну колонку с госномерами на кириллице в верхнем регистре"
)

# Добавляем альтернативный метод загрузки данных
st.write("### Или введите номера вручную")
text_input = st.text_area(
    "Введите госномера (один номер на строку)",
    height=200,
    key="manual_input"
)

if uploaded_file is not None:
    try:
        # Display file details for debugging
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size / 1024:.2f} KB",
            "File type": uploaded_file.type
        }
        st.write("### Детали файла:")
        for key, value in file_details.items():
            st.write(f"- {key}: {value}")
        
        # Read excel file with minimal options
        df = pd.read_excel(uploaded_file, header=None, engine='openpyxl')
        
        # Convert first column to string and apply transformation
        df[0] = df[0].astype(str).apply(change_letters)
        
        # Generate download link
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, header=False)
        
        output.seek(0)
        excel_data = output.read()
        
        # Create a download link using HTML
        b64 = base64.b64encode(excel_data).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="converted_numbers.xlsx">📥 Скачать конвертированный файл</a>'
        st.markdown(href, unsafe_allow_html=True)
        
        # Also show the first few rows
        st.write("### Предпросмотр результатов:")
        st.dataframe(df.head(10))
        
    except Exception as e:
        st.error(f"Ошибка при обработке файла: {str(e)}")
        st.exception(e)
        
# Process manually entered text if any
elif text_input:
    try:
        # Split input into lines and process
        lines = text_input.strip().split('\n')
        processed_lines = [change_letters(line) for line in lines]
        
        # Create dataframe
        df = pd.DataFrame(processed_lines)
        
        # Display results
        st.write("### Результаты конвертации:")
        results_df = pd.DataFrame({'Оригинал': lines, 'Конвертировано': processed_lines})
        st.dataframe(results_df)
        
        # Generate download for manual input
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, header=False)
        
        output.seek(0)
        excel_data = output.read()
        
        # Create download link
        b64 = base64.b64encode(excel_data).decode()
        href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="manual_converted.xlsx">📥 Скачать конвертированный файл</a>'
        st.markdown(href, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Ошибка при обработке введенного текста: {str(e)}")
        st.exception(e)

# Add instructions
st.write("""
### Инструкции:
1. Загрузите файл Excel с госномерами ИЛИ введите номера вручную
2. Приложение автоматически заменит кириллические символы на латинские
3. Скачайте результат, нажав на ссылку
""")

# Add debugging information
st.write("### Системная информация:")
st.write(f"- Версия Streamlit: {st.__version__}")
st.write(f"- Версия Pandas: {pd.__version__}")
