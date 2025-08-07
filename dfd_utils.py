import graphviz

def draw_dfd_from_text(dfd_dot_text):
    try:
        if 'digraph' in dfd_dot_text:
            start = dfd_dot_text.find('{')
            end = dfd_dot_text.rfind('}')
            dfd_dot_text = dfd_dot_text[start+1:end].strip()

        full_dot_code = (
            'digraph DFD {\n'
            'rankdir=LR;\n'
            'splines=polyline;\n'
            'nodesep=1.2;\n'
            'ranksep=1.7;\n'
            'graph [pad="0.5", fontsize=12, fontname="Arial"];\n'
            'node [style="filled,rounded", fillcolor="#f9f9f9", fontsize=11, fontname="Arial", margin="0.4,0.3"];\n'
            'edge [fontsize=10, fontname="Arial", labelfontcolor="#333333", color=black, penwidth=1.0];\n'
            + dfd_dot_text + '\n}'
        )

        graph = graphviz.Source(full_dot_code, format="png")
        graph.render("generated_dfd", cleanup=True)
        print("✅ DFD image saved as: generated_dfd.png")
    except Exception as e:
        print("❌ Error rendering DFD:", e)