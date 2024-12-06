import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime 
import re 
import time
from filelock import FileLock
import os
from mqtt_utilis import activate_irrigation


def main():
    st.title("Bem vindo ao FarmSettings")

    # Lista de itens do menu
    menu_items = ["Cadastrar área", "Alterar área", "Ativar irrigação", "Painel de dados"]

    # Criando o menu na sidebar usando radio buttons
    st.sidebar.title("Menu de Navegação")
    choice = st.sidebar.radio("Selcione", menu_items)

    # Mostrar o conteúdo baseado na escolha do menu
    show_content(choice)

def validade_string(string, string_len = 4):
    # Verifica se o nome tem pelo menos 4 caracteres e contém letras
    if len(string) < string_len or not re.search('[a-zA-Z]', string):
        return False
    return True

def cadastrar_nome_area(value_input=None):
        area_name = st.text_input("Nome da área", value=value_input)
           # Validação do nome da área
        if area_name:
            if not validade_string(area_name):
                st.error("O nome da área deve conter pelo menos 4 caracteres e incluir letras.")
            else:
                return area_name

def show_content(choice):
    area = ["", "Área 1", "Área 2", "Área 3"] 
    estadios = ["", "Germinação", "Desenvolvimento vegetativo", "Floração", "Frutificação", "Maturação"]

    if choice == "Cadastrar área":
        st.header("Cadastrar Área")
        st.write("Aqui você pode cadastrar novas áreas de plantio.")
        
        area_name = cadastrar_nome_area()
        area = st.number_input("Tamanho em hectares", min_value=1, step=100, value=None)
        crop = st.text_input("Cultura")
        planting_date = st.date_input("Data de plantio", max_value=datetime.now().date(),value=None)     
        phenological_stage = st.selectbox("Estádio fenológico", estadios)

        if st.button("Cadastrar"):
        # Validações
            empty_field = False
            if area_name is None or not area_name.strip():
                st.warning("Por favor, insira o nome da área.")
                empty_field = True
            elif area is None:
                st.warning("Por favor, insira um valor válido para a tamanho em hectares.")
                empty_field = True
            elif area_name is None or not crop.strip():
                st.warning("Por favor, insira o nome da cultura.")
                empty_field = True

            if not empty_field:
                st.success(f"Área '{area_name}' cadastrada com sucesso!")
                st.write(f"Tamanho: {area} hectares")
                st.write(f"Cultura: {crop}")
                 # Exibindo campos opcionais apenas se foram preenchidos
                if planting_date is not None:
                    st.write(f"Data de plantio: {planting_date}")
                if phenological_stage is not None:
                    st.write(f"Estádio fenológico: {phenological_stage}")

    elif choice == "Alterar área":
        st.header("Alterar área")
        # Exemplo de campos para alteração
        validacao = 'consulta banco'
        item = st.selectbox("Selecione a área que quer alterar", area)
        if item != "": 
            st.write(f"Campos em branco serão desconsiderados o preenchimento.")
            area_name = cadastrar_nome_area(item)
            #adcionar verificacao se ja existe data de plantio, caso existe nao exibir
            if validacao: 
                planting_date = st.date_input("Data de plantio", max_value=datetime.now().date(),value=None)     
                phenological_stage = st.selectbox("Estádio fenológico", estadios)
            if st.button("Alterar Item"):
                if item != area_name:
                    st.success(f"Nome da área alterado para quantidade {area_name}")
                elif planting_date is not None:
                    st.write(f"Data de plantio: {planting_date}")
                elif phenological_stage is not "":
                    st.write(f"Estádio fenológico: {phenological_stage}")
                else: 
                    st.error("Altere algum campo.")

    elif choice == "Ativar irrigação":
        st.header("Ativar irrigação")
        st.write("Controle de ativação da irrigação.")
        #controle para ativar irrigação
        area = st.selectbox("Selecione a área", area)
        duracao = st.slider("Duração (minutos)", 10, 200, 30)
        if st.button("Ativar Irrigação"):
            try:
                result = activate_irrigation("chanel/1")
                if result:
                    if "Failed" in result:
                        st.error(f"Falha na ativação da irrigação: {result}")
                    else:
                        st.success(f"Irrigação ativada na {area} por {duracao} minutos")
                else:
                        st.warning("A ativação da irrigação não retornou nenhum resultado.")
            except Exception as e:
                st.error(f"Ocorreu um erro ao tentar ativar a irrigação: {str(e)}")            
    elif choice == "Painel de dados":
        
        # Função para carregar os dados
        def load_data():
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            csv_path = os.path.join(root_dir, 'mqtt_data.csv')
            lock_file = csv_path + ".lock"
            
            with FileLock(lock_file):
                if os.path.exists(csv_path):
                    return pd.read_csv(csv_path)
            return None

        # Criar um placeholder para o conteúdo dinâmico
        placeholder = st.empty()

        # Loop principal para atualização contínua
        while True:
            df = load_data()
            
            with placeholder.container():
                if df is not None:
                    st.subheader("Dados em tempo real:")
                    st.dataframe(df)

                #puxar dados históricos
                #     st.text("Estatísticas Básicas:")
                #     st.write(df.describe())

                #     if 'temperature' in df.columns:
                #         st.subheader("Gráfico de Temperatura")
                #         if 'timestamp' in df.columns:
                #             df['timestamp'] = pd.to_datetime(df['timestamp'])
                #             st.line_chart(df.set_index('timestamp')['temperature'])
                #         else:
                #             st.error("Coluna 'timestamp' não encontrada no DataFrame.")
                # else:
                #     st.error("Arquivo CSV não encontrado ou está vazio.")


            time.sleep(5)  # Atualiza a cada 5 segundos


if __name__ == "__main__":
    main()