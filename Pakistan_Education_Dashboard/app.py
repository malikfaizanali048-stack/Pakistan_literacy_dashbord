# app.py
import os
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    layout="wide", 
    page_title="Pakistan Education Dashboard",
    page_icon="🇵🇰",
    initial_sidebar_state="expanded"
)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# --------- Helpers to load or create sample data ----------
def generate_sample_literacy():
    years = list(range(2008, 2025))
    provinces = ["Punjab", "Sindh", "Khyber Pakhtunkhwa", "Balochistan", "Gilgit-Baltistan", "AJK", "Islamabad"]
    rows = []
    for y in years:
        for p in provinces:
            male = max(40, min(90, np.random.normal(70 - (2024 - y) * 0.2 + np.random.uniform(-3,3), 5)))
            female = max(25, min(85, male - np.random.uniform(2,12)))
            overall = (male + female) / 2
            rows.append({"year": y, "province": p, "male_literacy": round(male,1),
                         "female_literacy": round(female,1), "overall_literacy": round(overall,1)})
    return pd.DataFrame(rows)

def generate_sample_enrollment():
    years = list(range(2015, 2025))
    provinces = ["Punjab", "Sindh", "Khyber Pakhtunkhwa", "Balochistan", "Gilgit-Baltistan", "AJK", "Islamabad"]
    levels = ["primary", "middle", "secondary", "higher"]
    rows = []
    for y in years:
        for p in provinces:
            base = np.random.randint(300000, 3000000) if p=="Punjab" else np.random.randint(50000, 800000)
            for lvl in levels:
                fluc = int(base * np.random.uniform(0.6, 1.4) * (1 - (levels.index(lvl) * 0.15)))
                rows.append({"year": y, "province": p, "level": lvl, "enrollment": fluc})
    return pd.DataFrame(rows)

def generate_sample_school_perf():
    years = [2019, 2020, 2021, 2022, 2023]
    districts = [f"District {i}" for i in range(1, 65)]
    provinces = ["Punjab", "Sindh", "Khyber Pakhtunkhwa", "Balochistan"]
    rows = []
    for y in years:
        for d in districts:
            prov = np.random.choice(provinces)
            avg = max(25, min(95, np.random.normal(60 + (years.index(y)-2)*1.5, 12)))
            passr = round(np.clip(np.random.normal(0.7 + (avg-60)/200, 0.12), 0.2, 0.99), 2)
            students = int(np.random.uniform(500, 20000))
            rows.append({"year": y, "district": d, "province": prov, "avg_score": round(avg,1),
                         "pass_rate": passr, "num_students": students})
    return pd.DataFrame(rows)

@st.cache_data
def load_or_create_data():
    # Try to load literacy.csv
    literacy_path = DATA_DIR / "literacy.csv"
    enrollment_path = DATA_DIR / "enrollment.csv"
    perf_path = DATA_DIR / "school_performance.csv"

    if literacy_path.exists():
        try:
            literacy = pd.read_csv(literacy_path)
        except Exception as e:
            st.warning(f"Error reading {literacy_path}: {e}. Using generated sample literacy data.")
            literacy = generate_sample_literacy()
    else:
        literacy = generate_sample_literacy()
        literacy.to_csv(literacy_path, index=False)

    if enrollment_path.exists():
        try:
            enrollment = pd.read_csv(enrollment_path)
        except Exception as e:
            st.warning(f"Error reading {enrollment_path}: {e}. Using generated sample enrollment data.")
            enrollment = generate_sample_enrollment()
    else:
        enrollment = generate_sample_enrollment()
        enrollment.to_csv(enrollment_path, index=False)

    if perf_path.exists():
        try:
            perf = pd.read_csv(perf_path)
        except Exception as e:
            st.warning(f"Error reading {perf_path}: {e}. Using generated sample school performance data.")
            perf = generate_sample_school_perf()
    else:
        perf = generate_sample_school_perf()
        perf.to_csv(perf_path, index=False)

    # Normalize column names to lower-case for robustness
    literacy.columns = [c.strip().lower() for c in literacy.columns]
    enrollment.columns = [c.strip().lower() for c in enrollment.columns]
    perf.columns = [c.strip().lower() for c in perf.columns]

    return literacy, enrollment, perf

# Load data
literacy_df, enrollment_df, perf_df = load_or_create_data()

# --------- Custom CSS for better styling ----------
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #01411C 0%, #01411C 33%, white 33%, white 66%, #01411C 66%, #01411C 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        color: white;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        margin: 0;
        font-size: 2.5rem;
    }
    .main-header p {
        color: #f0f0f0;
        margin: 0.5rem 0 0 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stPlotlyChart {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    h2 {
        color: #01411C;
        border-bottom: 3px solid #01411C;
        padding-bottom: 0.5rem;
    }
    h3 {
        color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

# --------- Sidebar: filters ----------
st.sidebar.markdown("## 🎛️ Dashboard Controls")
st.sidebar.markdown("---")

years_available = sorted(literacy_df['year'].unique())
year_sel = st.sidebar.selectbox("📅 Select Year", options=years_available[::-1], index=0)

st.sidebar.markdown("---")
province_choices = sorted(literacy_df['province'].unique())
province_sel = st.sidebar.multiselect(
    "🗺️ Filter Provinces", 
    options=province_choices, 
    default=province_choices,
    help="Leave empty to show all provinces"
)

st.sidebar.markdown("---")
min_students = st.sidebar.slider(
    "👥 Minimum District Students", 
    min_value=0, 
    max_value=int(perf_df['num_students'].max()), 
    value=500,
    help="Filter districts by minimum student count"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** Use filters to explore specific provinces and years. Download data at the bottom of the page!")

# Main layout
st.markdown("""
<div class="main-header">
    <h1>🇵🇰 Pakistan Education Insights Dashboard</h1>
    <p>Comprehensive analysis of literacy trends, gender gaps, enrollment statistics, and district performance across Pakistan</p>
</div>
""", unsafe_allow_html=True)

# Row: literacy trend + gender gap
st.markdown("## 📊 Literacy Analysis")
col1, col2 = st.columns([2,1])

with col1:
    st.markdown("### 📈 National Literacy Trend")
    # compute national mean per year if overall_literacy present else compute average of male/female
    if 'overall_literacy' in literacy_df.columns:
        trend = literacy_df.groupby('year')['overall_literacy'].mean().reset_index()
    else:
        # fallback
        literacy_df['overall_literacy'] = (literacy_df.get('male_literacy',0) + literacy_df.get('female_literacy',0)) / 2
        trend = literacy_df.groupby('year')['overall_literacy'].mean().reset_index()

    fig_trend = px.line(trend, x='year', y='overall_literacy', markers=True,
                        title="Mean Overall Literacy Rate (National Average)")
    fig_trend.update_traces(line=dict(color='#01411C', width=3), marker=dict(size=8))
    fig_trend.update_layout(
        yaxis_title="Literacy Rate (%)", 
        xaxis=dict(dtick=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        hovermode='x unified'
    )
    fig_trend.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig_trend.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown(f"### 🗺️ Province Comparison — {year_sel}")
    comp = literacy_df[literacy_df['year'] == year_sel]
    if province_sel:
        comp = comp[comp['province'].isin(province_sel)]
    if comp.empty:
        st.info("📭 No data available for selected filters.")
    else:
        fig_prov = px.bar(comp.sort_values('overall_literacy'), 
                          x='overall_literacy', y='province', orientation='h',
                          labels={'overall_literacy': 'Overall Literacy (%)', 'province': 'Province'},
                          title=f"Overall Literacy by Province — {year_sel}",
                          color='overall_literacy',
                          color_continuous_scale='Viridis')
        fig_prov.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        st.plotly_chart(fig_prov, use_container_width=True)

with col2:
    st.markdown("### 👫 Gender Gap Analysis")
    if 'male_literacy' in literacy_df.columns and 'female_literacy' in literacy_df.columns:
        # show area chart for male vs female over time (national average)
        gg = literacy_df.groupby('year')[['male_literacy', 'female_literacy']].mean().reset_index()
        fig_gap = go.Figure()
        fig_gap.add_trace(go.Scatter(
            x=gg['year'], y=gg['male_literacy'], 
            mode='lines+markers', name='Male',
            line=dict(color='#3498db', width=3),
            marker=dict(size=6)
        ))
        fig_gap.add_trace(go.Scatter(
            x=gg['year'], y=gg['female_literacy'], 
            mode='lines+markers', name='Female',
            line=dict(color='#e74c3c', width=3),
            marker=dict(size=6)
        ))
        fig_gap.update_layout(
            title="Male vs Female Literacy Rate (National Average)", 
            yaxis_title="Literacy Rate (%)", 
            xaxis=dict(dtick=2),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        fig_gap.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig_gap.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        st.plotly_chart(fig_gap, use_container_width=True)
        
        # show numeric gap for selected year
        sel = literacy_df[literacy_df['year'] == year_sel]
        if not sel.empty:
            ag = sel[['province','male_literacy','female_literacy']].copy()
            ag['gap'] = ag['male_literacy'] - ag['female_literacy']
            avg_gap = ag['gap'].mean()
            st.metric(
                "Gender Gap", 
                f"{avg_gap:.1f}%",
                delta=f"Male - Female ({year_sel})",
                help="Positive value indicates higher male literacy"
            )
    else:
        st.info("📊 Gender-specific data not available in literacy dataset.")

# Enrollment by province (stacked) — for selected year
st.markdown("---")
st.markdown("## 🎓 Enrollment Statistics")
st.markdown(f"### Student Enrollment by Province & Level — {year_sel}")
en_snap = enrollment_df[enrollment_df['year'] == year_sel]
if province_sel:
    en_snap = en_snap[en_snap['province'].isin(province_sel)]
if en_snap.empty:
    st.info("📭 No enrollment data available for these filters.")
else:
    # aggregate and pivot for stacked bar
    en_pivot = en_snap.groupby(['province','level'])['enrollment'].sum().reset_index()
    fig_en = px.bar(en_pivot, x='province', y='enrollment', color='level', 
                    title=f"Enrollment by Province and Education Level — {year_sel}",
                    labels={'enrollment':'Number of Students', 'province':'Province', 'level':'Education Level'},
                    color_discrete_map={
                        'primary': '#3498db',
                        'middle': '#2ecc71',
                        'secondary': '#f39c12',
                        'higher': '#9b59b6'
                    })
    fig_en.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        barmode='stack',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    st.plotly_chart(fig_en, use_container_width=True)
    
    # Add summary statistics
    col1, col2, col3, col4 = st.columns(4)
    total_enrollment = en_snap['enrollment'].sum()
    with col1:
        st.metric("📚 Total Enrollment", f"{total_enrollment:,}")
    with col2:
        primary_pct = (en_snap[en_snap['level']=='primary']['enrollment'].sum() / total_enrollment * 100) if total_enrollment > 0 else 0
        st.metric("🎒 Primary Level", f"{primary_pct:.1f}%")
    with col3:
        provinces_count = en_snap['province'].nunique()
        st.metric("🗺️ Provinces", f"{provinces_count}")
    with col4:
        avg_per_province = total_enrollment / provinces_count if provinces_count > 0 else 0
        st.metric("📊 Avg per Province", f"{avg_per_province:,.0f}")

# District performance: top and bottom
st.markdown("---")
st.markdown("## 🏆 District Performance Rankings")
st.markdown(f"### Top & Bottom Performing Districts — {year_sel}")
perf_snap = perf_df.copy()
# prefer using 'year' filter if perf has same years; otherwise show latest
if 'year' in perf_snap.columns and year_sel in perf_snap['year'].unique():
    perf_snap = perf_snap[perf_snap['year'] == year_sel]
else:
    # use latest available
    latest_perf_year = perf_snap['year'].max()
    perf_snap = perf_snap[perf_snap['year'] == latest_perf_year]
    st.caption(f"ℹ️ Note: Performance data uses year {latest_perf_year} (closest available to selected year).")

# apply province filter
if province_sel:
    perf_snap = perf_snap[perf_snap['province'].isin(province_sel)]
# apply min students
perf_snap = perf_snap[perf_snap['num_students'] >= min_students]

if perf_snap.empty:
    st.warning("⚠️ No district performance data available after applying filters. Try adjusting the filters.")
else:
    sorted_perf = perf_snap.sort_values('avg_score', ascending=False)
    top10 = sorted_perf.head(10)
    bottom10 = sorted_perf.tail(10).sort_values('avg_score')
    
    col_top, col_bot = st.columns(2)
    
    with col_top:
        st.markdown("#### 🥇 Top 10 Districts")
        fig_top = px.bar(top10, x='avg_score', y='district', orientation='h', 
                         labels={'avg_score':'Average Score','district':'District'},
                         title="Top 10 Districts by Average Score",
                         color='avg_score',
                         color_continuous_scale='Greens')
        fig_top.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            yaxis={'categoryorder':'total ascending'}
        )
        st.plotly_chart(fig_top, use_container_width=True)
        
        # Show top district details
        best_district = top10.iloc[0]
        st.success(f"🌟 **Best:** {best_district['district']} ({best_district['province']}) - Score: {best_district['avg_score']}")
        
    with col_bot:
        st.markdown("#### 📉 Bottom 10 Districts")
        fig_bot = px.bar(bottom10, x='avg_score', y='district', orientation='h', 
                         labels={'avg_score':'Average Score','district':'District'},
                         title="Bottom 10 Districts by Average Score",
                         color='avg_score',
                         color_continuous_scale='Reds')
        fig_bot.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            yaxis={'categoryorder':'total ascending'}
        )
        st.plotly_chart(fig_bot, use_container_width=True)
        
        # Show worst district details
        worst_district = bottom10.iloc[0]
        st.error(f"⚠️ **Needs Attention:** {worst_district['district']} ({worst_district['province']}) - Score: {worst_district['avg_score']}")
    
    # Overall statistics
    st.markdown("### 📊 Overall Performance Statistics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📈 Avg Score", f"{perf_snap['avg_score'].mean():.1f}")
    with col2:
        st.metric("✅ Avg Pass Rate", f"{perf_snap['pass_rate'].mean()*100:.1f}%")
    with col3:
        st.metric("👥 Total Students", f"{perf_snap['num_students'].sum():,}")
    with col4:
        st.metric("🏫 Districts", f"{perf_snap['district'].nunique()}")

# Download buttons and simple analysis outputs
st.markdown("---")
st.markdown("## 📥 Data Export & Summary")

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("📅 Literacy Years Range", f"{min(literacy_df['year'])} – {max(literacy_df['year'])}")
with col_b:
    st.metric("📊 Enrollment Records", f"{len(enrollment_df):,}")
with col_c:
    st.metric("🏫 District Records", f"{len(perf_df):,}")

# Allow export of filtered data to CSV
st.markdown("### 💾 Download Filtered Datasets")
st.markdown("Export your filtered data for further analysis in Excel, Python, or other tools.")

dlcol1, dlcol2, dlcol3 = st.columns(3)

def to_csv_download(df):
    return df.to_csv(index=False).encode('utf-8')

with dlcol1:
    filtered_literacy = literacy_df[literacy_df['province'].isin(province_sel)] if province_sel else literacy_df
    st.download_button(
        "📊 Download Literacy Data", 
        to_csv_download(filtered_literacy), 
        file_name=f"literacy_filtered_{year_sel}.csv",
        mime="text/csv",
        help="Download literacy data with current filters applied"
    )

with dlcol2:
    filtered_enrollment = enrollment_df[enrollment_df['province'].isin(province_sel)] if province_sel else enrollment_df
    st.download_button(
        "🎓 Download Enrollment Data", 
        to_csv_download(filtered_enrollment), 
        file_name=f"enrollment_filtered_{year_sel}.csv",
        mime="text/csv",
        help="Download enrollment data with current filters applied"
    )

with dlcol3:
    st.download_button(
        "🏆 Download District Data", 
        to_csv_download(perf_snap), 
        file_name=f"districts_filtered_{year_sel}.csv",
        mime="text/csv",
        help="Download district performance data with current filters applied"
    )

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;">
    <h3 style="color: white; margin: 0;">🇵🇰 Pakistan Education Dashboard</h3>
    <p style="margin: 0.5rem 0 0 0;">Built with ❤️ using Streamlit & Plotly</p>
    <p style="font-size: 0.9rem; margin: 0.5rem 0 0 0; opacity: 0.9;">Replace sample data in the <code>data/</code> folder with real datasets for actual insights</p>
</div>
""", unsafe_allow_html=True)
