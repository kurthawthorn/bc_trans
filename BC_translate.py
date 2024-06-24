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
st.write("Select the target language for translation:")
lang = st.selectbox("Language:", ['Svensk', 'Norsk', 'Dansk'])
lang_code = {'Svensk': 'sv', 'Norsk': 'no', 'Dansk': 'da'}[lang]

# Input file selection
input_file = st.file_uploader("Select input XLF file", type="xlf")

# Start translation button
if st.button("Start Translation"):
    if not input_file:
        st.error("No input file selected. Exiting.")
    else:
        # Read the content of the file
        lines = input_file.read().decode('utf-8').splitlines()

        # Perform the translation on the filtered content
        translated_lines = []
        total_lines = len(lines)
        skip_next_line = False
        translated_count = 0

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
                translated_count += 1
                skip_next_line = True
            else:
                translated_lines.append(line)

            # Print progress every 100 lines
            if i % 100 == 0:
                st.write(f'Translated {i}/{total_lines} lines')

        # Write the translated content to a new file
        output_file_name = f'BeCentral.{lang_code}.xlf'
        output_file_path = os.path.join("/tmp", output_file_name)
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.writelines(translated_lines)

        st.success(f"Translation completed. Translated {translated_count} out of {total_lines} lines.")
        
        with open(output_file_path, 'rb') as file:
            btn = st.download_button(
                label="Download Translated XLF File",
                data=file,
                file_name=output_file_name,
                mime='application/octet-stream'
            )
