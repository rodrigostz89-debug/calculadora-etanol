import streamlit as st
from streamlit.components.v1 import html
import datetime
import os
from cert_generator import preencher_certificado

# Configuração da página
st.set_page_config(page_title='Calculadora de Etanol', layout='centered')

st.title('Sistema de Etanol')
tab1, tab2 = st.tabs(['Calculadora', 'Gerador de Certificado'])

# Inicializar número do certificado no estado da sessão (não mais necessário estritamente aqui, mas mantido para fallback)
if 'num_cert_atual' not in st.session_state:
    st.session_state.num_cert_atual = ''

with tab1:
    st.markdown("Verificação de carregamento em veículos - Peso Líquido, Massa Específica e Volume")

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
    st.subheader("Dados de Entrada")

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

    # JavaScript para foco por Enter e Máscaras de Digitação
    html(r"""
    <script>
        const configs = [
            { maxDigits: 5, decimals: 3 }, // Peso Líquido (ex: 74.000)
            { maxDigits: 6, decimals: 3 }, // Massa Específica 20° (ex: 790.487)
            { maxDigits: 5, decimals: 3 }, // Volume Carregado (ex: 62.000)
            { maxDigits: 5, decimals: 4 }  // Fator de Redução (ex: 0.9946)
        ];

        function setNativeValue(element, value) {
            try {
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                    window.parent.HTMLInputElement.prototype, "value"
                ).set;
                nativeInputValueSetter.call(element, value);
                element.dispatchEvent(new Event('input', { bubbles: true }));
            } catch(e) {
                console.error("Erro ao definir valor no Streamlit:", e);
            }
        }

        function formatMask(value, config) {
            if (!value) return "";
            let digits = value.replace(/\D/g, '');
            if (digits.length === 0) return "";

            // Remove zeros à esquerda, mas mantém pelo menos 1 dígito
            digits = digits.replace(/^0+/, '');
            if (digits === '') digits = '0';

            // Limita o número máximo de dígitos
            if (digits.length > config.maxDigits) {
                digits = digits.slice(0, config.maxDigits);
            }

            // Preenche com zeros à esquerda para garantir as casas decimais
            while (digits.length <= config.decimals) {
                digits = '0' + digits;
            }

            const beforeDot = digits.slice(0, digits.length - config.decimals);
            const afterDot = digits.slice(-config.decimals);

            return beforeDot + '.' + afterDot;
        }

        try {
            const doc = window.parent.document;
            const inputs = doc.querySelectorAll('input[type="text"]');
            if (inputs.length > 0) {
                inputs.forEach((input, index) => {
                    if (index < configs.length) {
                        // Adiciona o listener de máscara (apenas uma vez)
                        if (!input.dataset.masked) {
                            input.dataset.masked = "true";

                            input.addEventListener('input', (e) => {
                                const formatted = formatMask(e.target.value, configs[index]);
                                if (formatted !== e.target.value) {
                                    setNativeValue(input, formatted);
                                }
                            });

                            // Formata valor inicial se existir
                            if (input.value) {
                                const formatted = formatMask(input.value, configs[index]);
                                if (formatted !== input.value) {
                                    setNativeValue(input, formatted);
                                }
                            }
                        }
                    }

                    // Adiciona listener de Enter (apenas uma vez)
                    if (!input.dataset.enterListener) {
                        input.dataset.enterListener = "true";
                        input.addEventListener('keydown', (e) => {
                            if (e.key === 'Enter') {
                                e.preventDefault();
                                if (index < inputs.length - 1) {
                                    inputs[index + 1].focus();
                                } else {
                                    // No último input, clica no botão Calcular
                                    const button = doc.querySelector('button[kind="primary"]');
                                    if (button) button.click();
                                }
                            }
                        });
                    }
                });

                // Foco inicial (uma vez apenas)
                if (!doc.body.dataset.focusSet) {
                     inputs[0].focus();
                     doc.body.dataset.focusSet = "true";
                }
            }
        } catch(e) {
            console.error("Máscaras desativadas devido a restrições de CORS no Streamlit Cloud.", e);
        }
    </script>
    """, height=0)

    # Botão Calcular
    if st.button("CALCULAR", type="primary", use_container_width=True):
        try:
            peso_liquido = float(peso_str) if peso_str else 0.0
            massa_especifica = float(massa_str) if massa_str else 0.0
            volume_carregado = float(volume_str) if volume_str else 0.0
            fator_reducao = float(fator_str) if fator_str else 0.0

            if peso_liquido > 0 and massa_especifica > 0 and volume_carregado >= 0 and fator_reducao > 0:
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
            else:
                st.warning("Preencha todos os campos com valores positivos válidos!")
        except ValueError:
            st.warning("Insira valores numéricos válidos em todos os campos!")


with tab2:
    st.header('Gerador de Certificado de Análise')
    st.write('Preencha os dados abaixo para gerar o documento preenchido.')

    # Funções auxiliares para lidar com arquivos locais
    ARQUIVO_NUM_CERT = 'cert_config.txt'
    TEMPLATE_PADRAO = 'template_padrao.docx'

    def ler_numero_certificado():
        if os.path.exists(ARQUIVO_NUM_CERT):
            try:
                with open(ARQUIVO_NUM_CERT, 'r') as f:
                    return f.read().strip()
            except:
                pass
        return '1'

    def salvar_numero_certificado(num):
        try:
            with open(ARQUIVO_NUM_CERT, 'w') as f:
                f.write(str(num))
        except:
            pass

    st.subheader('1. Modelo do Certificado')
    
    template_file = st.file_uploader('Enviar novo Modelo do Certificado (Word)', type=['docx'])
    
    # Lógica de salvar o template
    if template_file is not None:
        try:
            with open(TEMPLATE_PADRAO, "wb") as f:
                f.write(template_file.getbuffer())
            st.success("Novo modelo salvo com sucesso!")
        except Exception as e:
            st.error(f"Erro ao salvar o modelo: {e}")

    # Verifica se existe um template
    tem_template = os.path.exists(TEMPLATE_PADRAO)
    if tem_template:
        st.info("✅ Um modelo de certificado já está salvo no sistema e será utilizado.")
    else:
        st.warning("⚠️ Nenhum modelo de certificado encontrado. Por favor, envie um modelo acima.")

    st.subheader('2. Dados para Preenchimento')

    # Lê o último número ou '1'
    num_sugerido = ler_numero_certificado()

    col1, col2 = st.columns(2)
    with col1:
        num_cert = st.text_input('Número do Certificado', value=num_sugerido)
        data_cert = st.text_input('Data', value=datetime.datetime.now().strftime('%d/%m/%Y'))
    with col2:
        placa = st.text_input('Placa do Veículo', value='')
        quantidade = st.text_input('Quantidade (Litros)', value='')

    if st.button('Gerar Documento Word', type='primary'):
        if tem_template:
            if num_cert and placa and quantidade:
                try:
                    doc_bytes = preencher_certificado(TEMPLATE_PADRAO, num_cert, placa, quantidade, data_cert)
                    st.success('Certificado gerado com sucesso!')
                    st.download_button(
                        label='Baixar Certificado Preenchido',
                        data=doc_bytes,
                        file_name=f'Certificado_{placa}.docx',
                        mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                    )
                    
                    # Tenta incrementar o número automaticamente e salvar
                    if num_cert.isdigit():
                        proximo_num = int(num_cert) + 1
                        salvar_numero_certificado(proximo_num)
                except Exception as e:
                    st.error(f'Erro ao gerar documento: {e}')
            else:
                faltando = []
                if not num_cert: faltando.append("Número do Certificado")
                if not placa: faltando.append("Placa do Veículo")
                if not quantidade: faltando.append("Quantidade")
                st.warning(f"Falta preencher: {', '.join(faltando)}")
        else:
            st.warning('Por favor, envie o Modelo do Certificado antes de gerar.')

st.markdown('---')
st.caption('Desenvolvido por Rodrigo | Ferramenta para verificação de etanol em veículos')
