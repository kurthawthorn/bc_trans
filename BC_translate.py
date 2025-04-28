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
        # Save original filename
        original_filename = input_file.name

        # Read the content of the file
        lines = input_file.read().decode('utf-8').splitlines(keepends=True)

        translated_lines = []
        total_lines = len(lines)
        translated_count = 0

        i = 0
        while i < total_lines:
            line = lines[i]

            # Check if the line contains a <source> tag
            if '<source>' in line:
                source_text = line.strip().replace('<source>', '').replace('</source>', '')
                translated_lines.append(line)  # Keep the source line
                i += 1  # Move to the next line which should be the <target> line

                if i < total_lines and '<target>' in lines[i]:
                    target_line = lines[i]

                    if '[NAB: NOT TRANSLATED]' in target_line:
                        # Only translate if target says "[NAB: NOT TRANSLATED]"
                        indent = ' ' * (len(target_line) - len(target_line.lstrip()))
                        translated_text = translate_text(source_text, lang_code)
                        translated_lines.append(f'{indent}<target>{translated_text}</target>\n')
                        translated_count += 1
                    else:
                        # Keep the existing translation
                        translated_lines.append(target_line)
                else:
                    # If next line isn't a target (unexpected), just keep as-is
                    translated_lines.append(line)
            else:
                # For all other lines, keep them unchanged
                translated_lines.append(line)

            # Show progress every 100 lines
            if i % 100 == 0:
                st.write(f'Translated {i}/{total_lines} lines')

            i += 1  # Move to the next line

        # Write the translated content to a new file (keeping the original name)
        output_file_path = os.path.join("/tmp", original_filename)
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.writelines(translated_lines)

        st.success(f"Translation completed. Translated {translated_count} lines.")

        # Offer download of the translated file
        with open(output_file_path, 'rb') as file:
            st.download_button(
                label="Download Translated XLF File",
                data=file,
                file_name=original_filename,
                mime='application/octet-stream'
            )
