import streamlit as st
import tempfile
import pandas as pd
from src.parser import parse_file
from src.generator import generate_docstring
from src.coverage import coverage_report


# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Auto Docstring Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ DARK MODE CSS ------------------
st.markdown(
    """
    <style>
        body {
            background-color: #0e1117;
            color: white;
        }
        .stApp {
            background-color: #0e1117;
        }
        .block-container {
            padding-top: 1.5rem;
        }
        h1, h2, h3, h4 {
            color: #ffffff;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------ SIDEBAR ------------------
st.sidebar.title("🧠 Docstring Tool")
st.sidebar.caption("Automated Python Docstring Generator")
st.sidebar.markdown("---")

st.sidebar.markdown("### Features")
st.sidebar.markdown("""
- AST-based parsing  
- Function & class detection  
- Baseline docstring generation  
- Detailed coverage analysis  
""")

st.sidebar.markdown("---")
st.sidebar.markdown("📌 **Milestone 1**")

# ------------------ HEADER ------------------
st.markdown(
    "<h1 style='text-align:center;'>📄 Automated Python Docstring Generator</h1>",
    unsafe_allow_html=True
)
st.markdown("---")

# ------------------ FILE UPLOAD ------------------
uploaded_file = st.file_uploader(
    "Upload a Python (.py) file",
    type=["py"]
)

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp.write(uploaded_file.read())
        file_path = tmp.name

    parsed_data = parse_file(file_path)

    # ------------------ FUNCTIONS ------------------
    if parsed_data.get("functions"):
        st.subheader("🔹 Standalone Functions")

        for func in parsed_data["functions"]:
            with st.expander(f"Function: {func['name']}()", expanded=False):

                if func["has_docstring"]:
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("🟢 **Existing Docstring**")
                        st.code(func["docstring"], language="python")

                    with col2:
                        st.markdown("🔵 **Generated Docstring**")
                        st.code(generate_docstring(func), language="python")
                else:
                    st.warning("⚠️ No existing docstring found")
                    st.code(generate_docstring(func), language="python")

    # ------------------ CLASSES & METHODS ------------------
    if parsed_data.get("classes"):
        st.subheader("🧱 Classes & Methods")

        for cls in parsed_data["classes"]:
            with st.expander(f"📦 Class: {cls['class_name']}", expanded=False):

                for method in cls["methods"]:
                    with st.expander(f"🔧 Method: {method['name']}()", expanded=False):

                        if method["has_docstring"]:
                            col1, col2 = st.columns(2)

                            with col1:
                                st.markdown("🟢 **Existing Docstring**")
                                st.code(method["docstring"], language="python")

                            with col2:
                                st.markdown("🔵 **Generated Docstring**")
                                st.code(
                                    generate_docstring(method, cls["class_name"]),
                                    language="python"
                                )
                        else:
                            st.warning("⚠️ No existing docstring found")
                            st.code(
                                generate_docstring(method, cls["class_name"]),
                                language="python"
                            )

    # ------------------ COVERAGE REPORT ------------------
    report = coverage_report(parsed_data)

    st.markdown("---")
    st.subheader("📊 Docstring Coverage Report")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Functions & Methods", report["Total Functions & Methods"])
    col2.metric("Documented", report["Documented"])
    col3.metric("Missing Docstrings", report["Missing Docstrings"])
    col4.metric("Coverage (%)", f"{report['Coverage (%)']:.2f}%")

    # ------------------ COVERAGE BY TYPE ------------------
    st.markdown("### 📐 Coverage by Type")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Function Coverage (%)",
        f"{report['Function Coverage (%)']:.2f}%",
        f"{report['Documented Functions']}/{report['Total Functions']}"
    )

    c2.metric(
        "Method Coverage (%)",
        f"{report['Method Coverage (%)']:.2f}%",
        f"{report['Documented Methods']}/{report['Total Methods']}"
    )

    c3.metric(
        "Class Coverage (%)",
        f"{report['Class Coverage (%)']:.2f}%",
        f"{report['Documented Classes']}/{report['Total Classes']}"
    )

    # ------------------ DOWNLOAD DOCSTRINGS ------------------
    all_docstrings = []

    for func in parsed_data["functions"]:
        all_docstrings.append(generate_docstring(func))

    for cls in parsed_data["classes"]:
        for method in cls["methods"]:
            all_docstrings.append(
                generate_docstring(method, cls["class_name"])
            )

    st.download_button(
        label="⬇️ Download All Generated Docstrings",
        data="\n\n".join(all_docstrings),
        file_name="generated_docstrings.txt",
        mime="text/plain"
    )

    # ------------------ VISUALIZATION ------------------
    st.markdown("---")
    st.subheader("📈 Documentation Overview")

    chart_df = pd.DataFrame({
        "Status": ["Documented", "Missing"],
        "Count": [
            report["Documented"],
            report["Missing Docstrings"]
        ]
    })

    st.markdown("### 📊 Docstring Status Distribution")

    chart_data = chart_df.set_index("Status")
    st.bar_chart(chart_data)


    st.success("✅ Analysis completed successfully! Upload another file to continue.")
