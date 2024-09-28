---
O arquivo `README.md`, projeta os avanços no código e na estrutura do projeto:

---

# Projeto de Extensão Universitária - Estácio 2024

## Desenvolvedor: Marcus Cesar Pereira Ferreira  
**Matrícula**: 202102340918  
**Curso**: Projeto de Extensão Universitária - Estácio 2024  
**Disciplina**: Desenvolvimento Rápido de Aplicações em Python

---

## 1. Descrição do Projeto

Este projeto foi desenvolvido para o **Fonart - Espaço Fonoaudiologia Aplicada e Saúde Integral**, CNPJ 19.064.473/0001-80, CNES 7402589, com o objetivo de automatizar o processo de coleta, armazenamento e geração de relatórios de pacientes, incluindo gráficos estatísticos, garantindo conformidade com a **Lei Geral de Proteção de Dados (LGPD)**.

### Funcionalidades principais:
- Cadastro e armazenamento de informações de pacientes em um arquivo CSV.
- Geração automática de relatórios em PDF e Excel, com anonimização de dados pessoais.
- Ferramenta de estatística com projeção da imagem do período da coleta de dados gravados no arquivo CSV.
- Geração de gráficos estatísticos no formato Excel.

---

## 2. Estrutura de Diretórios

A estrutura de pastas do projeto é organizada da seguinte maneira:

```
PROJETO_FONART/
├── assets/                                    # Arquivos de mídia utilizados no projeto
│   ├── fonart4.gif                            # Animação para a interface ou relatórios
│   ├── fonart4.ico                            # Ícone da aplicação ou site
│   └── fonart4.png                            # Logotipo da empresa utilizado na interface
├── dados/
│   ├── Firebase/
│   │   └── fonart-8cd50-fiXXXXXXXXXXXXX.json  # Credenciais para o Firebase
│   ├── pacientes/
│   │   └── pacientes.csv                      # Arquivo CSV contendo os dados dos pacientes
│   └── relatorios/
│       ├── grafico.png                        # Gráfico gerado a partir dos dados de pacientes
│       ├── pacientes.xlsx                     # Dados dos pacientes em formato Excel
│       └── relatorio_pacientes.pdf            # Relatório em PDF gerado a partir dos dados
├── fonart-web/                                # Arquivos para a interface web (se aplicável)
│   ├── fonart.matriz.png                      # Logotipo utilizado na versão web
│   ├── fonovinho.png                          # Imagem utilizada na interface web
│   ├── index.html                             # Página inicial da interface web
│   └── qualidade.html                         # Página relacionada à qualidade do serviço ou produto
├── logs/
│   └── system.log                             # Arquivo de log com registros de eventos do sistema
├── node_modules/                              # Dependências do projeto (Node.js)
├── venv/                                      # Ambiente virtual do Python
├── .firebaserc                                # Arquivo de configuração do Firebase CLI
├── .gitignore                                 # Arquivo para ignorar determinados arquivos no Git
├── firebase login                             # Script ou arquivo de configuração para login no Firebase
├── firebase_setup.py                          # Script de configuração do Firebase
├── firebase.json                              # Arquivo de configuração do Firebase
├── README.md                                  # Arquivo de documentação do projeto
├── requirements.txt                           # Lista de dependências do Python necessárias ao projeto
---

## 3. Configuração e Execução

### Pré-requisitos:
- **Python 3.x** instalado.
- Bibliotecas necessárias:
  - `pandas`
  - `tkinter`
  - `reportlab`
  - `xlsxwriter`

Você pode instalar todas as dependências necessárias executando o seguinte comando:

```bash
pip install pandas reportlab xlsxwriter
```

### Como executar o sistema:
1. **Clone ou baixe o projeto** para seu diretório local.
2. **Navegue até a pasta do projeto**:
   ```bash
   cd C:\Projeto_Estacio_2024-Fono\Projeto_Fonart
   ```
3. **Execute o arquivo principal**:
   ```bash
   python sistema_fonart.py
   ```

---

## 4. Funcionalidades

### 4.1. Cadastro de Pacientes
- A interface permite cadastrar os seguintes dados de pacientes:
  - Nome
  - Idade
  - Diagnóstico
  - Localidade
  - Tratamento
  - Consentimento de uso de dados

### 4.2. Geração de Relatórios PDF
- O sistema gera um **relatório em PDF** dos pacientes cadastrados, com anonimização do nome para atender às exigências de privacidade da LGPD.
- O relatório é salvo na pasta `dados/relatorios/`.


### 4.4. Projeção das Estatísticas
- A ferramenta permite gerar a imagem do gráfico atualizado de dados consolidados por localidade dos pacientes, sem identificação de nomes.

---

## 5. Conformidade com a LGPD

- O sistema incorpora medidas para garantir a privacidade dos pacientes:
- Antes de qualquer acesso a dados pessoais, uma mensagem de alerta é exibida para lembrar o operador sobre as responsabilidades da proteção de dados.
- Nomes de pacientes são anonimizados em relatórios PDF e Excel.
- O uso dos dados pessoais só ocorre mediante o consentimento informado do paciente.

---

## 6. Exemplo de Uso

- 

## 7. Contato

Em caso de dúvidas ou sugestões, entre em contato:

- **Marcus Cesar Pereira Ferreira**  
- **Email**: 202102340918@alunos.estacio.br, marcus.cesar@outlook.com ou mcferreira@wert-sc.com.br

---

## 7. Licença

Este projeto está sob a licença [inserir tipo de licença aqui]. 

---

### Notas Finais
Este projeto faz parte do **Projeto de Extensão Universitária - Estácio 2024**, com foco na aplicação prática de automação em fonoaudiologia e conformidade com a legislação vigente, utilizando a Disciplina - **Desenvolvimento Rápido de Aplicações em Python**

---