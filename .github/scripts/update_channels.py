import os
import glob

def update_m3u8_files():
    new_username = os.environ.get("NEW_USERNAME")
    new_password = os.environ.get("NEW_PASSWORD")
    
    if not new_username or not new_password:
        print("Error: Username or Password not provided!")
        return

    pattern = re.compile(r'(http://line\.play01\.top/live/)([^/]+)/([^/]+)(/.*\.m3u8)')

    files = glob.glob('**/*.m3u8', recursive=True)
    
    if not files:
        print("No .m3u8 files found.")
        return

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        updated_content, count = pattern.subn(f'\\1{new_username}/{new_password}\\4', content)
        
        if count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Updated {count} links in: {file_path}")
        else:
            print(f"No matching links found in: {file_path}")

if __name__ == "__main__":
    import re
    update_m3u8_files()
