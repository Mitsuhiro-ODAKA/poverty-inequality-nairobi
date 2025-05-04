import streamlit as st
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

def main():
    # Page config
	st.set_page_config(page_title="Nairobi Spatial Inequality", layout="wide")

	st.title("🌍 Nairobi Spatial Inequality Dashboard")
	st.markdown("""
	This dashboard explores the spatial relationship between **building density**, **relative wealth**, and **infrastructure access** in Nairobi.
	Use the slider below to filter and explore the most vulnerable areas.
	""")

	# --- Load Data ---
	wards = gpd.read_file("data/processed/nairobi_vulnerability_score.shp")
	wards = wards.rename(columns={'buildings_': 'buildings_per_km2', 'dist_to_ra':'dist_to_rail_km','dist_to_wa':'dist_to_water_km','density_ra':'density_rank','vulnerabil':'vulnerability_score'})
	
	# --- Vulnerability Slider ---
	st.sidebar.header("Filter by Vulnerability")
	percentile = st.sidebar.slider("Show top X% most vulnerable wards", 10, 100, 100, step=10)
	threshold = wards["vulnerability_score"].dropna().quantile(1 - percentile/100)
	filtered_wards = wards[wards["vulnerability_score"] >= threshold]

	col1, col2 = st.columns([1, 1.2])  # 2カラムレイアウト

	# --- Vulnerability Map ---
	with col1:
	    st.subheader("Vulnerability Map")
	    m = folium.Map(location=[-1.29, 36.82], zoom_start=11)
	    folium.Choropleth(
	        geo_data=filtered_wards,
	        data=filtered_wards,
	        columns=["ward", "vulnerability_score"],
	        key_on="feature.properties.ward",
	        fill_color="OrRd",
	        fill_opacity=0.7,
	        line_opacity=0.2,
	        legend_name="Vulnerability Score"
	    ).add_to(m)
	    st_folium(m, width=700)

	# --- Pairplot ---
	with col2:
	    st.subheader("Pairplot of Variables")
	    st.markdown("""
	    This plot shows relationships between:
	    - **Wealth (RWI)**
	    - **Building Density**
	    - **Access to Railways and Waterways**
	    """)
	    fig = sns.pairplot(wards[[
	        "mean_rwi", "buildings_per_km2",
	        "dist_to_rail_km", "dist_to_water_km"
	    ]].dropna())
	    st.pyplot(fig)



if __name__=="__main__":
    main()
