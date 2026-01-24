import streamlit as st
from streamlit.components.v1 import html

# Configuração da página com layout compacto
st.set_page_config(page_title="Calculadora de Etanol", layout="centered")

# CSS para tema escuro com contraste melhorado
st.markdown("""
    <style>
        /* Tema escuro geral */
        .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        
        /* Inputs e labels */
        label {
            color: #FFFFFF !important;
        }
        .stTextInput > div > div > input {
            background-color: #333333 !important;
            border: 1px solid #555555;
            color: #FFFFFF !important;
        }
        
        /* Estilo para inputs desabilitados (resultados) */
        .stTextInput > div > div > input:disabled {
            background-color: #2D2D2D !important;
            border: 1px solid #444444 !important;
            color: #E0E0E0 !important;
            font-weight: bold !important;
            font-size: 16px !important;
        }
        
        /* Botões primary (Calcular) */
        button[kind="primary"] {
            background-color: #0077B6;
            color: #FFFFFF;
        }
        button[kind="primary"]:hover {
            background-color: #005F8F;
        }
        
        /* Botões secundários (Reiniciar) */
        button:not([kind="primary"]) {
            background-color: #0077B6 !important;
            color: #FFFFFF !important;
        }
        button:not([kind="primary"]):hover {
            background-color: #005F8F !important;
        }
        
        /* Alertas e métricas com cores mais visíveis */
        div.stAlert > div {
            background-color: #333333 !important;
            color: #FFFFFF !important;
            border: 1px solid #444444 !important;
        }
        
        /* Cores específicas para mensagens de sucesso e erro */
        div[data-testid="stSuccess"] > div {
            background-color: #1B4332 !important;
            border: 1px solid #2D6A4F !important;
            color: #D8F3DC !important;
        }
        
        div[data-testid="stError"] > div {
            background-color: #5A1A1A !important;
            border: 1px solid #7B2C2C !important;
            color: #FFB3B3 !important;
        }
        
        div[data-testid="stWarning"] > div {
            background-color: #5C4B1A !important;
            border: 1px solid #7D6B2C !important;
            color: #FFF3B3 !important;
        }
        
        /* Reduz padding global */
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        
        /* Reduz espaço entre elementos */
        .stMarkdown, .stSubheader, .stAlert, .stTextInput {
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Estilo para os títulos dos resultados */
        .result-label {
            color: #CCCCCC !important;
            font-size: 14px !important;
            margin-bottom: 0.2rem !important;
        }
        
        /* Container para os resultados */
        .result-container {
            background-color: #2A2A2A;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            border: 1px solid #444444;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Calculadora de Etanol")
st.markdown("Verificação de carregamento em veículos - Peso Líquido, Massa Específica e Volume", unsafe_allow_html=True)

st.markdown("---")

# Função de validação
def validar_entrada(texto):
    if texto == "":
        return True
    if texto.count('.') > 1:
        return False
    try:
        float(texto)
        return True
    except ValueError:
        return False

# Inputs como text_input para começar vazios
col1, col2 = st.columns(2)

with col1:
    peso_str = st.text_input("Peso Líquido (kg)", value="", key="peso")
    if peso_str and not validar_entrada(peso_str):
        st.warning("Valor inválido no Peso Líquido!")
    massa_str = st.text_input("Massa Específica 20° (kg/m³)", value="", key="massa")
    if massa_str and not validar_entrada(massa_str):
        st.warning("Valor inválido na Massa Específica!")

with col2:
    volume_str = st.text_input("Volume Carregado (L)", value="", key="volume")
    if volume_str and not validar_entrada(volume_str):
        st.warning("Valor inválido no Volume Carregado!")
    fator_str = st.text_input("Fator de Redução", value="", key="fator")
    if fator_str and not validar_entrada(fator_str):
        st.warning("Valor inválido no Fator de Redução!")

# JavaScript para foco por Enter
html("""
<script>
    const inputs = window.parent.document.querySelectorAll('input[type="text"]');
    if (inputs.length > 0) {
        inputs.forEach((input, index) => {
            input.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    if (index < inputs.length - 1) {
                        inputs[index + 1].focus();
                    } else {
                        const button = window.parent.document.querySelector('button[kind="primary"]');
                        if (button) button.click();
                    }
                }
            });
        });
        inputs[0].focus();
    }
</script>
""")

# Botão Calcular
if st.button("CALCULAR", type="primary", use_container_width=True):
    try:
        peso_liquido = float(peso_str) if peso_str else 0.0
        massa_especifica = float(massa_str) if massa_str else 0.0
        volume_carregado = float(volume_str) if volume_str else 0.0
        fator_reducao = float(fator_str) if fator_str else 0.0

        if peso_liquido > 0 and massa_especifica > 0 and volume_carregado >= 0 and fator_reducao > 0:
            # Cálculos
            diferenca_litros = (peso_liquido / massa_especifica) * 1000
            volume_real = volume_carregado * fator_reducao
            diferenca_ml = (diferenca_litros - volume_real) * 1000.0
            porcentagem = (diferenca_ml / volume_real) / 10 if volume_real != 0 else 0

            # Container para resultados com estilo melhorado
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            st.markdown("### 📊 Resultados")
            
            # Resultados em colunas
            col3, col4 = st.columns(2)
            
            with col3:
                # Volume Real
                st.markdown('<div class="result-label">Volume Real</div>', unsafe_allow_html=True)
                st.text_input(
                    "Volume Real", 
                    value=f"{volume_real:.3f} L", 
                    disabled=True,
                    key="result_volume",
                    label_visibility="collapsed"
                )
                
                # Diferença (Lts)
                st.markdown('<div class="result-label">Diferença (Lts)</div>', unsafe_allow_html=True)
                st.text_input(
                    "Diferença (Lts)", 
                    value=f"{diferenca_ml:.1f} Lts", 
                    disabled=True,
                    key="result_diferenca",
                    label_visibility="collapsed"
                )
            
            with col4:
                # Porcentagem
                st.markdown('<div class="result-label">Porcentagem</div>', unsafe_allow_html=True)
                st.text_input(
                    "Porcentagem", 
                    value=f"{porcentagem:.2f} %", 
                    disabled=True,
                    key="result_porcentagem",
                    label_visibility="collapsed"
                )
            
            # Avaliação
            st.markdown("### 📈 Avaliação")
            if porcentagem >= 0.099 or porcentagem <= -0.299:
                st.error("⚠️ **VALOR FORA DA MÉDIA!** - Verificar medições")
            else:
                st.success("✅ **VALOR DENTRO DA MÉDIA!** - Medições OK")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Botão reiniciar
            if st.button("🔄 Reiniciar Cálculo", use_container_width=True):
                st.rerun()
        else:
            st.warning("⚠️ Preencha todos os campos com valores positivos válidos!")
    except ValueError:
        st.warning("⚠️ Insira valores numéricos válidos em todos os campos!")

st.markdown("---")
st.caption("Desenvolvido por Rodrigo | Ferramenta para verificação de etanol em veículos")
