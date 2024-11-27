import os
import subprocess

def list_files(directory):
    r = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            r.append(os.path.join(root, name))
    return r


def patch_dates(folder_path):
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
         
            # check if the \date command is present in the file
            is_date_present = any(f'{comment_prefix} \\date' in line for line in lines)

            is_modified = False
            if not is_date_present:
                # git log -1 --date=format:'%b %Y' --pretty=format:"%ad" -- dataframe/Fibonacci.C
                git_date = subprocess.check_output(['git', 'log','-1','--date=format:\'%B %Y\'', '--pretty=format:"%ad"', file_path]).decode('utf-8')
                # Format the output
                git_date = git_date.strip().replace('"', '').replace('\'', '')       
                # Add the \date command to the file
                for i, line in enumerate(lines):
                    # Insert the \date command before the \author command as it is the last command in doxygen comments
                    if line.strip().startswith(f'{comment_prefix} \\author'):
                        lines.insert(i, f'{comment_prefix} \\date {git_date}\n')
                        is_modified = True
                        break
            
            # Write changes back to the file if modified
            if is_modified:
                print (f'Updating {file_path}')
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.writelines(lines)


folder_path = '/home/prozorov/dev/hackathon/root/tutorials/'  # Replace with the path to your folder
patch_dates(folder_path)

# include_directories = ['dataframe','fit','tree','roofit','hist','graphs','math']
# for mydir in include_directories:
#     print (f'Processing {folder_path+mydir}')
#     patch_dates(folder_path+mydir)