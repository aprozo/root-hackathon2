import os
# /// \file
# /// \ingroup tutorial_hist
# /// \notebook
# /// \preview
# /// Example showing how to combine the various candle plot options.
# ///
# /// \macro_image (tcanvas_js)
# /// \macro_code
# ///
# /// \author Georg Troska


def list_files(dir):
    r = []
    for root, dirs, files in os.walk(dir):
        for name in files:
            r.append(os.path.join(root, name))
    return r


def add_preview_line(comment_prefix, lines):
    preview_line = '\\preview'
    line_before='\\notebook'
    if preview_line not in lines:
        for i, line in enumerate(lines):
            if line.strip() == f'{comment_prefix} {line_before}':
                lines.insert(i+1, f'{comment_prefix} {preview_line}\n')
                return lines
    return lines
    


def add_or_update_macro_image_to_files(folder_path):
    """
    Adds or updates the line '/// \\macro_image (tcanvas_js)' or '## \\macro_image (tcanvas_js)'
    before the line '/// \\macro_code' or '## \\macro_code', respectively, in files if they contain
    'Draw(', 'DrawCopy(', or 'DrawClone('. If a line already contains '\\macro_image', ensures it
    includes '(tcanvas_js)'.
    
    Parameters:
        folder_path (str): The path to the folder containing the files to process.
    """
    # Supported file extensions and their comment styles
    comment_styles = {
        '.C': '///',
        '.py': '##'
    }
    
    # Traverse through files in the given folder and its subfolders
    for file_path in list_files(folder_path):
        file_extension = os.path.splitext(file_path)[1]
                
        # Check for valid file extensions
        if os.path.isfile(file_path) and file_extension in comment_styles:
            comment_prefix = comment_styles[file_extension]
            print (f'Processing {file_path}')
            
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # Check if the file contains 'Draw(', 'DrawCopy(', or 'DrawClone('
            if any(phrase in ''.join(lines) for phrase in ['Draw(', 'DrawCopy(', 'DrawClone(']):
                modified = False
                new_lines = []
                
                for line in lines:
                    if line.strip().startswith(f'{comment_prefix} \\macro_image'):
                        # Update the macro image line to include '(tcanvas_js)'
                        if '(tcanvas_js)' not in line:
                            new_lines.append(f'{comment_prefix} \\macro_image (tcanvas_js)\n')
                            modified = True
                        else:
                            new_lines.append(line)  # Leave the line as is
                    elif line.strip() == f'{comment_prefix} \\macro_code' and not any(l.strip().startswith(f'{comment_prefix} \\macro_image') for l in lines):
                        # Insert the macro image line before '\\macro_code' if not already present
                        new_lines.append(f'{comment_prefix} \\macro_image (tcanvas_js)\n')
                        new_lines.append(line)
                        modified = True
                    else:
                        new_lines.append(line)

                # Add a preview line if it doesn't exist
                new_lines = add_preview_line(comment_prefix, new_lines)

                
                # Write changes back to the file if modified
                if modified:
                    print (f'Updating {file_path}')
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.writelines(new_lines)

# Example usage
folder_path = './test'  # Replace with the path to your folder
add_or_update_macro_image_to_files(folder_path)
