import streamlit as st
from database import get_all_assets, log_onboarding, update_asset

def render():
    st.markdown("""
    <div class="main-header">
        <h1>👤 Employee Onboarding</h1>
        <p>Assign IT equipment to a new employee and generate an onboarding record</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 📝 New Employee Equipment Assignment")

        with st.form("onboarding_form", clear_on_submit=True):
            employee_name = st.text_input("Employee Full Name *", placeholder="e.g. John Smith")
            department    = st.selectbox("Department *", [
                "Finance", "HR", "IT", "Operations", "Sales",
                "Accounting", "Engineering", "Quality", "Marketing"
            ])
            location = st.selectbox("Location *", ["Windsor HQ", "Plant Floor"])

            st.markdown("---")
            st.markdown("#### 🖥️ Select Equipment to Assign")
            st.caption("Only Available assets are shown below.")

            # Show available assets
            available = [a for a in get_all_assets(status_filter="Available")]
            if not available:
                st.warning("No available assets at this time. Please check the Asset Inventory.")
                st.form_submit_button("Submit", disabled=True)
                return

            asset_options = {
                f"{a['asset_id']} — {a['brand']} {a['model']} ({a['device_type']})": a["asset_id"]
                for a in available
            }

            selected_labels = st.multiselect(
                "Assets to assign",
                options=list(asset_options.keys()),
                help="Select one or more assets to assign to this employee"
            )

            notes = st.text_area("Notes", placeholder="e.g. Standard IT kit for Finance dept — laptop, monitor, mouse")
            processed_by = st.text_input("Processed By (IT Staff) *", placeholder="e.g. Omar Farouk")

            submitted = st.form_submit_button("✅ Complete Onboarding", type="primary",
                                              use_container_width=True)

        if submitted:
            if not employee_name or not processed_by or not selected_labels:
                st.error("Please fill in employee name, processed by, and select at least one asset.")
            else:
                selected_ids = [asset_options[label] for label in selected_labels]

                # Update each asset
                for aid in selected_ids:
                    update_asset(aid, employee_name, department, location, "Active", "", processed_by)

                # Log the event
                log_onboarding(employee_name, department, selected_ids, processed_by, notes)

                st.success(f"✅ Onboarding complete for **{employee_name}**!")
                st.info(f"""
                **Summary:**
                - **Employee:** {employee_name} ({department} — {location})
                - **Assets Assigned:** {", ".join(selected_ids)}
                - **Processed By:** {processed_by}
                - **Record saved to Onboarding Log** ✓
                """)
                st.balloons()
