"""
Setup script to prepare data and run the Pakistan Education Dashboard
"""
import os
import sys
import subprocess
from pathlib import Path
import pandas as pd
import numpy as np

def generate_sample_literacy():
    """Generate sample literacy data with proper structure"""
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
    """Generate sample enrollment data with proper structure"""
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
    """Generate sample school performance data with proper structure"""
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

def check_dependencies():
    """Check if required packages are installed"""
    print("Checking dependencies...")
    required_packages = ['pandas', 'numpy', 'streamlit', 'plotly']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package} is installed")
        except ImportError:
            print(f"  ✗ {package} is NOT installed")
            missing.append(package)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Installing missing packages...")
        for package in missing:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print("All packages installed successfully!")
    else:
        print("\nAll dependencies are satisfied!")
    return True

def setup_data_files():
    """Setup data files with correct structure"""
    print("\nSetting up data files...")
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Generate and save literacy data
    literacy_path = data_dir / "literacy.csv"
    print(f"  Creating {literacy_path}...")
    literacy_df = generate_sample_literacy()
    literacy_df.to_csv(literacy_path, index=False)
    print(f"    ✓ Created with {len(literacy_df)} rows")
    
    # Generate and save enrollment data
    enrollment_path = data_dir / "enrollment.csv"
    print(f"  Creating {enrollment_path}...")
    enrollment_df = generate_sample_enrollment()
    enrollment_df.to_csv(enrollment_path, index=False)
    print(f"    ✓ Created with {len(enrollment_df)} rows")
    
    # Generate and save school performance data
    perf_path = data_dir / "school_performance.csv"
    print(f"  Creating {perf_path}...")
    perf_df = generate_sample_school_perf()
    perf_df.to_csv(perf_path, index=False)
    print(f"    ✓ Created with {len(perf_df)} rows")
    
    print("\nData files setup complete!")

def setup_streamlit_config():
    """Create Streamlit configuration with Pakistan theme"""
    print("\nSetting up Streamlit configuration...")
    streamlit_dir = Path(".streamlit")
    streamlit_dir.mkdir(exist_ok=True)
    
    config_content = """[theme]
primaryColor = "#01411C"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
"""
    
    config_path = streamlit_dir / "config.toml"
    config_path.write_text(config_content)
    print("  ✓ Created .streamlit/config.toml with Pakistan flag theme")
    print("Streamlit configuration complete!")

def run_dashboard():
    """Run the Streamlit dashboard"""
    print("\n" + "="*50)
    print("Starting Pakistan Education Dashboard...")
    print("="*50 + "\n")
    print("The dashboard will open in your browser.")
    print("Press Ctrl+C to stop the server.\n")
    
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    print("="*50)
    print("Pakistan Education Dashboard - Setup & Run")
    print("="*50 + "\n")
    
    try:
        # Step 1: Check dependencies
        check_dependencies()
        
        # Step 2: Setup Streamlit config
        setup_streamlit_config()
        
        # Step 3: Setup data files
        setup_data_files()
        
        # Step 4: Run dashboard
        run_dashboard()
        
    except KeyboardInterrupt:
        print("\n\nShutdown requested... exiting")
    except Exception as e:
        print(f"\n\nError occurred: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Python is installed and in PATH")
        print("2. Try installing packages manually: pip install pandas numpy streamlit plotly")
        print("3. Run the app directly: streamlit run app.py")
        sys.exit(1)
