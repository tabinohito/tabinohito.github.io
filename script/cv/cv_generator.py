from bs4 import BeautifulSoup
from fpdf import FPDF
import yaml

# PDFクラスの定義
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 20)
        self.cell(0, 10, 'Taro Tako', 0, 1, 'L')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(1)  # 行間を詰める

    def chapter_body(self, body):
        self.set_font('Arial', '', 10)  # フォントサイズを少し小さく
        self.multi_cell(0, 5, body)  # 行間を8に設定
        self.ln(1)  # 行間を詰める

if __name__ == "__main__":
    # HTMLファイルを読み込む
    with open('../../publication.html', 'r', encoding='utf-8') as file:
        soup_pub = BeautifulSoup(file, 'html.parser')

    with open('../../combination_resume.html', 'r', encoding='utf-8') as file:
        soup_resume = BeautifulSoup(file, 'html.parser')

    with open('personal_info.yaml', 'r', encoding='utf-8') as file:
        personal_info = yaml.safe_load(file)

    # PDF生成
    pdf = PDF()
    pdf.add_page()

    #0. 基本情報
    if 'email' in personal_info:
        pdf.chapter_body(f"Email: {personal_info['email']}")
    if 'homepage' in personal_info:
        pdf.chapter_body(f"Homepage: {personal_info['homepage']}")

    # 1. 個人情報
    pdf.chapter_title('Personal Information')
    if 'date_of_birth' in personal_info:
        pdf.chapter_body(f"Date of Birth: {personal_info['date_of_birth']}")
    if 'research_interests' in personal_info:
        pdf.chapter_body(f"Research Interests: {', '.join(personal_info['research_interests'])}")

    # 2. 学歴を取得
    pdf.chapter_title('Education')
    education_found = False
    for edu in soup_resume.select('.education li'):
        school = edu.select_one('.school-name').get_text(strip=True).replace(',', ', ') 
        degree = edu.select_one('.degree').get_text(strip=True)
        if 'Bachelor (Engineering)' in degree:
            if 'Associate Bachelor (Engineering)' in degree:
                degree = 'A.B.E.'
            else:
                degree = 'B.E.'
        elif 'Master (Engineering)' in degree:
            degree = 'M.E.'
        elif 'Ph.D Student' in degree:
            degree = 'Ph.D '
        
        edu_date = edu.select_one('.edu-date').get_text(strip=True)
        pdf.chapter_body(f"{degree} in {school}, {edu_date}")
        education_found = True
    if not education_found:
        pdf.chapter_body("No educational background found.")

    # 3. 職歴を取得
    pdf.chapter_title('Experience')
    experience_found = False
    for job in soup_resume.select('.experience li'):
        title = job.select_one('.job-title').get_text(strip=True)
        date = job.select_one('.job-date').get_text(strip=True)
        
        # 職務の説明を取得し、<br>を改行に置き換える
        description = job.select_one('.job-description').get_text(strip=True) if job.select_one('.job-description') else ''
        description = description.replace('<br>', '\n')  # <br>を改行に置き換え

        # 職務情報をPDFに追加
        pdf.chapter_body(f"{title} ({date})")  
        experience_found = True
    if not experience_found:
        pdf.chapter_body("No work experience found.")


    # 4. スキルを取得
    pdf.chapter_title('Skills')
    if 'skills' in personal_info:
        skills = personal_info['skills']
        
        # ソフトウェアスキルの確認
        if 'software' in skills:
            software_skills = []
            if 'advanced' in skills['software']:
                advanced_skills = skills['software']['advanced']
                if advanced_skills:
                    software_skills.append(f"Advanced: {', '.join(advanced_skills)}")
            if 'intermediate' in skills['software']:
                intermediate_skills = skills['software']['intermediate']
                if intermediate_skills:
                    software_skills.append(f"Intermediate: {', '.join(intermediate_skills)}")
            if 'basic' in skills['software']:
                basic_skills = skills['software']['basic']
                if basic_skills:
                    software_skills.append(f"Basic: {', '.join(basic_skills)}")
            if software_skills:
                pdf.chapter_body("Software Skills:\n" + "\n".join(software_skills))
        
        # ハードウェアスキルの確認
        if 'hardware' in skills:
            hardware_skills = []
            if 'intermediate' in skills['hardware']:
                intermediate_hardware = skills['hardware']['intermediate']
                if intermediate_hardware:
                    hardware_skills.append(f"Intermediate: {', '.join(intermediate_hardware)}")
            if 'basic' in skills['hardware']:
                basic_hardware = skills['hardware']['basic']
                if basic_hardware:
                    hardware_skills.append(f"Basic: {', '.join(basic_hardware)}")
            if hardware_skills:
                pdf.chapter_body("Hardware Skills:\n" + "\n".join(hardware_skills))
    else:
        pdf.chapter_body("No skills information found.")

    # 5. 論文を取得
    pdf.chapter_title('Publications')

    # 公開情報を取得するためのセレクタ
    publications = soup_pub.select('.publications table.publication-table tbody tr')
    projects_found = False

    # 国際会議だけを取得
    for pub in publications:
        # タイトルを取得
        title = pub.select_one('td:nth-child(2)').get_text(strip=True)
       
        # 著者を取得
        authors = pub.select_one('td:nth-child(3)').get_text(strip=True)
        
        # 会議名またはジャーナルを取得
        conference = pub.select_one('td:nth-child(4)').get_text(strip=True)
        
        # 日付を取得
        date = pub.select_one('td:nth-child(5)').get_text(strip=True)
        
        # DOIまたはリンクを取得
        link = pub.select_one('td:nth-child(6) a')['href'] if pub.select_one('td:nth-child(6) a') else 'No link available'
        
        # PDFに情報を書き込む
        pdf.chapter_body(f"Title: {title}\nAuthors: {authors}\nConference/Journal: {conference}\nDate: {date}\nLink: {link}\n")
    # PDFを保存
    pdf.output('resume.pdf')
