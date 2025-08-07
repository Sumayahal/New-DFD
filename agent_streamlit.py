import os
import time
import shutil
import streamlit as st
from main import generate_dfd_from_description, convert_folder_to_classic_datastore, generate_incremental_filename
from dfd_utils import draw_dfd_from_text

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(page_title="Smart DFD Agent", layout="wide")

st.title("🤖 Smart DFD Agent")
st.markdown("Enter your smart system description below to automatically generate a professional Data Flow Diagram (DFD).")

description = st.text_area("📝 System Description", height=250)

if st.button("Generate DFD"):
    if not description.strip():
        st.warning("Please enter a system description.")
    else:
        with st.spinner("Generating DFD..."):
            start = time.time()
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

            os.makedirs("outputs", exist_ok=True)
            os.makedirs("archive", exist_ok=True)

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

                st.success(f"DFD generated successfully in {elapsed_time:.2f} seconds ✅")
                st.image("generated_dfd.png", caption="Generated DFD", use_column_width=True)

                # Download button - PNG
                with open("generated_dfd.png", "rb") as img_file:
                    st.download_button(
                        label="📥 Download DFD as PNG",
                        data=img_file,
                        file_name=f"{filename}.png",
                        mime="image/png"
                    )

                # Generate PDF report
                pdf_path = f"{filename}.pdf"
                c = canvas.Canvas(pdf_path, pagesize=A4)
                width, height = A4

                c.setFont("Helvetica-Bold", 14)
                c.drawString(40, height - 40, "Smart DFD - System Report")

                c.setFont("Helvetica", 10)
                text_obj = c.beginText(40, height - 70)
                for line in content.split("\n"):
                    text_obj.textLine(line)
                c.drawText(text_obj)

                # Add image (scaled if needed)
                try:
                    c.drawImage("generated_dfd.png", 40, 40, width=500, preserveAspectRatio=True, mask='auto')
                except:  # noqa: E722
                    pass

                c.save()

                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📄 Download Full Report as PDF",
                        data=pdf_file,
                        file_name=pdf_path,
                        mime="application/pdf"
                    )
            else:
                st.error("❌ Failed to generate DFD image.")
