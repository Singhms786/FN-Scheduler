
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Furnace Plate Optimizer", layout="centered")

st.title("🔥 Furnace Plate Optimizer")
st.markdown("Upload your plate data, choose a furnace, and get the optimal set of plates to maximize utilization.")

# Upload file
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    st.subheader("Plate Data Preview")
    st.dataframe(df.head())

    # Select Furnace
    furnace_option = st.radio("Select Furnace", ("Furnace 1 (100 MT)", "Furnace 2 (200 MT)"))
    capacity = 100 if "1" in furnace_option else 200
    st.write(f"🔧 Selected Capacity: {capacity} MT")

    if st.button("Optimize Plate Selection"):
        df_sorted = df.sort_values(by="Plate Weight", ascending=False).copy()
        df_sorted["Cumulative_Weight"] = df_sorted["Plate Weight"].cumsum()
        selected_plates = df_sorted[df_sorted["Cumulative_Weight"] <= capacity].copy()
        total_weight = selected_plates["Plate Weight"].sum()

        selected_plates.drop(columns=["Cumulative_Weight"], inplace=True)
        selected_plates.reset_index(drop=True, inplace=True)

        st.success(f"✅ Selected {len(selected_plates)} plates totaling {total_weight:.2f} MT (out of {capacity} MT).")
        st.dataframe(selected_plates)

        # Prepare Excel to download
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            selected_plates.to_excel(writer, index=False, sheet_name='Selected Plates')
        output.seek(0)

        st.download_button(
            label="📥 Download Result as Excel",
            data=output,
            file_name=f"Furnace_{'1' if capacity==100 else '2'}_Selected_Plates.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
