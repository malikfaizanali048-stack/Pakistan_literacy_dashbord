# Pakistan Education Dashboard 🇵🇰

A beautiful, interactive dashboard for visualizing Pakistan's education data including literacy trends, gender gaps, enrollment statistics, and district performance.

![Dashboard](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python)

## ✨ Features

- **📈 National Literacy Trends**: Track overall literacy rates over time with interactive line charts
- **👫 Gender Gap Analysis**: Compare male vs female literacy rates and visualize the gap
- **🗺️ Province Comparison**: View and compare education metrics across all provinces
- **🎓 Enrollment Statistics**: Analyze student enrollment by province and education level (Primary, Middle, Secondary, Higher)
- **🏆 District Performance**: Identify top and bottom performing districts with detailed rankings
- **💾 Data Export**: Download filtered datasets as CSV for further analysis
- **🎨 Beautiful UI**: Modern design with Pakistan flag colors and smooth animations

## 🚀 Quick Start

### Method 1: One-Click Launch (Easiest)

**Windows Users:**
1. Double-click `run.bat`
2. Wait for the dashboard to open in your browser
3. Done! 🎉

### Method 2: Python Script

```bash
python setup_and_run.py
```

This will automatically:
- ✅ Check and install required dependencies
- ✅ Create sample data files
- ✅ Configure the theme
- ✅ Launch the dashboard

### Method 3: Manual Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Dashboard**
   ```bash
   streamlit run app.py
   ```

## 📋 Requirements

- Python 3.8 or higher
- Internet connection (for initial package installation only)

## 📊 Data Files

The dashboard uses three CSV files in the `data/` directory:

| File | Description |
|------|-------------|
| `literacy.csv` | Literacy rates by province, year, and gender |
| `enrollment.csv` | Student enrollment by province, level, and year |
| `school_performance.csv` | District-level performance metrics |

**Note:** If these files don't exist, the app will automatically generate sample data for demonstration purposes.

## 🎨 Customization

### Change Theme Colors

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#01411C"  # Pakistan flag green
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

### Use Your Own Data

Replace the CSV files in the `data/` folder with your own datasets. Ensure they have the required columns:

**literacy.csv:**
- `year`, `province`, `male_literacy`, `female_literacy`, `overall_literacy`

**enrollment.csv:**
- `year`, `province`, `level`, `enrollment`

**school_performance.csv:**
- `year`, `district`, `province`, `avg_score`, `pass_rate`, `num_students`

## 🛠️ Troubleshooting

### Module not found error
```bash
pip install pandas numpy streamlit plotly
```

### Streamlit command not found
```bash
python -m streamlit run app.py
```

### Data file issues
Delete the `data/` folder and restart the app to regenerate sample data

### Port already in use
The dashboard runs on port 8501 by default. If this port is busy, Streamlit will automatically use the next available port.

## 📱 Usage Guide

1. **Sidebar Filters**
   - 📅 Select year for data snapshots
   - 🗺️ Choose provinces to compare (multi-select)
   - 👥 Set minimum district student threshold for rankings

2. **Visualizations**
   - Interactive charts with hover details
   - Zoom, pan, and download chart images
   - Responsive design works on desktop and tablets

3. **Export Data**
   - Download filtered datasets at the bottom
   - Files include current filter settings
   - CSV format compatible with Excel, Python, R, etc.

## 🏗️ Built With

- **[Streamlit](https://streamlit.io/)** - Fast web app framework
- **[Plotly](https://plotly.com/python/)** - Interactive visualizations
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation
- **[NumPy](https://numpy.org/)** - Numerical computations

## 📝 Project Structure

```
Pakistan_Education_Dashboard/
├── app.py                  # Main dashboard application
├── setup_and_run.py        # Automated setup script
├── requirements.txt        # Python dependencies
├── run.bat                 # Windows launcher
├── README.md              # This file
├── .streamlit/
│   └── config.toml        # Streamlit configuration
└── data/
    ├── literacy.csv       # Literacy data
    ├── enrollment.csv     # Enrollment data
    └── school_performance.csv  # District performance data
```

## 🤝 Contributing

Feel free to fork this project and customize it for your needs. Some ideas:
- Add more visualizations (maps, heatmaps, etc.)
- Include more education metrics
- Add predictive analytics
- Create user authentication
- Add real-time data updates

## 📄 License

This project is open source and available for educational purposes.

## 🙏 Acknowledgments

Built with ❤️ for analyzing and improving Pakistan's education system.

---

**Need Help?** If you encounter any issues, check the Troubleshooting section above or open an issue in the repository.
