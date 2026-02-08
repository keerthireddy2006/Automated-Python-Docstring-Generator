import streamlit as st
import tempfile
import pandas as pd
from src.parser import parse_file
from src.generator import generate_docstring
from src.coverage import coverage_report
from src.compliance import analyze_docstring
from src.pydoc_report import run_pydocstyle
from src.pep257_fixer import run_full_pep257
from src.injector import inject_docstrings
import subprocess

if "show_code" not in st.session_state:
    st.session_state.show_code = False


def section(title, icon=""):
    st.markdown(
        f"""
        <div style="margin-top:30px; margin-bottom:15px;">
            <h2>{icon} {title}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Auto Docstring Generator",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------ DARK MODE CSS ------------------
st.markdown(
    """
    <style>
        body { background-color: #0e1117; color: white; }
        .stApp { background-color: #0e1117; }
        .block-container { padding-top: 1.5rem; }
        h1, h2, h3, h4 { color: #ffffff; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------ SIDEBAR ------------------
st.sidebar.title("🧠 Docstring Tool")
st.sidebar.caption("Automated Python Docstring Generator")
st.sidebar.markdown("---")

style = st.sidebar.selectbox("Docstring Style", ["Google", "NumPy", "reST"])

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
### Features
- AST-based parsing
- Multi-style docstrings
- Attribute extraction
- PEP-257 compliance
- Section completeness
- Coverage analytics
"""
)

# ------------------ HEADER ------------------
st.markdown(
    "<h1 style='text-align:center;'>📄 Automated Python Docstring Generator</h1>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ------------------ FILE UPLOAD ------------------
uploaded_file = st.file_uploader("Upload a Python (.py) file", type=["py"])

if uploaded_file:
    raw = uploaded_file.read()

    source_code = raw.decode("utf-8")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp.write(raw)
        tmp.flush()
        file_path = tmp.name

    parsed_data = parse_file(file_path)

    # ================= SOURCE CODE VIEWER =================
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    # st.markdown("---")
    if st.button("📄 Show Source Code"):
        st.session_state.show_code = True

    if st.session_state.get("show_code"):
        with st.expander("Uploaded Source Code", expanded=True):
            st.code(source_code, language="python")

    # ================= FUNCTIONS =================
    if parsed_data["functions"]:
        st.subheader("🔹 Standalone Functions")

        for func in parsed_data["functions"]:
            with st.expander(f"Function: {func['name']}()", expanded=False):

                result = analyze_docstring(func, style)
                if result["pep257_compliant"]:
                    st.success("PEP-257 Compliant")
                else:
                    st.error("Missing: " + ", ".join(result["missing_sections"]))

                if result.get("formatting_issues"):
                    st.warning("Formatting: " + ", ".join(result["formatting_issues"]))

                if result.get("warnings"):
                    st.info("Warnings: " + ", ".join(result["warnings"]))

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("🟢 **Existing Docstring**")
                    st.code(func["docstring"] or "No docstring", language="python")

                with col2:
                    st.markdown("🔵 **Generated Docstring**")
                    st.code(generate_docstring(func, style=style))

    # ================= CLASSES =================
    if parsed_data["classes"]:
        st.subheader("🧱 Classes & Methods")

        for cls in parsed_data["classes"]:
            with st.expander(f"📦 Class: {cls['class_name']}"):

                if cls["attributes"]:
                    st.markdown("**Attributes:** " + ", ".join(cls["attributes"]))
                else:
                    st.caption("No class attributes detected")

                for method in cls["methods"]:
                    with st.expander(f"🔧 Method: {method['name']}()"):

                        result = analyze_docstring(method, style)
                        if result["pep257_compliant"]:
                            st.success("PEP-257 Compliant")
                        else:
                            st.error(
                                "Missing: " + ", ".join(result["missing_sections"])
                            )

                        if result.get("formatting_issues"):
                            st.warning(
                                "Formatting: " + ", ".join(result["formatting_issues"])
                            )

                        if result.get("warnings"):
                            st.info("Warnings: " + ", ".join(result["warnings"]))

                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("🟢 **Existing Docstring**")
                            st.code(
                                method["docstring"] or "No docstring", language="python"
                            )

                        with col2:
                            st.markdown("🔵 **Generated Docstring**")
                            st.code(
                                generate_docstring(method, cls["class_name"], style),
                                language="python",
                            )

    # ================= COVERAGE =================
    report = coverage_report(parsed_data)

    st.markdown("---")
    section("Documentation Coverage", "📊")

    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Functions", report["Functions"])
        c2.metric("Methods", report["Methods"])
        c3.metric("Classes", report["Classes"])
        c4.metric("Total", report["Total"])

        st.markdown("")

        c5, c6, c7 = st.columns([1, 1, 2])
        c5.metric("Documented", report["Documented"])
        c6.metric("Missing", report["Missing"])
        c7.metric("Coverage %", f"{report['Coverage (%)']:.2f}%")

    # ================= COVERAGE BY TYPE =================

    section("Coverage by Type", "📐")

    with st.container():
        t1, t2, t3 = st.columns(3)
        t1.metric("Function Coverage", f"{report['Function Coverage (%)']:.2f}%")
        t2.metric("Method Coverage", f"{report['Method Coverage (%)']:.2f}%")
        t3.metric("Class Coverage", f"{report['Class Coverage (%)']:.2f}%")

    section("PEP-257 Compliance", "📘")

    with st.container():
        p1, p2 = st.columns([1, 2])
        p1.metric("Compliant", report["PEP-257 Compliant"])
        p2.metric("Compliance %", f"{report['PEP-257 Compliance (%)']:.2f}%")

    section("PEP-257 Detailed Compliance Report", "🚨")

    if st.button("Generate PEP-257 Compliance Report"):

        issues = run_pydocstyle(file_path)
        # st.write("RAW PYDOCSTYLE OUTPUT:")
        # st.write(issues)
        if issues:

            df = pd.DataFrame(issues)

            st.error(f"Found {len(df)} PEP-257 Violations")

            st.dataframe(df, use_container_width=True)

            st.download_button(
                "⬇️ Download Compliance Report",
                df.to_csv(index=False),
                "pep257_report.csv",
            )

        else:
            st.success("No PEP-257 violations found.")

    section("Non-Compliant Functions & Methods", "🚨")

    non_compliant = report.get("Non-Compliant Items", [])

    if non_compliant:
        df = pd.DataFrame(non_compliant)
        st.dataframe(df, use_container_width=True)

        st.download_button(
            "⬇️ Download Non-Compliant Report",
            df.to_csv(index=False),
            file_name="non_compliant_report.csv",
            mime="text/csv",
        )
    else:
        st.success("🎉 All functions and methods are PEP-257 compliant!")
    section("Missing Documentation Sections", "🧪")

    with st.container():
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Parameters", report["Missing Parameters"])
        m2.metric("Returns", report["Missing Returns"])
        m3.metric("Raises", report["Missing Raises"])
        m4.metric("Yields", report["Missing Yields"])
        m5.metric("Attributes", report["Missing Attributes"])

    # ================= DOWNLOAD REPORT =================
    report_df = pd.DataFrame(report.items(), columns=["Metric", "Value"])
    st.download_button(
        "⬇️ Download Coverage Report",
        report_df.to_csv(index=False),
        file_name="docstring_coverage_report.csv",
        mime="text/csv",
    )

    # ================= VISUAL ANALYTICS =================
    st.markdown("---")
    st.subheader("📈 Visual Analytics")

    viz_type = st.selectbox(
        "Select Visualization Type", ["Bar Chart", "Pie Chart", "Line Chart"]
    )

    # ---------- DATA PREP ----------
    status_df = pd.DataFrame(
        {
            "Category": ["Documented", "Missing"],
            "Count": [report["Documented"], report["Missing"]],
        }
    )

    coverage_type_df = pd.DataFrame(
        {
            "Category": ["Functions", "Methods", "Classes"],
            "Coverage (%)": [
                report["Function Coverage (%)"],
                report["Method Coverage (%)"],
                report["Class Coverage (%)"],
            ],
        }
    )

    missing_df = pd.DataFrame(
        {
            "Category": ["Parameters", "Returns", "Raises", "Yields", "Attributes"],
            "Count": [
                report["Missing Parameters"],
                report["Missing Returns"],
                report["Missing Raises"],
                report["Missing Yields"],
                report["Missing Attributes"],
            ],
        }
    )

    # ---------- VISUALIZATION ----------
    v1, v2, v3 = st.columns(3)

    with v1:
        st.markdown("**Docstring Status**")
        if viz_type == "Bar Chart":
            st.bar_chart(status_df.set_index("Category"))
        elif viz_type == "Pie Chart":
            st.pyplot(
                status_df.set_index("Category")
                .plot.pie(y="Count", autopct="%1.1f%%", legend=False)
                .figure
            )
        else:
            st.line_chart(status_df.set_index("Category"))

    with v2:
        st.markdown("**Coverage by Type (%)**")
        if viz_type == "Bar Chart":
            st.bar_chart(coverage_type_df.set_index("Category"))
        elif viz_type == "Pie Chart":
            st.pyplot(
                coverage_type_df.set_index("Category")
                .plot.pie(y="Coverage (%)", autopct="%1.1f%%", legend=False)
                .figure
            )
        else:
            st.line_chart(coverage_type_df.set_index("Category"))

    with v3:
        st.markdown("**Missing Sections**")
        if viz_type == "Bar Chart":
            st.bar_chart(missing_df.set_index("Category"))
        elif viz_type == "Pie Chart":
            st.pyplot(
                missing_df.set_index("Category")
                .plot.pie(y="Count", autopct="%1.1f%%", legend=False)
                .figure
            )
        else:
            st.line_chart(missing_df.set_index("Category"))

    st.markdown("---")
    if st.button("Apply Generated Docstrings"):

        with st.spinner("🧠 Phi is generating docstrings... please wait"):

            updated = inject_docstrings(source_code)

        st.success("✅ Docstrings generated successfully!")

        # Save updated file temporarily
        # Write updated code to temp file for compliance check
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".py", encoding="utf-8"
        ) as f:
            f.write(updated)
            f.flush()
            updated_path = f.name

        # Run PEP257 on updated file
        updated_issues = run_pydocstyle(updated_path)

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("### Original Source")
            st.code(source_code, language="python")

        with c2:
            st.markdown("### Updated Source")
            st.code(updated, language="python")

        st.download_button("⬇️ Download Updated File", updated, "updated_source.py")

    st.success("✅ Milestone-2 Completed Successfully")
