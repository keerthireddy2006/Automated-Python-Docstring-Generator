import streamlit as st
import tempfile
import pandas as pd
from autodocstring.parser import parse_file
from autodocstring.generator import generate_docstring
from autodocstring.coverage import coverage_report
from autodocstring.compliance import analyze_docstring
from autodocstring.pydoc_report import run_pydocstyle
from autodocstring.pep257_fixer import run_full_pep257
from autodocstring.injector import inject_docstrings
import subprocess

if "show_code" not in st.session_state:
    st.session_state.show_code = False

# ────────────────────────────────────────────────
# PAGE CONFIG & STYLING (royal purple accents, black background)
# ────────────────────────────────────────────────

st.set_page_config(
    page_title="Automated Python Docstring Generator",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stApp { background-color: #000000; color: #e0e0ff; }
        .block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1400px; }
        h1, h2, h3 { color: #e0e0ff; }
        .header-card {
            background: linear-gradient(135deg, #0f1626, #1e3a5f);
            border-radius: 16px;
            padding: 2.5rem 2rem;
            text-align: center;
            box-shadow: 0 12px 35px rgba(0,0,0,0.5);
            margin-bottom: 2.5rem;
        }
        .card {
            background: #111111;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 6px 20px rgba(0,0,0,0.5);
            margin-bottom: 1.5rem;
        }
        .stButton > button {
            background: linear-gradient(90deg, #8b5cf6, #7c3aed);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.8rem 1.6rem;
            font-weight: bold;
            transition: all 0.3s;
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #7c3aed, #6d28d9);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(139,92,246,0.4);
        }
        .stSuccess { background-color: #3f2c5a !important; border: 1px solid #8b5cf6; color: #e0e0ff !important; }
        .stExpander { border-radius: 10px; border: 1px solid #4b3a6e; background: #0d0d1a; }
        .stTabs [data-baseweb="tab"] { background: #111111; border-radius: 10px 10px 0 0; padding: 0.6rem 1.2rem; color: #c4b5fd; }
        .stTabs [data-baseweb="tab"]:hover { background: #2d1b4e; }
        .stTabs [aria-selected="true"] { background: #8b5cf6 !important; color: white !important; }
        .uploaded-banner { background: linear-gradient(90deg, #6d28d9, #8b5cf6); color: white; padding: 1rem; border-radius: 8px; margin: 1rem 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────

with st.sidebar:
    st.image(
        "https://img.icons8.com/fluency-systems-filled/96/c084fc/source-code.png",
        width=70,
    )
    st.title("Docstring Generator")
    st.caption("v1.0 | Infosys Springboard Internship")

    st.markdown("---")

    style = st.selectbox(
        "Docstring Style",
        ["Google", "NumPy", "reST"],
        index=0,
        help="Google: clean & readable\nNumPy: detailed for arrays & returns\nreST: best for Sphinx docs",
    )

    st.markdown("### Key Features")
    st.markdown("• AST-powered parsing")
    st.markdown("• Multi-style generation")
    st.markdown("• PEP-257 compliance")
    st.markdown("• Coverage analytics")
    st.markdown("• Auto-apply & reports")

    st.markdown("---")
    st.info("Upload .py file to begin →")

# ────────────────────────────────────────────────
# HERO HEADER
# ────────────────────────────────────────────────

st.markdown(
    """
    <div class="header-card">
        <h1 style="margin:0; font-size: 3.8rem;">Automated Python Docstring Generator</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# ────────────────────────────────────────────────
# FILE UPLOAD + FILTERS (Milestone 4 improvements)
# ────────────────────────────────────────────────

st.markdown("### Upload Python File")
uploaded_file = st.file_uploader("", type=["py"], key="uploader")

if uploaded_file is not None:
    st.success(f"File uploaded: **{uploaded_file.name}**", icon="✅")

    st.markdown(
        f'<div class="uploaded-banner">✅ File uploaded: {uploaded_file.name}</div>',
        unsafe_allow_html=True,
    )

    with st.spinner("Analyzing your code..."):
        raw = uploaded_file.read()
        source_code = raw.decode("utf-8")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
            tmp.write(raw)
            tmp.flush()
            file_path = tmp.name

        parsed_data = parse_file(file_path)

    # ────────────────────────────────────────────────
    # FILTERS: Search + Show only missing (stacked vertically)
    # ────────────────────────────────────────────────

    st.markdown("### Filters")
    search_term = st.text_input(
        "🔍 Search functions, classes or methods",
        "",
        help="Case-insensitive search by name",
    )

    show_missing_only = st.checkbox(
        "Show only items missing docstrings",
        value=False,
        help="Hide items that already have docstrings",
    )

    # Apply filters to functions
    filtered_functions = [
        f
        for f in parsed_data.get("functions", [])
        if (search_term.lower() in f["name"].lower())
        and (not show_missing_only or not f.get("docstring"))
    ]

    # Apply filters to classes & their methods
    filtered_classes = []
    for cls in parsed_data.get("classes", []):
        filtered_methods = [
            m
            for m in cls.get("methods", [])
            if (search_term.lower() in m["name"].lower())
            and (not show_missing_only or not m.get("docstring"))
        ]
        # Include class if search matches name or it has filtered methods
        if filtered_methods or search_term.lower() in cls["class_name"].lower():
            filtered_classes.append(
                {
                    "class_name": cls["class_name"],
                    "attributes": cls.get("attributes", []),
                    "methods": filtered_methods,
                }
            )

    # ────────────────────────────────────────────────
    # TABS (use filtered data)
    # ────────────────────────────────────────────────

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📄 Source Code", "🔹 Functions", "🧱 Classes", "📊 Coverage"]
    )

    with tab1:
        st.subheader("Source Code Preview")
        if st.button("Toggle Full Source Code", key="toggle_code"):
            st.session_state.show_code = not st.session_state.get("show_code", False)

        if st.session_state.get("show_code", False):
            st.code(source_code, language="python")

    with tab2:
        st.subheader("Standalone Functions")
        if filtered_functions:
            for func in filtered_functions:
                with st.expander(f"def {func['name']}()"):
                    result = analyze_docstring(func, style)
                    if result["pep257_compliant"]:
                        st.success("PEP-257 Compliant")
                    else:
                        st.error("Missing: " + ", ".join(result["missing_sections"]))

                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Existing**")
                        st.code(func["docstring"] or "No docstring", language="python")
                    with col2:
                        st.markdown("**Generated**")
                        st.code(
                            generate_docstring(func, style=style), language="python"
                        )
        else:
            st.info("No matching standalone functions found.")

    with tab3:
        st.subheader("Classes & Methods")
        if filtered_classes:
            for cls in filtered_classes:
                with st.expander(f"class {cls['class_name']}"):
                    if cls["attributes"]:
                        st.markdown(f"**Attributes:** {', '.join(cls['attributes'])}")
                    else:
                        st.caption("No class attributes detected")

                    for method in cls["methods"]:
                        with st.expander(f"Method: {method['name']}()"):
                            result = analyze_docstring(method, style)
                            if result["pep257_compliant"]:
                                st.success("PEP-257 Compliant")
                            else:
                                st.error(
                                    "Missing: " + ", ".join(result["missing_sections"])
                                )

                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**Existing**")
                                st.code(
                                    method["docstring"] or "No docstring",
                                    language="python",
                                )
                            with col2:
                                st.markdown("**Generated**")
                                st.code(
                                    generate_docstring(
                                        method, cls["class_name"], style
                                    ),
                                    language="python",
                                )
        else:
            st.info("No matching classes or methods found.")

    # (rest of your tab4 coverage code remains unchanged)

    with tab4:
        report = coverage_report(parsed_data)
        st.subheader("Documentation Coverage")

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        cols = st.columns(4)
        cols[0].metric("Functions", report["Functions"])
        cols[1].metric("Methods", report["Methods"])
        cols[2].metric("Classes", report["Classes"])
        cols[3].metric("Total", report["Total"])

        st.markdown("---")

        c1, c2, c3 = st.columns(3)
        c1.metric("Documented", report["Documented"])
        c2.metric("Missing", report["Missing"])
        c3.metric("Coverage %", f"{report['Coverage (%)']:.2f}%", delta_color="normal")

        st.markdown("---")

        t1, t2, t3 = st.columns(3)
        t1.metric("Functions", f"{report['Function Coverage (%)']:.2f}%")
        t2.metric("Methods", f"{report['Method Coverage (%)']:.2f}%")
        t3.metric("Classes", f"{report['Class Coverage (%)']:.2f}%")

        st.markdown("---")

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Parameters", report["Missing Parameters"])
        m2.metric("Returns", report["Missing Returns"])
        m3.metric("Raises", report["Missing Raises"])
        m4.metric("Yields", report["Missing Yields"])
        m5.metric("Attributes", report["Missing Attributes"])

        st.markdown("</div>", unsafe_allow_html=True)

        report_df = pd.DataFrame(report.items(), columns=["Metric", "Value"])
        st.download_button(
            label="⬇️ Download Coverage Report",
            data=report_df.to_csv(index=False),
            file_name="docstring_coverage_report.csv",
            mime="text/csv",
        )

        st.markdown("---")
        st.subheader("PEP-257 Compliance Report")

        if st.button("Generate PEP-257 Compliance Report"):
            issues = run_pydocstyle(file_path)
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

        st.markdown("---")
        st.subheader("Non-Compliant Functions & Methods")

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

        st.markdown("---")
        st.subheader("Visual Analytics")

        viz_type = st.selectbox(
            "Visualization Type", ["Bar Chart", "Pie Chart", "Line Chart"]
        )

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

        v1, v2, v3 = st.columns(3)

        with v1:
            st.markdown(
                "<div class='metric-card'><strong>Docstring Status</strong></div>",
                unsafe_allow_html=True,
            )
            if viz_type == "Bar Chart":
                st.bar_chart(status_df.set_index("Category"))
            elif viz_type == "Pie Chart":
                st.pyplot(
                    status_df.set_index("Category")
                    .plot.pie(
                        y="Count",
                        autopct="%1.1f%%",
                        legend=False,
                        colors=["#8b5cf6", "#ef4444"],
                    )
                    .figure
                )
            else:
                st.line_chart(status_df.set_index("Category"))

        with v2:
            st.markdown(
                "<div class='metric-card'><strong>Coverage by Type (%)</strong></div>",
                unsafe_allow_html=True,
            )
            if viz_type == "Bar Chart":
                st.bar_chart(coverage_type_df.set_index("Category"))
            elif viz_type == "Pie Chart":
                st.pyplot(
                    coverage_type_df.set_index("Category")
                    .plot.pie(
                        y="Coverage (%)",
                        autopct="%1.1f%%",
                        legend=False,
                        colors=["#8b5cf6", "#fbbf24", "#a855f7"],
                    )
                    .figure
                )
            else:
                st.line_chart(coverage_type_df.set_index("Category"))

        with v3:
            st.markdown(
                "<div class='metric-card'><strong>Missing Sections</strong></div>",
                unsafe_allow_html=True,
            )
            if viz_type == "Bar Chart":
                st.bar_chart(missing_df.set_index("Category"))
            elif viz_type == "Pie Chart":
                st.pyplot(
                    missing_df.set_index("Category")
                    .plot.pie(
                        y="Count",
                        autopct="%1.1f%%",
                        legend=False,
                        colors=["#f97316", "#ec4899", "#a855f7", "#7c3aed", "#6366f1"],
                    )
                    .figure
                )
            else:
                st.line_chart(missing_df.set_index("Category"))

    # ────────────────────────────────────────────────
    # APPLY BUTTON
    # ────────────────────────────────────────────────

    st.markdown("---")
    if st.button(
        "✨ Apply Generated Docstrings", type="primary", use_container_width=True
    ):
        with st.spinner("Generating and injecting docstrings..."):
            updated = inject_docstrings(source_code, style)

        st.success("Docstrings generated and injected successfully!", icon="🎉")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Original Source")
            st.code(source_code, language="python")
        with col2:
            st.markdown("### Updated Source")
            st.code(updated, language="python")

        st.download_button(
            label="⬇️ Download Updated File",
            data=updated,
            file_name="updated_source.py",
            mime="text/x-python",
        )

    st.success("✅ Milestone-3 Completed Successfully", icon="🏆")
