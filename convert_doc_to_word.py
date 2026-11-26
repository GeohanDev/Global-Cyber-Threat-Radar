import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import re
import os

def clean_xml_str(s):
    if not isinstance(s, str):
        return s
    return "".join(ch for ch in s if ch in ("\t", "\n", "\r") or ord(ch) >= 32)

orig_add_run = docx.text.paragraph.Paragraph.add_run
def safe_add_run(self, text=None, style=None):
    if text is not None:
        text = clean_xml_str(text)
    return orig_add_run(self, text=text, style=style)
docx.text.paragraph.Paragraph.add_run = safe_add_run

def set_cell_background(cell, hex_color):
    """Set background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set cell margins in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_word_documentation(md_path, docx_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    doc = docx.Document()

    # Page Margins: 1 inch everywhere
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header & Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Global AI Cyberattack Threat Radar | Technical Documentation")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(140, 150, 165)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Internal IT & AI SOC Security Intelligence — Confidential")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(140, 150, 165)

    # Styles setup
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = RGBColor(30, 41, 59) # Slate 800

    # Parse markdown lines
    lines = md_text.split('\n')
    i = 0
    in_code_block = False
    code_lines = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Handle Code Block Start/End
        if stripped.startswith('```'):
            if in_code_block:
                # End code block -> write table
                in_code_block = False
                code_text = '\n'.join(code_lines)
                table = doc.add_table(rows=1, cols=1)
                table.alignment = WD_TABLE_ALIGNMENT.CENTER
                cell = table.cell(0, 0)
                set_cell_background(cell, 'F1F5F9') # Slate 100
                set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
                cp = cell.paragraphs[0]
                cp.paragraph_format.space_before = Pt(2)
                cp.paragraph_format.space_after = Pt(2)
                crun = cp.add_run(code_text)
                crun.font.name = 'Consolas'
                crun.font.size = Pt(9.5)
                crun.font.color.rgb = RGBColor(15, 23, 42)
                p_after = doc.add_paragraph()
                p_after.paragraph_format.space_before = Pt(0)
                p_after.paragraph_format.space_after = Pt(4)
                code_lines = []
            else:
                in_code_block = True
                code_lines = []
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        # Markdown Table Detection
        if stripped.startswith('|') and '|' in stripped[1:]:
            # Collect all table lines
            table_lines = [stripped]
            i += 1
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            
            # Parse table
            rows_data = []
            for tl in table_lines:
                # Skip divider line like | :--- | :--- |
                if re.match(r'^\|[\s\:\-\|]+$', tl):
                    continue
                cells = [c.strip() for c in tl.strip('|').split('|')]
                rows_data.append(cells)
            
            if rows_data:
                num_cols = max(len(r) for r in rows_data)
                table = doc.add_table(rows=len(rows_data), cols=num_cols)
                table.alignment = WD_TABLE_ALIGNMENT.CENTER
                
                for r_idx, row in enumerate(rows_data):
                    is_header = (r_idx == 0)
                    for c_idx in range(num_cols):
                        cell = table.cell(r_idx, c_idx)
                        text_val = row[c_idx] if c_idx < len(row) else ""
                        # Strip simple bold markup
                        clean_text = text_val.replace('**', '').replace('`', '')
                        cell.text = clean_text
                        cp = cell.paragraphs[0]
                        cp.paragraph_format.space_before = Pt(3)
                        cp.paragraph_format.space_after = Pt(3)
                        
                        if is_header:
                            set_cell_background(cell, '1E293B') # Dark Slate header
                            set_cell_margins(cell, top=140, bottom=140, left=160, right=160)
                            for run in cp.runs:
                                run.font.name = 'Calibri'
                                run.font.size = Pt(10)
                                run.font.bold = True
                                run.font.color.rgb = RGBColor(255, 255, 255)
                        else:
                            bg_color = 'F8FAFC' if r_idx % 2 == 1 else 'FFFFFF'
                            set_cell_background(cell, bg_color)
                            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
                            for run in cp.runs:
                                run.font.name = 'Calibri'
                                run.font.size = Pt(9.5)
                                run.font.color.rgb = RGBColor(30, 41, 59)
                
                p_spacer = doc.add_paragraph()
                p_spacer.paragraph_format.space_before = Pt(2)
                p_spacer.paragraph_format.space_after = Pt(6)
            continue

        # Header 1 (# Title)
        if stripped.startswith('# '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(18)
            p.paragraph_format.space_after = Pt(8)
            run = p.add_run(stripped[2:])
            run.font.name = 'Calibri'
            run.font.size = Pt(22)
            run.font.bold = True
            run.font.color.rgb = RGBColor(30, 58, 138) # Deep Blue
            i += 1
            continue

        # Header 2 (## Section)
        if stripped.startswith('## '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(6)
            run = p.add_run(stripped[3:])
            run.font.name = 'Calibri'
            run.font.size = Pt(15)
            run.font.bold = True
            run.font.color.rgb = RGBColor(37, 99, 235) # Royal Blue
            i += 1
            continue

        # Header 3 (### Sub-section)
        if stripped.startswith('### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            p.paragraph_format.space_after = Pt(4)
            run = p.add_run(stripped[4:])
            run.font.name = 'Calibri'
            run.font.size = Pt(12.5)
            run.font.bold = True
            run.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
            i += 1
            continue

        # Header 4 (#### Sub-sub-section)
        if stripped.startswith('#### '):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(stripped[5:])
            run.font.name = 'Calibri'
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = RGBColor(71, 85, 105) # Slate 600
            i += 1
            continue

        # Blockquote (> Callout Box)
        if stripped.startswith('>'):
            quote_lines = []
            while i < len(lines) and (lines[i].strip().startswith('>') or lines[i].strip() == ''):
                if lines[i].strip().startswith('>'):
                    quote_lines.append(lines[i].strip().lstrip('>').strip())
                elif lines[i].strip() == '':
                    if i + 1 < len(lines) and lines[i+1].strip().startswith('>'):
                        quote_lines.append('')
                    else:
                        break
                i += 1
            quote_text = '\n'.join(quote_lines).strip()
            if quote_text:
                q_table = doc.add_table(rows=1, cols=1)
                q_table.alignment = WD_TABLE_ALIGNMENT.CENTER
                q_cell = q_table.cell(0, 0)
                set_cell_background(q_cell, 'F0FDF4' if 'ALERT' in quote_text or 'PLAYBOOK' in quote_text else 'EFF6FF')
                set_cell_margins(q_cell, top=120, bottom=120, left=180, right=180)
                qp = q_cell.paragraphs[0]
                qp.paragraph_format.space_before = Pt(2)
                qp.paragraph_format.space_after = Pt(2)
                parts = re.split(r'(\*\*.*?\*\*)', quote_text)
                for part in parts:
                    if part.startswith('**') and part.endswith('**'):
                        qr = qp.add_run(part[2:-2])
                        qr.font.bold = True
                    else:
                        qp.add_run(part.replace('`', ''))
                for r in qp.runs:
                    r.font.name = 'Calibri'
                    r.font.size = Pt(10)
                    r.font.italic = True
                    r.font.color.rgb = RGBColor(22, 101, 52) if 'ALERT' in quote_text or 'PLAYBOOK' in quote_text else RGBColor(30, 64, 175)
                p_sp = doc.add_paragraph()
                p_sp.paragraph_format.space_before = Pt(0)
                p_sp.paragraph_format.space_after = Pt(4)
            continue

        # Horizontal Divider (---)
        if stripped == '---':
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(8)
            run = p.add_run("―" * 50)
            run.font.color.rgb = RGBColor(203, 213, 225)
            i += 1
            continue

        # Bullet List (* or -)
        if stripped.startswith('* ') or stripped.startswith('- '):
            bullet_text = stripped[2:]
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            
            # Simple bold parsing inside bullet
            parts = re.split(r'(\*\*.*?\*\*)', bullet_text)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    r = p.add_run(clean_xml_str(part[2:-2]))
                    r.font.bold = True
                else:
                    p.add_run(part.replace('`', ''))
            i += 1
            continue

        # Numbered List (1. , 2. )
        m_num = re.match(r'^(\d+)\.\s+(.*)', stripped)
        if m_num:
            num_val = m_num.group(1)
            text_val = m_num.group(2)
            p = doc.add_paragraph(style='List Number')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            parts = re.split(r'(\*\*.*?\*\*)', text_val)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    r = p.add_run(clean_xml_str(part[2:-2]))
                    r.font.bold = True
                else:
                    p.add_run(part.replace('`', ''))
            i += 1
            continue

        # Checkbox lists (* [x] or * [ ])
        if stripped.startswith('* [x]') or stripped.startswith('* [ ]'):
            is_checked = stripped.startswith('* [x]')
            box = "☑ " if is_checked else "☐ "
            item_text = stripped[5:].strip()
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(2)
            r_box = p.add_run(box)
            r_box.font.bold = True
            r_box.font.color.rgb = RGBColor(16, 185, 129) if is_checked else RGBColor(148, 163, 184)
            p.add_run(item_text.replace('**', ''))
            i += 1
            continue

        # Regular Paragraph
        if stripped:
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            
            parts = re.split(r'(\*\*.*?\*\*)', line)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    r = p.add_run(clean_xml_str(part[2:-2]))
                    r.font.bold = True
                else:
                    p.add_run(part.replace('`', ''))

        i += 1

    try:
        doc.save(docx_path)
        print(f"Successfully generated Word document at: {docx_path}")
    except PermissionError:
        fallback_path = docx_path.replace('.docx', '_updated.docx')
        doc.save(fallback_path)
        print(f"Notice: {docx_path} is currently locked by another program (e.g. Word). Saved updated version to: {fallback_path}")

if __name__ == "__main__":
    src_md = "DOCUMENTATION.md"
    dest_docx_1 = "DOCUMENTATION.docx"
    dest_docx_2 = r"C:\Users\Foong Shi Hui\.gemini\antigravity\brain\69e43c11-51b4-4512-a70f-ff2080663807\DOCUMENTATION.docx"
    
    create_word_documentation(src_md, dest_docx_1)
    create_word_documentation(src_md, dest_docx_2)
