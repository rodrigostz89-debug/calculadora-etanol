import streamlit as st
from streamlit.components.v1 import html

# Configuração da página
st.set_page_config(page_title="Calculadora de Etanol", layout="centered")

st.title("Calculadora de Etanol")
st.markdown("Verificação de carregamento em veículos - Peso Líquido, Massa Específica e Volume")

st.markdown("---")

# Inputs com mais precisão e foco por Enter
st.subheader("Dados de Entrada")

col1, col2 = st.columns(2)

with col1:
    peso_liquido = st.number_input("Peso Líquido (kg)", min_value=0.0, step=0.001, format="%.3f", key="peso")
    massa_especifica = st.number_input("Massa Específica 20° (kg/m³)", min_value=0.0, step=0.0001, format="%.4f", key="massa")

with col2:
    volume_carregado = st.number_input("Volume Carregado (L)", min_value=0.0, step=0.001, format="%.3f", key="volume")
    fator_reducao = st.number_input("Fator de Redução", min_value=0.0, max_value=2.0, step=0.0001, format="%.4f", key="fator")

# JavaScript para foco por Enter (pula pro próximo input ou calcula no último)
html("""
<script>
    const inputs = window.parent.document.querySelectorAll('input[type="number"]');
    if (inputs.length > 0) {
        inputs.forEach((input, index) => {
            input.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    if (index < inputs.length - 1) {
                        inputs[index + 1].focus();
                    } else {
                        // No último input, clica no botão Calcular
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
    if peso_liquido > 0 and massa_especifica > 0 and volume_carregado >= 0 and fator_reducao > 0:
        try:
            # Cálculos exatamente iguais ao seu original
            diferenca_litros = (peso_liquido / massa_especifica) * 1000
            volume_real = volume_carregado * fator_reducao
            diferenca_ml = (diferenca_litros - volume_real) * 1000.0
            porcentagem = (diferenca_ml / volume_real) / 10 if volume_real != 0 else 0

            # Exibição dos resultados com formatação igual
            st.subheader("Resultados")
            st.success(f"**Volume Real:** {volume_real:.3f} L")
            st.info(f"**Diferença:** {diferenca_ml:.1f} Lts")
            st.metric("Porcentagem", f"{porcentagem:.2f} %")

            # Avaliação
            if porcentagem >= 0.099 or porcentagem <= -0.299:
                st.error("⚠️ Valor fora da média!")
            else:
                st.success("✅ Valor dentro da média!")

            # Botão reiniciar
            if st.button("Reiniciar"):
                st.rerun()

        except Exception as e:
            st.error(f"Erro nos cálculos: {e}")
    else:
        st.warning("Preencha todos os campos com valores positivos válidos!")

st.markdown("---")
st.caption("Desenvolvido por Rodrigo | Ferramenta para verificação de etanol em veículos")
