import io
import re
from datetime import datetime
import PyPDF2
from docx import Document

def extrair_dados_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        texto = ""
        for page in reader.pages:
            if page.extract_text():
                texto += page.extract_text() + "\n"
        
        # Regex para extrair a Placa
        placa_match = re.search(r"Placas\s*[:]\s*(.+)", texto, re.IGNORECASE)
        placas = placa_match.group(1).strip() if placa_match else ""
        
        # Regex para extrair a Quantidade
        # Pode aparecer como "Quantidade: : 61.000,000 L" ou "Quantidade: 61000"
        quant_match = re.search(r"Quantidade\s*[:]+?\s*(?:[:]\s*)?([\d\.,]+)", texto, re.IGNORECASE)
        quantidade = quant_match.group(1).strip() if quant_match else ""
        if quantidade.endswith(",000"):
            quantidade = quantidade[:-4]
            
        return placas, quantidade
        
    except Exception as e:
        print(f"Erro ao extrair PDF: {e}")
        return "", ""

def preencher_certificado(template_file, numero_cert, placa, quantidade, data):
    doc = Document(template_file)
    
    substituicoes = {
        "{{NUMERO}}": numero_cert,
        "{{DATA}}": data,
        "{{PLACA}}": placa,
        "{{QUANTIDADE}}": quantidade
    }
    
    # Substituir em parágrafos comuns
    for p in doc.paragraphs:
        for tag, valor in substituicoes.items():
            if tag in p.text:
                # Substituição preservando o run o máximo possível ou resetando
                for run in p.runs:
                    if tag in run.text:
                        run.text = run.text.replace(tag, str(valor))
                # Fallback caso a tag esteja dividida em múltiplos runs
                if tag in p.text:
                    p.text = p.text.replace(tag, str(valor))
                
    # Substituir em tabelas
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for tag, valor in substituicoes.items():
                        if tag in p.text:
                            for run in p.runs:
                                if tag in run.text:
                                    run.text = run.text.replace(tag, str(valor))
                            if tag in p.text:
                                p.text = p.text.replace(tag, str(valor))
                            
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    
    return doc_io
