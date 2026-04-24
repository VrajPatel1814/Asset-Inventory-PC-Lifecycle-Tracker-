import streamlit as st
from database import get_all_employees, get_assets_by_employee, log_offboarding

def render():
    st.markdown("""
    <div class="main-header">
        <h1>📤 Employee Offboarding</h1>
        <p>Collect and return IT equipment from departing or transferring employees</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔄 Equipment Return Process")

        employees = get_all_employees()
        emp_names = [e["name"] for e in employees]

        selected_employee = st.selectbox("Select Employee", ["— Select —"] + emp_names)

        if selected_employee and selected_employee != "— Select —":
            emp_assets = get_assets_by_employee(selected_employee)
            emp_info   = next((e for e in employees if e["name"] == selected_employee), None)

            if emp_info:
                st.info(f"🏢 **{selected_employee}** — {emp_info['department']} | {emp_info['location']}")

            if not emp_assets:
                st.warning(f"No active assets currently assigned to **{selected_employee}**.")
            else:
                st.markdown(f"#### 🖥️ Currently Assigned Assets ({len(emp_assets)} items)")

                asset_options = {
                    f"{a['asset_id']} — {a['brand']} {a['model']} ({a['device_type']})": a["asset_id"]
                    for a in emp_assets
                }

                for a in emp_assets:
                    st.markdown(f"- `{a['asset_id']}` {a['brand']} {a['model']} — {a['device_type']}")

                st.markdown("---")

                with st.form("offboarding_form", clear_on_submit=True):
                    st.markdown("#### 📦 Select Assets Being Returned")
                    returned_labels = st.multiselect(
                        "Assets returned",
                        options=list(asset_options.keys()),
                        default=list(asset_options.keys()),
                        help="Deselect any items not yet returned"
                    )

                    processed_by = st.text_input("Processed By (IT Staff) *",
                                                 placeholder="e.g. Fatima Al-Hassan")
                    notes        = st.text_area("Notes",
                                                placeholder="e.g. All equipment returned in good condition. Laptop needs cleaning.")

                    submitted = st.form_submit_button("✅ Complete Offboarding",
                                                      type="primary", use_container_width=True)

                if submitted:
                    if not processed_by or not returned_labels:
                        st.error("Please select at least one asset and enter the IT staff name.")
                    else:
                        returned_ids = [asset_options[label] for label in returned_labels]
                        dept = emp_info["department"] if emp_info else "Unknown"
                        log_offboarding(selected_employee, dept, returned_ids, processed_by, notes)

                        st.success(f"✅ Offboarding complete for **{selected_employee}**!")
                        st.info(f"""
                        **Summary:**
                        - **Employee:** {selected_employee}
                        - **Assets Returned:** {", ".join(returned_ids)}
                        - **New Status:** Available (ready for redeployment)
                        - **Processed By:** {processed_by}
                        - **Record saved to Onboarding Log** ✓
                        """)
