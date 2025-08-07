🤖 New-DFD: AI-Powered Data Flow Diagram Generator

This project was built as part of my master’s thesis to explore how artificial intelligence can be used to **automatically generate Data Flow Diagrams (DFDs)** for smart systems. It uses a **fine-tuned OpenAI GPT model** that takes a natural language description as input and outputs a structured, professional DFD diagram in multiple formats.

📁 What's Inside?

- `main.py`: Command-line script to run the tool.
- `agent_main.py`: Core logic to process user input and interact with GPT.
- `agent_streamlit.py`: Web interface to input system descriptions and view generated DFDs (with download options).
- `dfd_utils.py`: Functions to process and render DFDs using Graphviz.
- `convert_to_prompt_engine.py`: Converts natural language into a structured prompt for GPT.
- `requirements.txt`: A list of Python libraries required for the project.
- `.env`: Not included. You’ll need to create this file with your OpenAI API key.
- `outputs/`: Folder where all generated DFDs, images, and reports are saved.


🧑‍💻 How to Download and Run This Project

Here’s how you can set it up on your own machine in a few easy steps:

 ✅ 1. Download the project

Option 1 – via Git:

```bash
git clone https://github.com/Sumayahal/New-DFD.git
cd New-DFD

Option 2 – via ZIP:

Go to this repository

Click the green “Code” button → choose “Download ZIP”

Extract the ZIP file somewhere on your computer (e.g., Desktop)

✅ 2. Open a terminal in the folder
If you're using Windows:

Right-click inside the project folder → select "Open in Terminal"

On macOS/Linux:

Open Terminal → cd into the extracted folder

✅ 3. (Optional but recommended) Create a virtual environment

Windows:
python -m venv venv
venv\Scripts\activate

macOS/Linux:
python3 -m venv venv
source venv/bin/activate

✅ 4. Install the required Python packages

pip install -r requirements.txt
This will install:
-openai
-graphviz
-python-dotenv

✅ 5. Install Graphviz
Windows:
Download and install from:
https://graphviz.org/download
➡️ During installation, make sure to check “Add Graphviz to system PATH”

Ubuntu (Linux):
sudo apt install graphviz

macOS (with Homebrew):
brew install graphviz

✅ 6. Create your .env file
Inside the same project folder, create a file named .env and add the following line:
OPENAI_API_KEY=your_openai_key_here

✅ 7. Run the tool

Option 1 – Terminal Interface (CLI):

python main.py

You’ll be asked to enter a smart system description. The tool will generate:

generated_dfd.dot: the raw Graphviz output

generated_dfd.png: the rendered image

outputs/<date>SystemXX.txt: full summary

Option 2 – Web Interface (Streamlit):
-venv\Scripts\activate
streamlit run agent_streamlit.py

This will launch a web UI where you can:

Paste your system description

View the generated DFD image

Download the result as PNG or PDF

📝 Notes
You need an internet connection to access the OpenAI API.

This tool was developed for academic and research purposes.

You can modify the prompts, shapes, or GPT output format inside main.py and agent_streamlit.py.

👩‍💻 Author
Sumayah Najah Sabea Alaasam
Master’s Thesis – Software Engineering
Mälardalens University, Sweden
GitHub: Sumayahal


