import os
import glob

def update_m3u8_files():
    new_username = os.environ.get("NEW_USERNAME")
    new_password = os.environ.get("NEW_PASSWORD")
    
    if not new_username or not new_password:
        print("Error: Username or Password not provided!")
        return

    files = glob.glob('**/*.m3u8', recursive=True)
    print(f"Found {len(files)} m3u8 files in total.")
    
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
            if "http://line.play01.top/live/" in line:
                try:
                    parts = line.strip().split('/')
                    # parts[0]: http:, parts[2]: line.play01.top, parts[3]: live
                    # parts[4]: اليوزر القديم، parts[5]: الباسورد القديم
                    if len(parts) >= 6:
                        base_url = f"{parts[0]}//{parts[2]}/{parts[3]}"
                        end_part = "/".join(parts[5:]) # الحفاظ على ما بعد اليوزر والباسورد القديم
                        
                        # إعادة بناء الرابط باليوزر والباسورد الجدد بدقة
                        # نأخذ الباقي من بعد الباسورد القديم (أي من parts[6] فصاعداً)
                        rest_of_path = "/".join(parts[6:]) if len(parts) > 6 else parts[5]
                        
                        # بناء الرابط الجديد تماماً
                        # ملاحظة: parts[5] هو الباسورد القديم، وما بعده هو رقم القناة والامتداد
                        # لذا الأفضل استبدال الجزئية الخاصة باليوزر والباسورد مباشرة من السطر الأصلي لتفادي أي خطأ في التقسيم
                        pass
                except Exception:
                    pass
                
                # طريقة أبسط وأضمن: البحث عن الجزء الثابت واستبدال اليوزر والباسورد عبر الـ replace المباشر
                # سنقوم بالبحث عن النص القديم في السطر واستبداله
            
            # حل بديل ومضمون 100% للسطر الذي يحتوي على الرابط:
            if "http://line.play01.top/live/" in line:
                # تقسيم السطر حسب المسافات أو علامات التنصيص إن وجدت للحفاظ على الـ tags
                # الروابط عادة تكون بالشكل: http://line.play01.top/live/USER/PASS/file.m3u8
                words = line.split()
                line_updated = False
                new_words = []
                for word in words:
                    if "http://line.play01.top/live/" in word:
                        p = word.split('/')
                        if len(p) >= 6:
                            # p[4] هو اليوزر القديم، p[5] هو الباسورد القديم
                            # نقوم بتعديلهم وترك الباقي كما هو
                            p[4] = new_username
                            p[5] = new_password
                            new_word = "/".join(p)
                            new_words.append(new_word)
                            line_updated = True
                            file_updated = True
                            continue
                    new_words.append(word)
                
                if line_updated:
                    new_lines.append(" ".join(new_words) + "\n")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        if file_updated:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Successfully updated: {file_path}")
            updated_any = True
        else:
            print(f"No changes made in: {file_path}")

if __name__ == "__main__":
    update_m3u8_files()
