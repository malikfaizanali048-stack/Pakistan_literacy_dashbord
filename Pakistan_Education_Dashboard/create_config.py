"""
Quick script to create .streamlit directory and config
"""
from pathlib import Path

# Create .streamlit directory
streamlit_dir = Path(".streamlit")
streamlit_dir.mkdir(exist_ok=True)

# Create config.toml
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

print("✓ Created .streamlit/config.toml")
print("Theme configured with Pakistan flag colors!")
