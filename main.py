import os
import re
import time
import shutil
from datetime import datetime
from dotenv import dotenv_values
from openai import OpenAI
from dfd_utils import draw_dfd_from_text

api_key = dotenv_values().get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

fine_tuned_model = "ft:gpt-4.1-2025-04-14:personal::ByG2Ij7V"

def sanitize_filename(text):
    return re.sub(r'[^\w\s-]', '', text).replace(" ", "_")[:80]

def generate_incremental_filename():
    date_str = datetime.now().strftime("%Y-%m-%d")
    counter_file = "archive/counter.txt"

    if not os.path.exists(counter_file):
        with open(counter_file, "w") as f:
            f.write("1")
        count = 1
    else:
        with open(counter_file, "r") as f:
            count = int(f.read().strip()) + 1
        with open(counter_file, "w") as f:
            f.write(str(count))

    return f"{date_str}System{count:02d}"

def generate_dfd_from_description(description):
    messages = [
        {
            "role": "system",
            "content": """You are a senior security architect and system modeler specializing in smart systems such as IoT, healthcare, and industrial automation.

Your mission:
1. Generate a high-quality Data Flow Diagram (DFD) in Graphviz DOT format based on the user description. The diagram must be fully aligned with Microsoft Threat Modeling Tool (TMT) conventions.

2. Follow these shape mappings:
   - ExternalInteractor → shape=square
   - Process → shape=circle
   - Multi-Process → shape=doublecircle
   - DataStore → shape=cylinder
   - Trust Boundary → red dashed cluster

3. Rules for modeling:
- Classify each component properly based on name and behavior.
- Label each data flow explicitly as a request, **response, **stream, or **control signal
- Show bidirectional flows if present (two separate arrows)
- Do not group distinct functions in the same node
- Ensure all components mentioned or implied in the description are modeled.
- If zones like "IoT Device Zone", "Azure Zone", etc. are described or implied, wrap them in subgraphs with dashed red borders labeled accordingly

4. Use only the following allowed components:
   - ExternalInteractor: Human User, Browser, Mobile Application, External Web Application, IoT Device
   - Process: Web Application, Web Server, Native Application, Managed Application, IoT Gateway, AI Service, Stream Processor, Cloud Gateway
   - DataStore: SQL Database, File System, Cloud Storage, Audit Log, Azure Storage
   - Trust Boundary: IoT Device Zone, IoT Field Gateway Zone, IoT Cloud Gateway Zone, Azure Zone, User Interaction, Generic Trust Boundary

5. Do not explain the diagram — output only Graphviz DOT code

Format:
====================
<Graphviz DOT code>
====================
Then generate this:
Trust Boundaries Breakdown:
1. <Zone Name> (Trust Boundary Type):
   - External Interactors:
     • Name → Type
   - Processes:
     • Name → Type
   - Data Stores:
     • Name → Type
"""
        },
        {"role": "user", "content": description}
    ]

    start_time = time.time()
    response = client.chat.completions.create(
        model=fine_tuned_model,
        messages=messages,
        temperature=0.4
    )
    end_time = time.time()
    elapsed = end_time - start_time
    return response.choices[0].message.content.strip(), elapsed

def convert_folder_to_classic_datastore(dot_code):
    datastore_keywords = ["azure storage", "audit log", "sql database", "file system", "cloud storage"]

    def create_datastore_block(node_id, label):
        return f'{node_id} [label="{label}", shape=cylinder];'

    lines = dot_code.splitlines()
    new_lines = []

    for line in lines:
        match = re.match(r'(\w+)\s*\[.label\s=\s*"(.*?)"', line)
        if match:
            node_id, label = match.groups()
            if label.strip().lower() in [k.lower() for k in datastore_keywords]:
                new_lines.append(create_datastore_block(node_id, label.strip()))
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    return "\n".join(new_lines)

def main():
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("archive", exist_ok=True)

    while True:
        user_input = input("📝 Enter system description (or type 'exit'): ").strip()
        if not user_input:
            continue
        if user_input.lower() == "exit":
            break

        full_output, elapsed_time = generate_dfd_from_description(user_input)
        parts = full_output.split("Trust Boundaries Breakdown:")
        if len(parts) == 2:
            dfd_dot = parts[0].replace("====================", "").strip()
            trust_info = "Trust Boundaries Breakdown:\n" + parts[1].strip()
        else:
            dfd_dot = full_output
            trust_info = "⚠ Trust boundary info not found."

        dfd_dot = convert_folder_to_classic_datastore(dfd_dot)
        dfd_dot = dfd_dot.replace("shape=ellipse", "shape=circle")
        dfd_dot = dfd_dot.replace("shape=box", "shape=square")

        filename = generate_incremental_filename()

        output_path = os.path.join("outputs", f"{filename}.txt")
        archive_txt_path = os.path.join("archive", f"{filename}.txt")
        archive_img_path = os.path.join("archive", f"{filename}.png")

        content = (
            f"Time taken to generate DFD: {elapsed_time:.2f} seconds\n\n"
            f"System Description:\n{user_input.strip()}\n\n"
            f"Generated DFD (DOT format):\n{dfd_dot}\n\n"
            f"{trust_info}\n"
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        with open(archive_txt_path, "w", encoding="utf-8") as f:
            f.write(content)

        draw_dfd_from_text(dfd_dot)
        print(f"🕒 Total generation time: {elapsed_time:.2f} seconds")

        if os.path.exists("generated_dfd.png"):
            shutil.copy("generated_dfd.png", archive_img_path)

        print(f"✅ Output saved to: {output_path}")

if __name__ == "__main__":
    main()
