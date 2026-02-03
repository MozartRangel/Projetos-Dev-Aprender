from playwright.sync_api import sync_playwright
import openpyxl

#Iniciar o Playwright e abrir o navegador
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://produtos-devaprender.netlify.app/", wait_until ="domcontentloaded")

    produtos = []
    #obter todos os produtos
    cartao_produtos = page.locator(".card").all()
    
    #Extrair as 3 informações de cada produto:*nome, preço, descrição*
    for cartao in cartao_produtos:
        produto = cartao.locator(".title").inner_text()
        preco = cartao.locator(".price").inner_text()
        descricao = cartao.locator(".desc").inner_text()

        produtos.append([produto, preco, descricao])
        print(f"Produto: {produto} | Preço: {preco} | Descrição: {descricao}")

    browser.close()   

#Workbook
planilha = openpyxl.Workbook()
del planilha["Sheet"]
Sheet_Produtos = planilha.create_sheet("Produtos") 

#Cabeçalho
Sheet_Produtos.append(["Nome", "Preço", "Descrição"])
for produto in produtos:
    Sheet_Produtos.append(produto)

#salvar a planilha
planilha.save("produtos.xlsx")


