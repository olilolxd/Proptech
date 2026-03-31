import streamlit as st
import pandas as pd
import plotly.express as px
import os
from financial_model import calculate_celiapp_benefit, calculate_profitability
from data_extractor import create_fallback_dataset

st.set_page_config(page_title="Proptech Dashboard Montréal", layout="wide")
st.title("🏡 Tableau de Bord Immobilier (Proptech) - Montréal")

# Load data
data_file = "listings_montreal.csv"
if not os.path.exists(data_file):
    with st.spinner("Création du dataset initial..."):
        create_fallback_dataset()

try:
    df = pd.read_csv(data_file)
except:
    st.error("Erreur de lecture du fichier CSV.")
    st.stop()

# Sidebar - User inputs
st.sidebar.header("⚙️ Paramètres de l'Acheteur")
income = st.sidebar.number_input("Revenu Annuel ($)", min_value=30000, value=90000, step=5000)
marginal_tax_rate = st.sidebar.slider("Taux d'imposition marginal estimé", 0.20, 0.55, 0.37)

st.sidebar.subheader("📈 Stratégie CELIAPP")
celiapp_contrib = st.sidebar.number_input("Cotisation Annuelle CELIAPP ($)", min_value=0, max_value=8000, value=8000, step=1000)
years_saving = st.sidebar.slider("Années d'épargne avant achat", 0, 15, 3)

st.sidebar.subheader("💰 Paramètres Hypothécaires")
base_down_payment = st.sidebar.number_input("Mise de fonds initiale hors CELIAPP ($)", min_value=0, value=20000, step=5000)
interest_rate = st.sidebar.slider("Taux d'intérêt annuel (%)", 1.0, 10.0, 4.5, 0.1) / 100
amortization = st.sidebar.selectbox("Amortissement (années)", [15, 20, 25, 30], index=2)

st.sidebar.subheader("🏢 Hypothèses d'exploitation")
est_monthly_rent = st.sidebar.number_input("Loyer Mensuel Estimatif ($)", min_value=0, value=2500, step=100)

# Calculations
celiapp_data = calculate_celiapp_benefit(celiapp_contrib, years_saving, marginal_tax_rate)
total_down_payment = base_down_payment + celiapp_data["total_extra_down_payment"]

st.header(f"💼 Budget de Mise de Fonds totalisé : {total_down_payment:,.2f} $")
col1, col2, col3 = st.columns(3)
col1.metric("Mise de fonds de base", f"{base_down_payment:,.2f} $")
col2.metric("Épargne CELIAPP", f"{celiapp_data['celiapp_total']:,.2f} $")
col3.metric("Remboursement d'impôt réinvesti", f"{celiapp_data['tax_return']:,.2f} $")

st.markdown("---")

# Display Properties
st.subheader("📍 Propriétés Disponibles (Montréal)")
st.dataframe(df)

# Run profitability on the dataset
if not df.empty:
    st.subheader("📊 Analyse de Rentabilité")
    
    # On calcule la rentabilité pour chaque propriété
    def apply_profitability(row):
        # Prevent errors if price is too low to cover down payment
        dp = total_down_payment if total_down_payment < row['Prix'] else row['Prix'] * 0.99
        return calculate_profitability(
            price=row['Prix'],
            down_payment=dp,
            monthly_rent=est_monthly_rent,
            annual_rate=interest_rate,
            amort_years=amortization
        )
    
    results = df.apply(lambda row: apply_profitability(row), axis=1)
    
    df['Mise_de_fonds_Appliquée'] = [total_down_payment if total_down_payment < df.loc[i, 'Prix'] else df.loc[i, 'Prix'] * 0.99 for i in df.index]
    df['Mensualité_Hypothèque'] = [r['monthly_mortgage'] for r in results]
    df['NOI'] = [r['noi'] for r in results]
    df['Cash_Flow_Mensuel'] = [r['monthly_cash_flow'] for r in results]
    df['Cap_Rate_%'] = [r['cap_rate'] for r in results]
    df['Cash_on_Cash_%'] = [r['cash_on_cash'] for r in results]
    
    # Display the financial columns
    disp_cols = ['Adresse', 'Prix', 'Mise_de_fonds_Appliquée', 'Mensualité_Hypothèque', 'Cash_Flow_Mensuel', 'Cap_Rate_%', 'Cash_on_Cash_%']
    st.dataframe(df[disp_cols].style.format({
        'Prix': '{:,.0f} $',
        'Mise_de_fonds_Appliquée': '{:,.0f} $',
        'Mensualité_Hypothèque': '{:,.2f} $',
        'Cash_Flow_Mensuel': '{:,.2f} $',
        'Cap_Rate_%': '{:.2f} %',
        'Cash_on_Cash_%': '{:.2f} %'
    }))
    
    # Plotly Graph
    st.subheader("Comparaison du Cash Flow par Propriété")
    # Wrap addresses for better display on X axis
    df['Adresse_Courte'] = df['Adresse'].apply(lambda x: x.split(',')[0])
    
    fig = px.bar(df, x='Adresse_Courte', y='Cash_Flow_Mensuel', 
                 title="Cash Flow Mensuel (impacté par votre grande mise de fonds CELIAPP)",
                 color='Cash_Flow_Mensuel', color_continuous_scale=px.colors.diverging.RdYlGn,
                 labels={'Adresse_Courte': 'Propriété', 'Cash_Flow_Mensuel': 'Cash Flow Mensuel ($)'})
    
    # adding horizontal line for zero
    fig.add_shape(type="line", x0=-0.5, x1=len(df['Adresse_Courte'])-0.5, y0=0, y1=0,
                  line=dict(color="gray", width=2, dash="dash"))
                  
    st.plotly_chart(fig, use_container_width=True)

    st.info("💡 Note: Le modèle suppose un revenu locatif uniforme pour toutes ces propriétés à titre démonstratif. Utilisez la barre latérale pour ajuster le loyer marché.")
    
st.markdown("---")
st.markdown("*Proptech Dashboard - Développé par Antigravity*")
