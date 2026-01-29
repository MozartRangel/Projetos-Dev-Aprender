import openpyxl
import datetime

workbook = openpyxl.Workbook()  
del workbook['Sheet']   
sheet_vagas = workbook.create_sheet(title='Vagas')
sheet_vagas.append(['Empresa','vaga',"data de aplicação","retorno"])
continuar = 's'
while continuar == "s":
    empresa = input("Digite o nome da empresa: ")
    vaga = input("Digite o nome da vaga: ")
    #data de aplicação usando o calendário do sistema
    data_aplicacao = datetime.date.today().strftime("%d/%m/%Y")
    retorno = input("Qual a data(DD/MM/AAAA) limite que será feito o retorno ao candidato: ")
    sheet_vagas.append([empresa, vaga, data_aplicacao, retorno])
    continuar = input("Deseja adicionar outra vaga? (s/n): ").lower()

workbook.save('vagas.xlsx')