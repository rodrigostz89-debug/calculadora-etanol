import streamlit as st

# Configuração da página
st.set_page_config(page_title="Calculadora de Etanol", layout="centered")

st.title("Calculadora de Etanol")
st.markdown("Verificação de carregamento em veículos - Peso Líquido, Massa Específica e Volume")

st.markdown("---")

# Inputs
st.subheader("Dados de Entrada")

col1, col2 = st.columns(2)

with col1:
    peso_liquido = st.number_input("Peso Líquido (kg)", min_value=0.0, step=0.001, format="%.3f")
    massa_especifica = st.number_input("Massa Específica 20° (g/cm³)", min_value=0.0, step=0.0001, format="%.4f")

with col2:
    volume_carregado = st.number_input("Volume Carregado (L)", min_value=0.0, step=0.1, format="%.1f")
    fator_reducao = st.number_input("Fator de Redução", min_value=0.0, max_value=2.0, step=0.001, format="%.3f")

# Botão Calcular
if st.button("CALCULAR", type="primary", use_container_width=True):
    if peso_liquido > 0 and massa_especifica > 0 and volume_carregado >= 0 and fator_reducao > 0:
        try:
            # Cálculos (lógica igual ao seu Tkinter, com correção na ordem da diferença)
            volume_real = (peso_liquido / massa_especifica) * 1000
            diferenca_litros = volume_carregado * fator_reducao
            diferenca_ml = (volume_real - diferenca_litros) * 1000.0
            porcentagem = (diferenca_ml / volume_real) / 10 if volume_real != 0 else 0

            # Exibição dos resultados
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
