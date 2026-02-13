from fpdf import FPDF

pdf = FPDF(orientation='p', unit='cm', format='A4')
pdf.add_page()
pdf.set_font(family = "times", style = "B", size = 16)
pdf.cell(w=0, h=0.8, txt="Hello World!",
         align='l', new_x='LMARGIN', new_y='NEXT')
pdf.ln(0.1)

pdf.set_font(family = "times", style = "", size = 12)
pdf.cell(w=0, h=0.8, txt ="Para o mês de dezembro foram registrados um total de 190 vendas para o setor de veículos importados ",
         align='l', new_x='LMARGIN', new_y='NEXT')
pdf.ln(1)
pdf.set_font(family = "times", style = "B", size = 16)
pdf.cell(w=0, h=0.8, txt ="VENDAS DE CARROS AMERICANOS",
         align='l', new_x='LMARGIN', new_y='NEXT')
pdf.ln(0.1)

pdf.set_font(family = "times", style = "", size = 12)
pdf.cell(w=0, h=0.8, txt ="Foram vendidos 100 veículos americanos",
         align='l', new_x='LMARGIN', new_y='NEXT')
pdf.ln(1)
pdf.set_font(family = "times", style = "B", size = 16)
pdf.cell(w=0, h=0.8, txt ="VENDAS DE CARROS ITALIANOS",
         align='l', new_x='LMARGIN', new_y='NEXT')
pdf.ln(0.1)
pdf.set_font(family = "times", style = "", size = 12)
pdf.cell(w=0, h=0.8, txt ="Foram vendidos 90 veículos italianos",
         align='l', new_x='LMARGIN', new_y='NEXT')

pdf.output("Desafio Aula PDF.pdf")