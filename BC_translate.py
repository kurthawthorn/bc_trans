import os
import streamlit as st
from googletrans import Translator

# Initialize the translator
translator = Translator()

# Function to translate text
def translate_text(text, lang):
    translation = translator.translate(text, src='en', dest=lang)
    return translation.text

# Streamlit UI
st.title("XLF Translator")

# Language selection
lang = st.selectbox("Select language:", ['Svensk', 'Norsk', 'Dansk'])
lang_code = {'Svensk': 'sv', 'Norsk': 'no', 'Dansk': 'da'}[lang]

# Input file selection
input_file = st.file_uploader("Select input XLF file", type="xlf")

# Output folder selection
output_folder = st.text_input("Select output folder path")

# Start translation button
if st.button("Start Translation"):
    if not input_file or not output_folder:
        st.error("Input file or output folder not selected. Exiting.")
    else:
        # Read the content of the file
        lines = input_file.read().decode('utf-8').splitlines()

        # Perform the translation on the filtered content
        translated_lines = []
        total_lines = len(lines)
        skip_next_line = False

        for i, line in enumerate(lines):
            if skip_next_line:
                skip_next_line = False
                continue

            if line.strip().endswith('</note>'):
                continue

            if '<source>' in line:
                source_text = line.strip().replace('<source>', '').replace('</source>', '')
                translated_text = translate_text(source_text, lang_code)
                translated_lines.append(f'          <source>{source_text}</source>\n')
                translated_lines.append(f'          <target>{translated_text}</target>\n')
                skip_next_line = True
            else:
                translated_lines.append(line)

            # Print progress every 100 lines
            if i % 100 == 0:
                st.write(f'Translated {i}/{total_lines} lines')

        # Write the translated content to a new file
        output_file_path = os.path.join(output_folder, f'BeCentral.{lang_code}.xlf')
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.writelines(translated_lines)

        st.success(f'Translation completed. Translated file saved to {output_file_path}')
