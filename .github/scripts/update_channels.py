import os
import glob

def update_m3u8_files():
    new_username = os.environ.get("NEW_USERNAME")
    new_password = os.environ.get("NEW_PASSWORD")
    
    if not new_username or not new_password:
        print("Error: Username or Password not provided!")
        return

    files = glob.glob('**/*.m3u8', recursive=True)
    print(f"Found {len(files)} m3u8 files.")
    
    if not files:
        print("No .m3u8 files found.")
        return

    updated_any = False
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        file_updated = False
        
        for line in lines:
            # إذا السطر يحتوي على رابط السيرفر
            if "http://line.play01.top/live/" in line:
                try:
                    # تقسيم الرابط لاستخراج الجزء الأخير الثابت (اسم الملف أو رقم القناة مثل /3854.m3u8)
                    parts = line.strip().split('/')
                    # الجزء الأخير هو اسم ملف الـ m3u8 والرقم
                    if len(parts) >= 6:
                        # parts[0]: http:, parts[2]: line.play01.top, parts[3]: live, parts[4]: old_user, parts[5]: old_pass, parts[6...]: rest
                        # نجعل البداية ثابتة ونغير اليوزر والباسورد ونحتفظ بالباقي بدقة
                        base_url = f"{parts[0]}//{parts[2]}/{parts[3]}"
                        end_part = "/".join(parts[5:]) # الحفاظ على ما بعد الباسورد
                        
                        # التنسيق الجديد للرابط
                        new_link = f"{base_url}/{new_username}/{end_part}\n"
                        
                        # الحفاظ على الـ tags الخاصة بـ m3u8 لو كانت في نفس السطر أو التعامل معه كـ URL مباشر
                        if line.startswith("http"):
                            new_lines.append(new_link)
                        else:
                            # لو الرابط مدمج مع نص آخر
                            fixed_line = line.replace(f"/{parts[4]}/{parts[5]}/", f"/{new_username}/{new_password}/")
                            new_lines.append(fixed_line)
                            
                        file_updated = True
                        continue
                except Exception as e:
                    print(f"Error parsing line: {line.strip()} -> {e}")
            
            new_lines.append(line)

        if file_updated:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Successfully updated: {file_path}")
            updated_any = True
        else:
            print(f"No matching server links in: {file_path}")

if __name__ == "__main__":
    update_m3u8_files()
