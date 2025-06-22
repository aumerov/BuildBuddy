# 🔧 BuildBuddy

AI-powered hardware repair and design assistant using Claude API. Upload images of hardware tools, PCBs, drones, or other devices and get step-by-step repair instructions and design feedback.

## Features

- 📷 **Image Analysis**: Upload photos of broken or problematic hardware
- 📝 **Text Descriptions**: Describe issues when images aren't available  
- 🤖 **AI-Powered Analysis**: Uses Claude API for expert hardware analysis
- 🔧 **Multiple Analysis Types**: Repair, troubleshooting, design review, component analysis
- 💾 **Export Results**: Download analysis as text files
- 🛡️ **Safety Focused**: Includes safety warnings and best practices

## Quick Start

1. **Clone and setup**:
   ```bash
   cd BuildBuddy
   uv sync
   ```

2. **Configure API key**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Anthropic API key
   ```

3. **Run the application**:
   ```bash
   uv run streamlit run app.py
   ```

4. **Open in browser**: http://localhost:8501

## Configuration

### API Key Setup
1. Get your API key from [Anthropic Console](https://console.anthropic.com/)
2. Copy `.env.example` to `.env`
3. Add your key: `ANTHROPIC_API_KEY=your_key_here`

### Supported Image Formats
- JPG/JPEG
- PNG  
- WebP
- Maximum file size: 10MB
- Maximum resolution: 2048x2048px

## Usage Examples

### PCB Analysis
- Upload images of circuit boards
- Describe symptoms (not working, burning smell, etc.)
- Get component-level troubleshooting steps

### Drone Repair  
- Show damaged propellers, motors, or frames
- Describe flight issues or mechanical problems
- Receive repair procedures and part recommendations

### Design Review
- Upload PCB layouts or mechanical designs
- Get feedback on improvements and potential issues
- Learn best practices and design optimization

## Project Structure

```
BuildBuddy/
├── app.py                 # Main Streamlit application
├── src/
│   ├── claude_client.py   # Claude API integration
│   ├── image_processor.py # Image handling and validation
│   └── prompts.py         # System prompts for hardware analysis
├── .env.example           # Environment variable template
└── pyproject.toml         # Project dependencies
```

## Safety Notes

⚠️ **Always prioritize safety when working with hardware:**
- Disconnect power before repairs
- Use proper ESD protection  
- Wear appropriate safety equipment
- Consult professionals for high-voltage or complex repairs

## Dependencies

- `streamlit` - Web interface
- `anthropic` - Claude API client
- `python-dotenv` - Environment variable management
- `pillow` - Image processing

## Contributing

This project follows defensive security practices:
- API keys are stored securely in environment variables
- Input validation for all user uploads
- Error handling for API failures
- No malicious code generation capabilities