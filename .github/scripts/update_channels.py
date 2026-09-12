import os
import glob
import re

def update_m3u8_files():
    new_username = os.environ.get("NEW_USERNAME")
    new_password = os.environ.get("NEW_PASSWORD")
    
    if not new_username or not new_password:
        print("Error: Username or Password not provided!")
        return

    # التعبير النمطي الدقيق: يبحث عن بداية الرابط الثابت، ثم يلتقط اليوزر القديم والباسورد القديم بغض النظر عن ما هما، ثم يحافظ على باقي الرابط (رقم القناة وامتداد m3u8)
    # مثال للرابط: http://line.play01.top/live/OLD_USER/OLD_PASS/3854.m3u8
    pattern = re.compile(r'(http://line\.play01\.top/live/)([^/]+)/([^/]+)(/.*)')

    files = glob.glob('**/*.m3u8', recursive=True)
    print(f"Found {len(files)} m3u8 files in total.")
    
    if not files:
        print("No .m3u8 files found.")
        return

    updated_any = False
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # استبدال البداية الثابتة + اليوزر الجديد + الباسورد الجديد + الجزء الأخير الثابت
        # المجموعة الأولى (\1): http://line.play01.top/live/
        # المجموعة الرابعة (\4): /3854.m3u8 (أو أي رقم وقناة يتبعها)
        updated_content, count = pattern.subn(rf'\1{new_username}/{new_password}\4', content)
        
        if count > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"Successfully updated {count} links in: {file_path}")
            updated_any = True
        else:
            print(f"No matching links found in: {file_path}")

    if not updated_any:
        print("Warning: No links matched the pattern in any file. Make sure your m3u8 files contain links starting with http://line.play01.top/live/")

if __name__ == "__main__":
    update_m3u8_files()
