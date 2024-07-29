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
        lines = input_file.read().decode('utf-8').splitlines(keepends=True)

        # Perform the translation on the filtered content
        translated_lines = []
        total_lines = len(lines)
        translated_count = 0

        i = 0
        while i < total_lines:
            line = lines[i]

            # Check if the line contains a <source> tag
            if '<source>' in line:
                source_text = line.strip().replace('<source>', '').replace('</source>', '')
                translated_text = translate_text(source_text, lang_code)
                translated_lines.append(line)  # Keep the source line as it is
                i += 1  # Move to the next line which should be the <target> line
                
                # Check if the next line contains a <target> tag
                if i < total_lines and '<target>' in lines[i]:
                    # Preserve original indent
                    indent = ' ' * (len(lines[i]) - len(lines[i].lstrip()))
                    # Replace the content within the <target> tag with the translated text
                    translated_lines.append(f'{indent}<target>{translated_text}</target>\n')
                    translated_count += 1
                else:
                    # If no <target> line found (unexpected case), log an error or handle it
                    translated_lines.append(line)  # This is a fallback to ensure line isn't lost
            else:
                # For all other lines, keep them unchanged
                translated_lines.append(line)

            # Print progress every 100 lines
            if i % 100 == 0:
                st.write(f'Translated {i}/{total_lines} lines')
            
            i += 1  # Move to the next line

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
