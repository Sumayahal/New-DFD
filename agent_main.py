import os
from dotenv import dotenv_values
from openai import OpenAI
from dfd_utils import draw_dfd_from_text
from main import generate_dfd_from_description, convert_folder_to_classic_datastore, generate_incremental_filename
import shutil

class DFDAgent:
    def __init__(self):
        self.api_key = dotenv_values().get("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "ft:gpt-4.1-2025-04-14:personal::ByG2Ij7V"

    def run(self, description):
        print("🤖 Agent: Generating DFD, please wait...")
        full_output, elapsed_time = generate_dfd_from_description(description)
        
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
            f"System Description:\n{description.strip()}\n\n"
            f"Generated DFD (DOT format):\n{dfd_dot}\n\n"
            f"{trust_info}\n"
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        with open(archive_txt_path, "w", encoding="utf-8") as f:
            f.write(content)

        draw_dfd_from_text(dfd_dot)
        if os.path.exists("generated_dfd.png"):
            shutil.copy("generated_dfd.png", archive_img_path)

        print(f"✅ Agent: DFD generated and saved as '{filename}.png'")
        print(f"🕒 Total time: {elapsed_time:.2f} seconds")
        print(f"📄 Output saved to: {output_path}")

# Entry point
if __name__ == "__main__":
    agent = DFDAgent()
    print("🧠 Welcome to Smart DFD Agent")
    while True:
        user_input = input("📝 Describe your system (or type 'exit'): ").strip()
        if user_input.lower() == "exit":
            break
        if not user_input:
            continue
        agent.run(user_input)
