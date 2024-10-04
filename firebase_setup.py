"""
Projeto de Extensão Universitária - Estácio 2024 - Marcus Cesar Pereira Ferreira - Matrícula - 202102340918@alunos.estacio.br
Resumo do Projeto: Este sistema integra várias tecnologias e foi desenvolvido para a Extensão Universitária na Estácio 2024. Localmente, utiliza Python para integração com o Firebase do Google Cloud e o Cloud Firestore, armazenando dados de pacientes de fonoaudiologia.

        A interface em Tkinter permite a coleta de informações como nome, idade e diagnóstico. O sistema também oferece funcionalidades como geração de relatórios em PDF e gráficos de análise, além de sincronizar automaticamente os dados locais e na nuvem. O formulário utiliza HTML e JavaScript para encaminhar os dados ao Cloud Firestore, que os valida e armazena.
        O objetivo do formulário WEB https://fonart-8cd50.web.app/ é coletar dados estatísticos de pacientes em tratamento fonoaudiológico. A coleta de informações como idade, diagnóstico, localidade e tratamento é essencial para entender as necessidades dos pacientes e aprimorar a atuação da equipe. O consentimento do paciente é obrigatório para a utilização dos dados, tratados com a máxima confidencialidade, visando à conformidade com a LGPD.
"""
# Importações necessárias para o sistema

import os
import csv
import logging
from datetime import datetime
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials,firestore
from tkinter import ttk, messagebox
import pandas as pd
import tkinter as tk
from PIL import Image, ImageTk
import threading
import matplotlib.pyplot as plt  # Importação do matplotlib para gráficos
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import random
import string

# Configuração do logging
log_path = r'C:\Projeto_Estacio_2024-Fono\Projeto_Fonart\logs\system.log'
logging.basicConfig(filename=log_path,
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Inicialização do Firebase
def inicializar_firebase():
    """Inicializa a conexão com o Firebase e retorna a instância do Firestore."""
    try:
        if not firebase_admin._apps:  # Verifica se o Firebase já foi inicializado
            # Configuração do Firebase
            cred = credentials.Certificate(r"C:\Projeto_Estacio_2024-Fono\Projeto_Fonart\dados\Firebase\fonart-8cd50-firebase-INSIRA SEUS CREDENCIAIS.json")
            firebase_admin.initialize_app(cred)
        db = firestore.client()  # Conexão com o Firestore
        return db
    except Exception as e:
        print(f"Erro ao inicializar o Firebase: {e}")
        return None

# Chama a função para inicializar e obter o cliente do Firestore
db = inicializar_firebase()

# Função para validar os dados
def validar_dados(nome, idade, diagnostico, localidade, tratamento, mes, consentimento):
    """Valida os dados de entrada antes de salvar."""
    if not (nome and idade and diagnostico and localidade and tratamento and mes):
        messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos!")
        return False
    if not consentimento:
        messagebox.showwarning("Aviso", "É necessário o consentimento para uso de dados!")
        return False
    try:
        if not isinstance(int(idade), int) or int(idade) < 0:
            messagebox.showwarning("Aviso", "A idade deve ser um número válido!")
            return False
    except ValueError:
        messagebox.showwarning("Aviso", "A idade deve ser um número válido!")
        return False
    return True

# Função para salvar dados no Firebase
def salvar_dados_firebase(dados_paciente):
    global status_label  # Torna o status_label acessível dentro da função
    try:
        db = inicializar_firebase()  # Inicializa o Firebase e conecta ao Firestore
        if db:
            dados_paciente['data_modificacao'] = datetime.now().isoformat()
            db.collection('pacientes').add(dados_paciente)
            # Lógica para salvar os dados no Firebase...
            print("Dados salvos com sucesso no Firebase!")
            logging.info(f"Dados salvos no Firebase: {dados_paciente}")

            # Atualiza o status de sucesso
            status_label.config(text="DADOS ENVIADOS COM SUCESSO!", fg="green")
    except Exception as e:
        print(f"ERRO AO SALVAR DADOS: {e}")
        logging.error(f"Erro ao salvar dados no Firebase: {e}")

        # Atualiza o status de erro
        status_label.config(text="Erro ao enviar os dados.", fg="red")

# Função para salvar os dados no CSV local
def salvar_dados_csv(dados_paciente):
    global status_label  # Torna o status_label acessível dentro da função
    arquivo_csv = r'C:\\Projeto_Estacio_2024-Fono\\Projeto_Fonart\\dados\\pacientes\\pacientes.csv'
    campos = ['nome', 'idade', 'diagnostico', 'localidade', 'tratamento', 'mes', 'consentimento', 'data_modificacao']
    try:
        with open(arquivo_csv, mode='a', newline='', encoding='utf-8') as arquivo:
            escritor_csv = csv.DictWriter(arquivo, fieldnames=campos)
            if arquivo.tell() == 0:
                escritor_csv.writeheader()

            escritor_csv.writerow(dados_paciente)
            logging.info(f'Dados salvos no CSV: {dados_paciente}')
            print(f"Dados salvos com sucesso no arquivo {arquivo_csv}!")

            # Atualiza o status de sucesso
            status_label.config(text="Dados salvos no CSV com sucesso!", fg="green")
    except Exception as e:
        logging.error(f'Erro ao salvar dados no CSV: {e}')
        print(f"Erro ao salvar dados no CSV: {e}")

        # Atualiza o status de erro
        status_label.config(text="Erro ao salvar os dados no CSV.", fg="red")

# Função para salvar os dados após validação
def salvar_dados(db, nome, idade, diagnostico, localidade, tratamento, mes, consentimento, data_modificacao):
    data_modificacao = datetime.now()  # Corrige o uso do datetime
   
    # Exibe a data de modificação
    print(f"Data de Modificação: {data_modificacao}")
   
    # Lógica para salvar os dados no banco de dados
    """Salva os dados se forem válidos."""
    if validar_dados(nome, idade, diagnostico, localidade, tratamento, mes, consentimento):
        dados_paciente = {
            "nome": nome,
            "idade": idade,
            "diagnostico": diagnostico,
            "localidade": localidade,
            "tratamento": tratamento,
            "mes": mes,
            "consentimento": consentimento
            
        }
        print(f"Salvando dados: {dados_paciente}")  # Log detalhado
        salvar_dados_firebase(dados_paciente)  # Salva no Firebase

# Sincronização Firestore para CSV 
def sincronizar_firestore_para_csv(db):
    """Sincroniza os dados do Firestore com o arquivo CSV."""
    caminho_csv = "C:/Projeto_Estacio_2024-Fono/Projeto_Fonart/dados/pacientes/pacientes.csv"
    try:
        pacientes_ref = db.collection('pacientes')
        docs = pacientes_ref.stream() 
        
        with open(caminho_csv, mode='w', newline='', encoding='utf-8') as arquivo_csv:
            # Adicionar 'data_modificacao' à lista de campos
            campos = ["nome", "idade", "diagnostico", "localidade", "tratamento", "mes", "consentimento", "data_modificacao"]
            escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=campos)
            escritor_csv.writeheader()  # Escreve o cabeçalho

            # Escreve cada documento do Firestore no CSV
            for doc in docs:
                dados = doc.to_dict()
                
                # Verifica se 'data_modificacao' está presente no documento, senão insere uma data padrão
                if 'data_modificacao' not in dados:
                    dados['data_modificacao'] = "Não disponível"  # Você pode mudar essa linha para uma data padrão, se preferir
                
                escritor_csv.writerow(dados)
        
        print("Sincronização do Firestore para o CSV concluída!")
    
    except Exception as e:
        print(f"Erro ao sincronizar Firestore para CSV: {e}")

# Sincronização CSV para Firestore
def sincronizar_csv_para_firestore(db):
    """Sincroniza os dados do CSV com o Firestore, resolvendo conflitos de data de modificação."""
    caminho_csv = "C:/Projeto_Estacio_2024-Fono/Projeto_Fonart/dados/pacientes/pacientes.csv"
    try:
        with open(caminho_csv, mode='r', encoding='utf-8') as arquivo_csv:
            leitor_csv = csv.DictReader(arquivo_csv)
            for linha in leitor_csv:
              
                # Verifica se o documento já existe
                doc_ref = db.collection('pacientes').where('nome', '==', linha['nome']).get()  # Usando argumentos nomeados
                
                if doc_ref:
                    
                    # Compara datas de modificação
                    for doc in doc_ref:
                        if linha.get('data_modificacao', '') > doc.to_dict().get('data_modificacao', ''):
                            db.collection('pacientes').document(doc.id).set(linha)  # Atualiza Firestore
                else:
                    db.collection('pacientes').add(linha)  # Adiciona novo documento
        print("Sincronização do CSV para o Firestore concluída!")
    except Exception as e:
        print(f"Erro ao sincronizar CSV para Firestore: {e}")

# Função para iniciar a sincronização em uma thread
def iniciar_sincronizacao(db):
    sincronizar_firestore_para_csv(db)
    sincronizar_csv_para_firestore(db)

# Função para mostrar gráfico
def mostrar_grafico():
   
    # Lendo dados do CSV
    csv_path = 'C:/Projeto_Estacio_2024-Fono/Projeto_Fonart/dados/pacientes/pacientes.csv'
    df = pd.read_csv(csv_path)
   
    # Agrupar os dados do CSV por localidade e contar o número de tratamentos
    tratamentos_por_localidade_csv = df['localidade'].value_counts()
   
    # Consultar dados do Firebase
    tratamentos_por_localidade_firebase = {}
    pacientes_ref = db.collection('pacientes')
    for doc in pacientes_ref.stream():
        data = doc.to_dict()
        localidade = data.get('localidade')
        if localidade:
            tratamentos_por_localidade_firebase[localidade] = tratamentos_por_localidade_firebase.get(localidade, 0) + 1
   
    # Juntando dados do CSV e do Firebase
    localidades = list(set(tratamentos_por_localidade_csv.index).union(set(tratamentos_por_localidade_firebase.keys())))
    tratamentos_por_localidade = [
        tratamentos_por_localidade_csv.get(localidade, 0) + tratamentos_por_localidade_firebase.get(localidade, 0)
        for localidade in localidades
    ]
   
    # Criando o gráfico de barras
    plt.figure(figsize=(8, 6))
    plt.bar(localidades, tratamentos_por_localidade, color=['blue', 'green', 'orange'])
    plt.title("Tratamentos por Localidade")
    plt.xlabel("Localidade")
    plt.ylabel("Número de Tratamentos")
  
    # Exibir o gráfico
    plt.show()
   
    # Define o diretório base do projeto
diretorio_base = r"C:\Projeto_Estacio_2024-Fono\Projeto_Fonart"

# Função para gerar relatório PDF
def gerar_relatorio_pdf():
    print("Iniciando geração do relatório PDF...")
    """
    Gera um relatório em PDF com os dados dos pacientes.
    Anonimiza o nome dos pacientes para proteção de dados, conforme a LGPD.
    Inclui o logotipo da empresa centralizado no cabeçalho e evita cortes.
    Também adiciona as informações da empresa no rodapé do relatório, com margens consistentes.
    Agora, inclui um espaçamento extra entre o título e os dados.
    Adiciona numeração automática aos dados dos pacientes.
    """
    try:
        if not messagebox.askyesno("Atenção", "Você está prestes a acessar dados pessoais - (Nome será anonimizado). Deseja continuar?"):
            return
        arquivo = os.path.join(diretorio_base, 'dados', 'pacientes', 'pacientes.csv')
        if not os.path.exists(arquivo):
            logging.warning("Tentativa de gerar relatório sem dados disponíveis.")
            messagebox.showwarning("Aviso", "Nenhum dado para gerar o relatório.")
            return
        df = pd.read_csv(arquivo)
        pdf_file = os.path.join(diretorio_base, 'dados', 'relatorios', 'relatorio_pacientes.pdf')
        c = canvas.Canvas(pdf_file, pagesize=letter)
       
        # Adiciona o logotipo centralizado
        logotipo_path = r"C:\Projeto_Estacio_2024-Fono\Projeto_Fonart\assets\fonart.matriz.jpg"
        logotipo_width = 100
        logotipo_height = 46
        x_position = (letter[0] - logotipo_width) / 2
        y_position = 720
        c.drawImage(logotipo_path, x_position, y_position, width=logotipo_width, height=logotipo_height)
        title = "Fonart - Espaço Fonoaudiologia Aplicada e Saúde Integral - Relatório de Pesquisa Estatística"
        title_x = 100
        title_y = 710
        for line in title.split(" - "):
            c.drawString(title_x, title_y, line)
            title_y -= 15
        title_y -= 30
        c.setFont("Helvetica", 10)  # Define o tamanho da fonte aqui
        c.drawString(100, title_y, "Num. - Nome - Idade - Diagnóstico - Localidade - Tratamento - Mês")
        linha_atual = title_y - 20
        for index, row in df.iterrows():
            if linha_atual < 60:  # Checa se vai ultrapassar o rodapé
                adicionar_rodape(c)  # Adiciona rodapé antes de mudar de página
                c.showPage()  # Inicia uma nova página
                linha_atual = 750  # Reinicia a posição vertical
               
                # Adiciona o logotipo novamente na nova página
                c.drawImage(logotipo_path, x_position, y_position, width=logotipo_width, height=logotipo_height)
               
                # Redefine o título e a numeração
                for line in title.split(" - "):
                    c.drawString(title_x, title_y, line)
                    title_y -= 15
                title_y -= 30
                c.drawString(100, title_y, "Num. - Nome - Idade - Diagnóstico - Localidade - Tratamento, Mês")
                linha_atual = title_y - 20
            numero = index + 1
            nome_anonimo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            c.drawString(100, linha_atual, f"{numero}. {nome_anonimo} - {row['idade']} - {row['diagnostico']} - {row['localidade']} - {row['tratamento']} - {row['mes']}")
            linha_atual -= 20  # Move para a próxima linha
       
        # Adiciona rodapé na última página
        adicionar_rodape(c)
        c.save()
        logging.info(f"Relatório PDF gerado com sucesso: {pdf_file}")
        messagebox.showinfo("Sucesso", f"Relatório gerado: {pdf_file}")
        
        # Após gerar o PDF, abrir o arquivo
        abrir_arquivo(pdf_file)
    except Exception as e:
        logging.error(f"Erro ao gerar relatório PDF: {e}")
        messagebox.showerror("Erro", "Falha ao gerar o relatório PDF.")  
def abrir_arquivo(caminho):
    try:
        os.startfile(caminho)  # Abre o arquivo no visualizador padrão
    except Exception as e:
        logging.error(f"Erro ao abrir o arquivo: {e}")
        messagebox.showerror("Erro", "Falha ao abrir o arquivo PDF.")
def adicionar_rodape(c):
    """ Adiciona o rodapé e numeração da página no PDF. """
    c.setFont("Helvetica", 8)  # Define o tamanho da fonte para o rodapé
    rodape_texto1 = "FONART - Maxxi Business Freguesia"
    rodape_texto2 = "Estr. dos Três Rios, 1097 - Sala 530, Freguesia de Jacarepaguá, 22745-004"
    rodape_texto3 = "E-mail: fonartrio@gmail.com - Tel.: 21 9 7282-2546"
    rodape_texto4 = "Relatório gerado via tecnologia Python, Extensão Universitária - Estácio 2024 - Marcus Cesar Ferreira"
    c.drawString(100, 50, rodape_texto1)
    c.drawString(100, 40, rodape_texto2)
    c.drawString(100, 30, rodape_texto3)
    c.drawString(100, 20, rodape_texto4)
   
    # Adiciona numeração da página
    c.drawString(500, 20, f"Página {c.getPageNumber()}")

# Criação da interface gráfica
def criar_janela_principal(db):
    global status_label  # Declara que irá usar a variável global
    """Cria a janela principal da aplicação."""
    janela = tk.Tk()
    janela.title("Sistema FONART")
   
    # Carrega o logotipo da empresa
    with Image.open(r"C:\Projeto_Estacio_2024-Fono\Projeto_Fonart\assets\fonart.matriz.png") as imagem_original:
        imagem_redimensionada = imagem_original.resize((100, 50))
        imagem_logo = ImageTk.PhotoImage(imagem_redimensionada)
    label_logo = tk.Label(janela, image=imagem_logo)
    label_logo.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
   
    # Label de status
    status_label = tk.Label(janela, text="", font=("Arial", 10), bg=janela.cget("bg"), padx=10, pady=5)
    status_label.grid(row=9, columnspan=2, padx=10, pady=10)
   
    # Campos de entrada
    tk.Label(janela, text="Nome:").grid(row=1, column=0, padx=5, pady=5)
    entry_nome = tk.Entry(janela)
    entry_nome.grid(row=1, column=1, padx=5, pady=5)
    tk.Label(janela, text="Idade:").grid(row=2, column=0, padx=5, pady=5)
    entry_idade = tk.Entry(janela)
    entry_idade.grid(row=2, column=1, padx=5, pady=5)
    tk.Label(janela, text="Diagnóstico:").grid(row=3, column=0, padx=5, pady=5)
    diagnosticos = ["Disartria", "Afasia", "Dislexia", "Disgrafia", "Disfagia", "Gagueira", "Autismo"]
    combobox_diagnostico = ttk.Combobox(janela, values=diagnosticos)
    combobox_diagnostico.grid(row=3, column=1, padx=5, pady=5)
    
    # Listagens para localidade, tratamento e meses
    localidades = ["Rio de Janeiro", "Niterói", "São Gonçalo"]
    tratamentos = ["Terapia de Linguagem", "Terapia de Voz", "Terapia de Deglutição",
                   "Reabilitação da Audição", "Terapia de Articulação", "Intervenção Precoce",
                   "Terapia de Leitura e Escrita"]
    meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", 
             "Setembro", "Outubro", "Novembro", "Dezembro"]
    tk.Label(janela, text="Localidade:").grid(row=4, column=0, padx=5, pady=5)
    combobox_localidade = ttk.Combobox(janela, values=localidades)
    combobox_localidade.grid(row=4, column=1, padx=5, pady=5)
    tk.Label(janela, text="Tratamento:").grid(row=5, column=0, padx=5, pady=5)
    combobox_tratamento = ttk.Combobox(janela, values=tratamentos)
    combobox_tratamento.grid(row=5, column=1, padx=5, pady=5)
    tk.Label(janela, text="Mês:").grid(row=6, column=0, padx=5, pady=5)
    combobox_mes = ttk.Combobox(janela, values=meses)
    combobox_mes.grid(row=6, column=1, padx=5, pady=5)
    
    # Checkbutton para consentimento
    consentimento_var = tk.BooleanVar() # Variável para o consentimento
    check_consentimento = tk.Checkbutton(janela, text="Consentimento para uso de dados", variable=consentimento_var)
    check_consentimento.grid(row=7, columnspan=2, padx=5, pady=5)
    
    # Botão para salvar os dados
    btn_salvar = tk.Button(
        janela, 
        text="Salvar Dados", 
        command=lambda: salvar_dados(
            db, # Certifique-se de passar o db aqui
            entry_nome.get(), 
            entry_idade.get(), 
            combobox_diagnostico.get(),
            combobox_localidade.get(), 
            combobox_tratamento.get(), 
            combobox_mes.get(),
            consentimento_var.get(),
            datetime.now()  # Adiciona a data de modificação 
        )
    )
    btn_salvar.grid(row=8, columnspan=1, padx=5, pady=5)
    
    # Label para mostrar a mensagem de sucesso
    status_label = tk.Label(janela, text="", fg="green")  # Mensagem de sucesso em verde
    status_label.grid(row=8, column=1, padx=5, pady=5)  # Coluna 2 ao lado do botão
    
    # Botão para gerar relatório PDF
    btn_gerar_relatorio = tk.Button(janela, text="Gerar Relatório PDF", command=gerar_relatorio_pdf)
    btn_gerar_relatorio.grid(row=9, column=0, padx=5, pady=5)  # Posicionado na linha 9, coluna 0
    
    # Botão para gerar gráficos
    btn_graficos = tk.Button(janela, text="Gerar Gráficos", command=mostrar_grafico)
    btn_graficos.grid(row=9, column=1, padx=5, pady=5)
 
 # Iniciar a sincronização em uma thread
    threading.Thread(target=iniciar_sincronizacao, args=(db,), daemon=True).start()
    janela.mainloop()  # Executa a interface gráfica
if __name__ == "__main__":
    db = inicializar_firebase()  # Inicializa o Firebase
    criar_janela_principal(db)  # Cria a janela principal
