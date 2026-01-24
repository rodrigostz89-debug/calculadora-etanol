import streamlit as st
from streamlit.components.v1 import html

# Configuração da página
st.set_page_config(page_title="Calculadora de Etanol", layout="centered")

st.title("Calculadora de Etanol")
st.markdown("Verificação de carregamento em veículos - Peso Líquido, Massa Específica e Volume")
st.markdown("---")

# Inicializa session_state se necessário (para reset funcionar desde o início)
if "peso" not in st.session_state:
    st.session_state.peso = ""
if "massa" not in st.session_state:
    st.session_state.massa = ""
if "volume" not in st.session_state:
    st.session_state.volume = ""
if "fator" not in st.session_state:
    st.session_state.fator = ""

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

# Inputs usando session_state para controle de valor
st.subheader("Dados de Entrada")
col1, col2 = st.columns(2)

with col1:
    peso_str = st.text_input("Peso Líquido (kg)",
                             value=st.session_state.peso,
                             key="peso")
    if peso_str and not validar_entrada(peso_str):
        st.warning("Valor inválido no Peso Líquido!")

    massa_str = st.text_input("Massa Específica 20° (kg/m³)",
                              value=st.session_state.massa,
                              key="massa")
    if massa_str and not validar_entrada(massa_str):
        st.warning("Valor inválido na Massa Específica!")

with col2:
    volume_str = st.text_input("Volume Carregado (L)",
                               value=st.session_state.volume,
                               key="volume")
    if volume_str and not validar_entrada(volume_str):
        st.warning("Valor inválido no Volume Carregado!")

    fator_str = st.text_input("Fator de Redução",
                              value=st.session_state.fator,
                              key="fator")
    if fator_str and not validar_entrada(fator_str):
        st.warning("Valor inválido no Fator de Redução!")

# JavaScript para foco por Enter (pula pro próximo ou calcula no último)
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
        // Foco inicial no primeiro input
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

            # Exibição dos resultados
            st.subheader("Resultados")
            st.success(f"**Volume Real:** {volume_real:.3f} L")
            st.info(f"**Diferença:** {diferenca_ml:.1f} mL")  # Ajustei unidade para mL por clareza
            st.metric("Porcentagem", f"{porcentagem:.2f} %")

            # Avaliação
            if porcentagem >= 0.099 or porcentagem <= -0.299:
                st.error("⚠️ Valor fora da média!")
            else:
                st.success("✅ Valor dentro da média!")

            # Botão Reiniciar (azul)
            if st.button("Reiniciar", type="primary", use_container_width=True):
                # Zera os campos no session_state
                st.session_state.peso = ""
                st.session_state.massa = ""
                st.session_state.volume = ""
                st.session_state.fator = ""
                st.rerun()

        else:
            st.warning("Preencha todos os campos com valores positivos válidos!")

    except ValueError:
        st.warning("Insira valores numéricos válidos em todos os campos!")

st.markdown("---")
st.caption("Desenvolvido por Rodrigo | Ferramenta para verificação de etanol em veículos")
