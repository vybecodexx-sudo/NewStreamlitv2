import streamlit as st
import pandas as pd
from collections import Counter

# 1. Configuração da página (Visual Profissional)
st.set_page_config(page_title="Dashboard de Levantamento", layout="wide")

st.title("Análise de Levantamento de Infraestrutura")
st.write("Visão simplificada dos dados de localização e distribuição de equipamentos.")
st.markdown("---")

# 2. Upload de arquivos
uploaded_file = st.file_uploader("Selecione a planilha de Levantamento (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    # Lendo as abas do arquivo
    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names
    
    col1, col2 = st.columns([1, 3])
    with col1:
        selected_sheet = st.selectbox("Selecione a Aba", sheet_names)
    
    df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
    
    # 3. Criando abas de navegação para separar os dados do gráfico
    tab1, tab2 = st.tabs(["Visão Gráfica (Apresentação)", "Tabela Bruta (Consulta)"])
    
    with tab1:
        st.subheader("Concentração de Equipamentos por Local")
        st.write("Frequência de componentes distribuídos pelas instalações (Armários, Locações, Interfaces, etc).")
        
        # Lógica para simplificar a leitura: varre toda a planilha em busca de locais de instalação
        all_values = df.astype(str).values.flatten()
        termos_chave = ['Locação', 'Armário', 'Armario', 'Interface', 'Sinaleiro']
        
        valores_filtrados = []
        for valor in all_values:
            valor_str = str(valor).strip()
            # Filtra apenas as células que contêm os termos relevantes e exclui vazios
            if any(termo.lower() in valor_str.lower() for termo in termos_chave) and valor_str.lower() != 'nan':
                # Padronização de nomenclatura
                if 'armario' in valor_str.lower() or 'armário' in valor_str.lower():
                    valores_filtrados.append('Armários TB')
                else:
                    valores_filtrados.append(valor_str)
                    
        # Contagem e seleção dos 10 locais com mais itens
        contagem = Counter(valores_filtrados)
        top_10 = contagem.most_common(10)
        
        if top_10:
            # Preparação dos dados para o gráfico do Streamlit
            df_grafico = pd.DataFrame(top_10, columns=['Local de Instalação', 'Volume de Componentes'])
            df_grafico.set_index('Local de Instalação', inplace=True)
            
            # Gráfico de barras nativo, com design limpo e responsivo
            st.bar_chart(df_grafico)
            
            st.info("**Ponto de Foco para a Apresentação:** Este gráfico ilustra onde está o maior adensamento de hardware. Utilize-o para demonstrar rapidamente as áreas que demandam mais infraestrutura ou manutenção, sem precisar explicar as nomenclaturas técnicas individuais de cada porta ou cabo.")
        else:
            st.warning("Não foram encontrados dados de localização suficientes nesta aba para gerar o gráfico.")

    with tab2:
        st.subheader("Amostra dos Dados Originais")
        st.write("Visualização das primeiras linhas do documento para auditoria rápida.")
        # Limpa colunas e linhas 100% vazias para melhorar a leitura na tela
        df_clean = df.dropna(how='all', axis=1).dropna(how='all', axis=0)
        st.dataframe(df_clean.head(15), use_container_width=True)
