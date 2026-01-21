"""
IS Curve Slope Classification Interface
========================================
Streamlit application for human validation of Claude's classifications
of FOMC speaker beliefs about how sensitive output/growth is to monetary policy
(the slope of the IS curve).

Following Mullainathan et al. (2024) framework for LLM output validation.

Usage:
    streamlit run coding_interface.py
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import io


def get_script_directory():
    """Get the directory where this script is located."""
    return Path(__file__).resolve().parent


SCRIPT_DIR = get_script_directory()

# Columns that are hidden from coders during classification
HIDDEN_COLUMNS = ['claude_is_slope', 'claude_is_slope_category']

# Columns included in output (alongside human coding)
OUTPUT_COLUMNS = [
    'coding_id', 'original_index', 'coder_name', 'classification',
    'claude_is_slope', 'claude_is_slope_category',
    'quotation', 'variable', 'stablespeaker', 'ymd',
    'notes', 'coded_at'
]

# Page configuration
st.set_page_config(
    page_title="IS Curve Slope Classification",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def load_coding_data_from_file(file_content):
    """Load the coding sample data from uploaded file."""
    return pd.read_csv(io.StringIO(file_content.decode('utf-8')), keep_default_na=False, na_values=[''])


def load_default_coding_data():
    """Load the default coding data from the repo (no cache to ensure fresh data on deploy)."""
    coding_file = SCRIPT_DIR / 'validation_samples' / 'production' / 'coding_is_slope.csv'
    if coding_file.exists():
        return pd.read_csv(coding_file, keep_default_na=False, na_values=[''])
    return None


def get_results_csv(results, coding_df):
    """
    Convert results to CSV for download.
    Includes Claude's classifications and key columns from the source data.
    """
    results_df = pd.DataFrame(results)

    # Merge with coding_df to get all the extra columns
    merged = results_df.merge(
        coding_df[['coding_id', 'original_index', 'quotation',
                   'variable', 'stablespeaker', 'ymd',
                   'claude_is_slope', 'claude_is_slope_category']],
        on='coding_id',
        how='left'
    )

    # Reorder columns for clarity
    output_cols = [c for c in OUTPUT_COLUMNS if c in merged.columns]
    merged = merged[output_cols]

    return merged.to_csv(index=False).encode('utf-8')


def get_previous_coding(coding_id, results):
    """Get previous coding values for a specific coding_id."""
    for result in results:
        if result.get('coding_id') == coding_id:
            return result
    return None


def validate_resume_csv(resume_df, coding_df):
    """
    Validate that a resume CSV is compatible with the current coding data.

    Returns:
        tuple: (is_valid, message, matching_ids)
    """
    required_cols = {'coding_id', 'coder_name', 'classification'}
    if not required_cols.issubset(resume_df.columns):
        missing = required_cols - set(resume_df.columns)
        return False, f"Missing required columns: {missing}", set()

    resume_ids = set(resume_df['coding_id'].tolist())
    coding_ids = set(coding_df['coding_id'].tolist())

    matching_ids = resume_ids.intersection(coding_ids)
    unmatched_ids = resume_ids - coding_ids

    if len(matching_ids) == 0:
        return False, "No coding_ids in resume file match current data source", set()

    if len(unmatched_ids) > 0:
        return True, f"Warning: {len(unmatched_ids)} coding_ids in resume file not found in current data (will be ignored)", matching_ids

    return True, f"Successfully validated {len(matching_ids)} coded arguments", matching_ids


def initialize_session_state():
    """Initialize all session state variables."""
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'results' not in st.session_state:
        st.session_state.results = []
    if 'coded_ids' not in st.session_state:
        st.session_state.coded_ids = set()
    if 'widget_version' not in st.session_state:
        st.session_state.widget_version = 0
    if 'locked_coder_name' not in st.session_state:
        st.session_state.locked_coder_name = None


def main():
    st.title("IS Curve Slope Classification")
    st.markdown("**Human Validation of LLM Classifications**")
    st.markdown("---")

    # Initialize session state
    initialize_session_state()

    # Sidebar setup
    with st.sidebar:
        st.header("Setup")

        # Coder identification
        if st.session_state.locked_coder_name is not None:
            st.text_input(
                "Your Name (locked)",
                value=st.session_state.locked_coder_name,
                disabled=True,
                help="Name is locked after first save to ensure consistency"
            )
            coder_name = st.session_state.locked_coder_name
        else:
            coder_name = st.text_input(
                "Your Name",
                placeholder="Enter your name",
                help="Used to identify your coding results. Will be locked after first save."
            )

        if not coder_name:
            st.warning("Please enter your name to begin")
            st.stop()

        # Data source selection
        st.markdown("---")
        st.subheader("Data Source")

        data_source = st.radio(
            "Choose data source:",
            ["Use default sample", "Upload custom file"],
            help="Use the pre-loaded sample or upload your own CSV"
        )

        coding_df = None

        if data_source == "Use default sample":
            coding_df = load_default_coding_data()
            if coding_df is None:
                st.error("Default coding file not found. Please upload a file.")
                st.stop()
            else:
                st.success(f"Loaded {len(coding_df)} arguments")
        else:
            uploaded_file = st.file_uploader(
                "Upload Coding File",
                type=['csv'],
                help="Upload a coding CSV file"
            )
            if uploaded_file:
                coding_df = load_coding_data_from_file(uploaded_file.getvalue())
                st.success(f"Loaded {len(coding_df)} arguments")
            else:
                st.info("Please upload a coding file")
                st.stop()

    total_arguments = len(coding_df)
    current_index = st.session_state.current_index

    # Get current widget version for keying
    v = st.session_state.widget_version

    # Progress tracking in sidebar
    with st.sidebar:
        st.markdown("---")
        st.header("Progress")

        n_coded = len(st.session_state.coded_ids)
        progress_pct = n_coded / total_arguments if total_arguments > 0 else 0
        st.progress(progress_pct)
        st.write(f"Coded: {n_coded} / {total_arguments}")
        st.write(f"Current: Argument {current_index + 1}")

        # Download results button
        st.markdown("---")
        st.subheader("Save Results")

        if st.session_state.results:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_name = coder_name.lower().replace(' ', '_')
            filename = f"coded_{safe_name}_is_slope_{timestamp}.csv"

            st.download_button(
                label="Download Results CSV",
                data=get_results_csv(st.session_state.results, coding_df),
                file_name=filename,
                mime="text/csv",
                help="Download your coding results (includes Claude's classifications)"
            )
            st.caption(f"{len(st.session_state.results)} arguments coded")
        else:
            st.info("Code some arguments to enable download")

        # Load previous session via upload
        st.markdown("---")
        st.subheader("Resume Session")

        resume_file = st.file_uploader(
            "Upload previous session",
            type=['csv'],
            key="resume_upload",
            help="Upload a previously downloaded results file to continue"
        )

        if resume_file:
            if st.button("Load Session"):
                try:
                    resume_df = pd.read_csv(resume_file, keep_default_na=False, na_values=[''])

                    # Validate the resume CSV
                    is_valid, message, matching_ids = validate_resume_csv(resume_df, coding_df)

                    if not is_valid:
                        st.error(f"Cannot load session: {message}")
                    else:
                        if "Warning" in message:
                            st.warning(message)

                        # Filter to only matching IDs and extract just the coding results
                        valid_resume = resume_df[resume_df['coding_id'].isin(matching_ids)]
                        valid_results = []
                        for _, row in valid_resume.iterrows():
                            valid_results.append({
                                'coding_id': row['coding_id'],
                                'coder_name': row['coder_name'],
                                'classification': row['classification'],
                                'notes': row.get('notes', ''),
                                'coded_at': row.get('coded_at', datetime.now().isoformat())
                            })

                        st.session_state.results = valid_results
                        st.session_state.coded_ids = set(r['coding_id'] for r in valid_results)

                        # Lock the coder name from the resume file
                        if len(valid_results) > 0:
                            st.session_state.locked_coder_name = valid_results[0].get('coder_name', coder_name)

                        # INCREMENT WIDGET VERSION to force fresh widget state
                        st.session_state.widget_version += 1

                        # Jump to first uncoded argument
                        found_uncoded = False
                        for idx in range(len(coding_df)):
                            if coding_df.iloc[idx]['coding_id'] not in st.session_state.coded_ids:
                                st.session_state.current_index = idx
                                found_uncoded = True
                                break

                        if not found_uncoded:
                            st.session_state.current_index = len(coding_df) - 1

                        st.success(f"Loaded {len(valid_results)} coded arguments")
                        st.rerun()

                except Exception as e:
                    st.error(f"Error loading session: {e}")

    # Main coding area
    if current_index < total_arguments:
        current_row = coding_df.iloc[current_index]
        coding_id = current_row['coding_id']
        quotation = current_row['quotation']
        description = current_row.get('description', '')
        variable = current_row.get('variable', '')

        is_coded = coding_id in st.session_state.coded_ids
        previous_coding = get_previous_coding(coding_id, st.session_state.results) if is_coded else None

        # Two-column layout
        col1, col2 = st.columns([3, 2])

        with col1:
            st.subheader(f"Argument {coding_id}")

            if variable:
                st.caption(f"Economic Variable: **{variable}**")

            if is_coded:
                st.success("Already coded - you can update or skip")

            # Quotation
            st.markdown("**Quotation:**")
            st.markdown(
                f"""<div style="background-color: #f0f2f6; padding: 20px;
                border-radius: 10px; font-size: 16px; line-height: 1.6;">
                {quotation}
                </div>""",
                unsafe_allow_html=True
            )

            # Description (context about what the speaker is discussing)
            if description:
                st.markdown("**Description:**")
                st.markdown(
                    f"""<div style="background-color: #e8eaed; padding: 15px;
                    border-radius: 8px; font-size: 14px; line-height: 1.5; font-style: italic;">
                    {description}
                    </div>""",
                    unsafe_allow_html=True
                )

        with col2:
            st.subheader("Classification")

            st.markdown("""
            **Does this speaker express a belief about how sensitive
            output/growth is to monetary policy?**

            *(The slope of the IS curve - how much does changing interest
            rates affect real economic activity?)*
            """)

            # Get default value from previous coding
            categories = ['flat', 'moderate', 'steep', 'null']
            category_labels = {
                'flat': 'FLAT - Output is HIGHLY SENSITIVE to monetary policy',
                'moderate': 'MODERATE - Qualified/partial transmission from policy to output',
                'steep': 'STEEP - Output is RELATIVELY INSENSITIVE to monetary policy',
                'null': 'NULL - No IS curve slope belief expressed'
            }

            default_idx = 3  # Default to null
            if previous_coding:
                prev_cat = previous_coding.get('classification', 'null')
                if prev_cat in categories:
                    default_idx = categories.index(prev_cat)

            classification = st.radio(
                "Select classification:",
                options=categories,
                format_func=lambda x: category_labels[x],
                index=default_idx,
                key=f"classification_{current_index}_v{v}"
            )

            # Optional notes
            st.markdown("---")
            notes_default = ''
            if previous_coding:
                notes_val = previous_coding.get('notes', '')
                if isinstance(notes_val, str) and pd.notna(notes_val):
                    notes_default = notes_val

            notes = st.text_area(
                "Notes (optional):",
                value=notes_default,
                max_chars=500,
                key=f"notes_{current_index}_v{v}",
                help="Any observations or issues with this argument"
            )

            # Classification guide
            with st.expander("Classification Guide"):
                st.markdown("""
                ## What is the IS Curve Slope?

                The IS curve describes the relationship between monetary policy
                (interest rates) and real economic output/growth. Classify whether
                the speaker believes policy significantly affects output, has
                little effect, or expresses no belief.

                ---

                ### FLAT

                Output is **HIGHLY SENSITIVE** to monetary policy changes.

                **Key indicators:**
                - Causal language: "rate hikes are slowing", "policy is restraining"
                - Traction language: "gaining traction", "working through", "biting"
                - Concern about overtightening: "risk of slowing too much", "could tip into recession"
                - Sector effects: "housing is weakening due to rates"
                - Effectiveness affirmation: "policy is working", "already seeing impact"

                **Examples:**
                - "Our rate increases are clearly slowing interest-sensitive sectors"
                - "Policy tightening is gaining traction and restraining demand"
                - "Further rate hikes risk tipping the economy into recession"
                - "The 200 basis points of easing is providing significant support"

                ---

                ### MODERATE

                **QUALIFIED or PARTIAL** transmission from policy to output.

                **Key indicators:**
                - Hedging: "some", "modest", "incremental", "limited", "to some extent"
                - Mixed channels: works in some sectors but not others
                - Conditionality: "depends on", "in certain circumstances"
                - Weakening transmission: "less than before", "diminished effect"

                **Examples:**
                - "An incremental prod towards activity in the real economy"
                - "Policies contributed to mortgage and auto borrowing, but business investment remained weak"
                - "We see limited passthrough from policy to spending"
                - "Some transmission is occurring, but effects are modest"

                ---

                ### STEEP

                Output is **RELATIVELY INSENSITIVE** to monetary policy changes.

                **Key indicators:**
                - Resilience despite policy: "despite tightening, growth continues"
                - Impairment language: "transmission impaired", "pushing on a string"
                - Skepticism: "less effect than expected", "not seeing impact"
                - Other factors dominate: "fiscal policy driving growth", "structural factors"

                **CRITICAL - "Despite/Even as" construction:**
                - "even with several more rate increases, the economy should expand" -> STEEP
                - "maintained solid momentum even as we reduce accommodation" -> STEEP
                - Key insight: if growth continues regardless of policy direction, output is insensitive

                **Examples:**
                - "Despite 300 basis points of tightening, growth remains above trend"
                - "The economy has proven surprisingly resilient to higher rates"
                - "A further 25 basis point cut will do nothing to change the outlook"

                ---

                ### NULL (default)

                **No IS curve slope belief expressed.**

                Use NULL when:
                - Only mentions policy OR growth (not both connected)
                - Describes data without interpreting policy transmission
                - Discusses policy decisions without mechanism
                - Forecasts growth without linking to policy
                - Focuses on INFLATION channel only, not OUTPUT channel

                **Key distinction - Inflation vs Output:**
                - "Rate hikes will reduce inflation" -> NULL (inflation channel only)
                - "Rate hikes will slow growth and thus reduce inflation" -> FLAT (output explicit)
                - "Tightening will cool demand" -> FLAT (demand = output)

                ---

                ### Critical Disambiguation

                **"Resilient" language:**
                - "solid growth DESPITE tightening" -> STEEP
                - "solid growth BECAUSE of accommodation" -> FLAT
                - "solid growth" (no policy connection) -> NULL

                **Policy preference vs transmission belief:**
                - Focus on TRANSMISSION BELIEF, not policy preference
                - "We should cut because it will boost growth" -> FLAT
                - "We should pause because hikes are already slowing economy" -> FLAT
                - "Cutting won't help - problems aren't monetary" -> STEEP
                - "We can keep tightening - economy is resilient" -> STEEP

                **Lag discussions:**
                - "Effects in 2-3 quarters" -> FLAT (transmission working)
                - "Won't see effects for 2+ years" -> STEEP (weak transmission)
                - "Long and variable lags" without specifics -> NULL

                ---

                *When in doubt, select NULL.*
                """)

        # Navigation
        st.markdown("---")
        col_prev, col_save, col_next, col_jump = st.columns([1, 2, 1, 2])

        with col_prev:
            if st.button("Previous", disabled=(current_index == 0), use_container_width=True):
                st.session_state.current_index -= 1
                st.rerun()

        with col_save:
            if st.button("Save & Continue", type="primary", use_container_width=True):
                # Lock coder name on first save
                if st.session_state.locked_coder_name is None:
                    st.session_state.locked_coder_name = coder_name

                result = {
                    'coding_id': coding_id,
                    'coder_name': st.session_state.locked_coder_name,
                    'classification': classification,
                    'notes': notes,
                    'coded_at': datetime.now().isoformat()
                }

                # Update or append
                existing_idx = None
                for i, r in enumerate(st.session_state.results):
                    if r['coding_id'] == coding_id:
                        existing_idx = i
                        break

                if existing_idx is not None:
                    st.session_state.results[existing_idx] = result
                else:
                    st.session_state.results.append(result)

                st.session_state.coded_ids.add(coding_id)

                st.success(f"Saved! ({len(st.session_state.results)} total)")

                # Move to next
                if current_index < total_arguments - 1:
                    st.session_state.current_index += 1
                    st.rerun()

        with col_next:
            if st.button("Skip", disabled=(current_index == total_arguments - 1), use_container_width=True):
                st.session_state.current_index += 1
                st.rerun()

        with col_jump:
            jump_to = st.number_input(
                "Jump to:",
                min_value=1,
                max_value=total_arguments,
                value=current_index + 1,
                step=1,
                key=f"jump_{current_index}_v{v}"
            )
            if st.button("Go", use_container_width=True):
                st.session_state.current_index = jump_to - 1
                st.rerun()

    else:
        st.success("All arguments have been reviewed!")
        st.info(f"Total coded: {len(st.session_state.coded_ids)} / {total_arguments}")

        st.markdown("### Download your results:")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = coder_name.lower().replace(' ', '_')
        filename = f"coded_{safe_name}_is_slope_{timestamp}.csv"

        st.download_button(
            label="Download Results CSV",
            data=get_results_csv(st.session_state.results, coding_df),
            file_name=filename,
            mime="text/csv",
            type="primary"
        )

        if st.button("Return to Start"):
            st.session_state.current_index = 0
            st.rerun()


if __name__ == "__main__":
    main()
