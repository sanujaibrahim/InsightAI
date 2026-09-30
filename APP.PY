import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="InsightAI",
    page_icon="📊",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.kpi {
    padding: 20px;
    border-radius: 12px;
    background-color: #f5f7fa;
    text-align: center;
    border: 1px solid #e0e0e0;
}

.kpi h2 {
    margin: 0;
    font-size: 28px;
}

.kpi p {
    margin: 5px;
    color: #666;
}

.card {
    padding: 18px;
    border-radius: 12px;
    background-color: #f8f9fa;
    border: 1px solid #e2e2e2;
    margin-bottom: 15px;
}

.decision {
    padding: 20px;
    border-radius: 12px;
    background-color: #f5f7fa;
    border-left: 5px solid #555;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 InsightAI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Data Explorer",
        "AI Insights",
        "Ask InsightAI",
        "Future Decision Support"
    ]
)

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV Dataset",
    type=["csv"]
)


# ---------------- LOAD DATA ----------------
if uploaded_file is None:

    st.title("📊 InsightAI")
    st.subheader("AI-Powered CSV Data Insight Assistant")

    st.info("Please upload a CSV file from the sidebar.")

    st.markdown("""
    ### How InsightAI works

    **1. Upload CSV → 2. Explore Data → 3. AI Insights →  
    4. Ask Questions → 5. Future Decision Support**
    """)

    st.stop()


# ---------------- READ CSV ----------------
try:
    df = pd.read_csv(uploaded_file)

except Exception as e:
    st.error(f"Unable to read the CSV file: {e}")
    st.stop()


# Remove spaces from column names
df.columns = df.columns.astype(str).str.strip()


# =========================================================
# IMPORTANT: NUMERIC COLUMN DETECTION
# =========================================================

numeric_data = {}

for column in df.columns:

    # Remove common symbols such as $, %, commas
    cleaned = (
        df[column]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.strip()
    )

    converted = pd.to_numeric(cleaned, errors="coerce")

    # If at least 50% of values are numeric,
    # treat the column as numeric
    if converted.notna().sum() >= max(1, len(df) * 0.50):
        numeric_data[column] = converted


numeric_df = pd.DataFrame(numeric_data)

numeric_columns = list(numeric_data.keys())


# =========================================================
# PAGE 1 - DASHBOARD
# =========================================================

if page == "Dashboard":

    st.title("📊 InsightAI Dashboard")
    st.caption("Interactive overview of your dataset")

    # KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="kpi">
                <h2>{len(df):,}</h2>
                <p>Total Rows</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="kpi">
                <h2>{len(df.columns)}</h2>
                <p>Total Columns</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        missing = int(df.isnull().sum().sum())

        st.markdown(
            f"""
            <div class="kpi">
                <h2>{missing:,}</h2>
                <p>Missing Values</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        duplicates = int(df.duplicated().sum())

        st.markdown(
            f"""
            <div class="kpi">
                <h2>{duplicates:,}</h2>
                <p>Duplicate Rows</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    # Filters
    st.subheader("🔎 Filters")

    filter_col1, filter_col2 = st.columns(2)

    categorical_columns = [
        col for col in df.columns
        if col not in numeric_columns
    ]

    selected_filter = None

    with filter_col1:

        if categorical_columns:

            selected_filter = st.selectbox(
                "Select Filter",
                categorical_columns
            )

    filtered_df = df.copy()

    with filter_col2:

        if selected_filter:

            values = filtered_df[selected_filter].dropna().unique()

            selected_value = st.selectbox(
                "Select Value",
                ["All"] + list(map(str, values))
            )

            if selected_value != "All":
                filtered_df = filtered_df[
                    filtered_df[selected_filter].astype(str)
                    == selected_value
                ]

    st.write(
        f"Showing **{len(filtered_df):,} rows**"
    )

    # Charts
    st.subheader("📈 Visual Analytics")

    if len(numeric_columns) > 0:

        chart1, chart2 = st.columns(2)

        with chart1:

            column1 = st.selectbox(
                "Chart 1 - Select Numeric Column",
                numeric_columns,
                key="chart1"
            )

            fig1 = px.histogram(
                filtered_df,
                x=column1,
                title=f"{column1} Distribution"
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

        with chart2:

            column2 = st.selectbox(
                "Chart 2 - Select Numeric Column",
                numeric_columns,
                key="chart2"
            )

            temp = filtered_df[[column2]].copy()

            fig2 = px.box(
                temp,
                y=column2,
                title=f"{column2} Analysis"
            )

            st.plotly_chart(
                fig2,
                use_container_width=True
            )

        chart3, chart4 = st.columns(2)

        with chart3:

            selected_bar = st.selectbox(
                "Chart 3 - Numeric Column",
                numeric_columns,
                key="chart3"
            )

            fig3 = px.bar(
                filtered_df.head(20),
                y=selected_bar,
                title=f"Top Records - {selected_bar}"
            )

            st.plotly_chart(
                fig3,
                use_container_width=True
            )

        with chart4:

            selected_line = st.selectbox(
                "Chart 4 - Numeric Column",
                numeric_columns,
                key="chart4"
            )

            fig4 = px.line(
                filtered_df.head(50),
                y=selected_line,
                title=f"{selected_line} Trend"
            )

            st.plotly_chart(
                fig4,
                use_container_width=True
            )

    else:

        st.warning(
            "No numeric columns were detected in this dataset."
        )


# =========================================================
# PAGE 2 - DATA EXPLORER
# =========================================================

elif page == "Data Explorer":

    st.title("🔍 Data Explorer")

    st.subheader("Dataset Preview")

    search = st.text_input(
        "Search inside dataset"
    )

    display_df = df.copy()

    if search:

        mask = display_df.astype(str).apply(
            lambda row: row.str.contains(
                search,
                case=False,
                na=False
            ).any(),
            axis=1
        )

        display_df = display_df[mask]

    st.dataframe(
        display_df,
        use_container_width=True
    )

    st.divider()

    st.subheader("📋 Column Information")

    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str).values,
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    })

    st.dataframe(
        column_info,
        use_container_width=True
    )

    st.divider()

    st.subheader("📊 Statistical Summary")

    if numeric_columns:

        stats = numeric_df.describe().T

        stats = stats.round(2)

        st.dataframe(
            stats,
            use_container_width=True
        )

    else:

        st.info("No numerical columns available.")


# =========================================================
# PAGE 3 - AI INSIGHTS
# =========================================================

elif page == "AI Insights":

    st.title("🤖 AI Insights")

    st.caption(
        "Automatically generated insights from your dataset"
    )

    # DEBUG / STATUS
    st.success(
        f"✅ {len(numeric_columns)} numerical columns detected"
    )

    if numeric_columns:

        st.write(
            "**Detected numerical columns:**",
            ", ".join(numeric_columns)
        )

        st.divider()

        # Generate insights
        for column in numeric_columns:

            values = numeric_data[column].dropna()

            if len(values) == 0:
                continue

            total = values.sum()
            average = values.mean()
            median = values.median()
            maximum = values.max()
            minimum = values.min()
            std = values.std()

            max_index = values.idxmax()
            min_index = values.idxmin()

            max_row = df.loc[max_index]
            min_row = df.loc[min_index]

            st.subheader(f"📌 {column}")

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric(
                    "Total",
                    f"{total:,.2f}"
                )

            with c2:
                st.metric(
                    "Average",
                    f"{average:,.2f}"
                )

            with c3:
                st.metric(
                    "Highest",
                    f"{maximum:,.2f}"
                )

            with c4:
                st.metric(
                    "Lowest",
                    f"{minimum:,.2f}"
                )

            # Automatic interpretation
            if maximum > average:
                high_text = (
                    f"The highest value is {maximum:,.2f}, "
                    f"which is above the average of {average:,.2f}."
                )
            else:
                high_text = (
                    f"The highest value is {maximum:,.2f}."
                )

            if minimum < average:
                low_text = (
                    f"The lowest value is {minimum:,.2f}, "
                    f"which is below the average."
                )
            else:
                low_text = (
                    f"The lowest value is {minimum:,.2f}."
                )

            st.markdown(
                f"""
                <div class="card">
                <b>AI Interpretation</b><br><br>

                • {high_text}<br>

                • {low_text}<br>

                • Median value is {median:,.2f}.<br>

                • Variation in the data is
                {std:,.2f}.<br>

                • The record with the highest value
                occurs at row {max_index + 1}.<br>

                • The record with the lowest value
                occurs at row {min_index + 1}.
                </div>
                """,
                unsafe_allow_html=True
            )

        # ---------------- DATA QUALITY ----------------

        st.divider()

        st.subheader("🛡️ Data Quality Findings")

        missing_total = int(
            df.isnull().sum().sum()
        )

        duplicate_total = int(
            df.duplicated().sum()
        )

        q1, q2, q3 = st.columns(3)

        with q1:
            st.metric(
                "Missing Values",
                missing_total
            )

        with q2:
            st.metric(
                "Duplicate Rows",
                duplicate_total
            )

        with q3:
            st.metric(
                "Columns",
                len(df.columns)
            )

        if missing_total > 0:

            st.warning(
                f"⚠️ The dataset contains "
                f"{missing_total} missing values. "
                "Data cleaning is recommended."
            )

        else:

            st.success(
                "✅ No missing values detected."
            )

        if duplicate_total > 0:

            st.warning(
                f"⚠️ {duplicate_total} duplicate rows detected."
            )

        else:

            st.success(
                "✅ No duplicate rows detected."
            )

        # ---------------- CORRELATION ----------------

        if len(numeric_columns) >= 2:

            st.divider()

            st.subheader("🔗 Relationship Between Variables")

            correlation = numeric_df.corr()

            fig_corr = px.imshow(
                correlation,
                text_auto=True,
                title="Correlation Matrix"
            )

            st.plotly_chart(
                fig_corr,
                use_container_width=True
            )

    else:

        st.error(
            "❌ No numerical columns were detected."
        )

        st.info(
            "Your CSV should contain columns such as "
            "Sales, Revenue, Profit, Quantity, Age, Marks, etc."
        )


# =========================================================
# PAGE 4 - ASK INSIGHTAI
# =========================================================

elif page == "Ask InsightAI":

    st.title("💬 Ask InsightAI")

    st.write(
        "Ask questions about your uploaded dataset."
    )

    st.info("""
    Example questions:

    • How many rows?

    • How many columns?

    • What is the average Sales?

    • What is the highest Profit?

    • What is the lowest Sales?

    • Which columns are available?
    """)

    question = st.text_input(
        "Ask your question"
    )

    if question:

        q = question.lower()

        answered = False

        # ROWS
        if "row" in q:

            st.success(
                f"Your dataset contains **{len(df):,} rows**."
            )

            answered = True

        # COLUMNS
        elif "column" in q:

            st.success(
                f"Your dataset contains **{len(df.columns)} columns**."
            )

            answered = True

        # MISSING
        elif "missing" in q:

            missing = int(
                df.isnull().sum().sum()
            )

            st.success(
                f"Your dataset contains **{missing} missing values**."
            )

            answered = True

        # NUMERIC COLUMN QUESTIONS
        else:

            for column in numeric_columns:

                if column.lower() in q:

                    values = numeric_data[column].dropna()

                    if "average" in q or "mean" in q:

                        st.success(
                            f"Average {column}: "
                            f"**{values.mean():,.2f}**"
                        )

                        answered = True

                    elif (
                        "highest" in q
                        or "maximum" in q
                        or "max" in q
                    ):

                        st.success(
                            f"Highest {column}: "
                            f"**{values.max():,.2f}**"
                        )

                        answered = True

                    elif (
                        "lowest" in q
                        or "minimum" in q
                        or "min" in q
                    ):

                        st.success(
                            f"Lowest {column}: "
                            f"**{values.min():,.2f}**"
                        )

                        answered = True

                    break

        if not answered:

            st.warning(
                "I could not understand that question. "
                "Try one of the example questions."
            )


# =========================================================
# PAGE 5 - FUTURE DECISION SUPPORT
# =========================================================

elif page == "Future Decision Support":

    st.title("🔮 Future Decision Support")

    st.caption(
        "Data-based decision support generated from the dataset"
    )

    if not numeric_columns:

        st.error(
            "No numerical data available for decision support."
        )

        st.info(
            "Upload a dataset containing numerical columns."
        )

    else:

        # Select the main business metric
        selected_metric = st.selectbox(
            "Select the main business metric",
            numeric_columns
        )

        values = numeric_data[selected_metric].dropna()

        # Basic calculations
        total_value = values.sum()
        average_value = values.mean()
        maximum_value = values.max()
        minimum_value = values.min()

        # Missing values
        missing_count = int(
            df[selected_metric].isnull().sum()
        )

        # Duplicate rows
        duplicate_count = int(
            df.duplicated().sum()
        )

        # Trend
        if len(values) >= 2:

            first_value = values.iloc[0]
            last_value = values.iloc[-1]

            if last_value > first_value:

                trend = "Increasing"

            elif last_value < first_value:

                trend = "Decreasing"

            else:

                trend = "Stable"

        else:

            trend = "Insufficient data"

        # Variation
        if average_value != 0:

            variation = (
                values.std() / abs(average_value)
            ) * 100

        else:

            variation = 0

        # Risk
        if missing_count > 0:

            risk = "Data Quality Risk"

        elif variation > 50:

            risk = "High Variation Risk"

        elif duplicate_count > 0:

            risk = "Duplicate Data Risk"

        else:

            risk = "Low Data Risk"

        # Recommended action
        if trend == "Decreasing":

            action = (
                f"Investigate the reasons behind the decline "
                f"in {selected_metric} and identify areas "
                "requiring improvement."
            )

        elif trend == "Increasing":

            action = (
                f"Monitor the growth in {selected_metric} "
                "and identify the factors contributing "
                "to the positive trend."
            )

        else:

            action = (
                f"Monitor {selected_metric} regularly and "
                "look for opportunities to improve performance."
            )

        # Focus area
        if variation > 50:

            focus = (
                "Focus on reducing large fluctuations "
                "and improving consistency."
            )

        elif missing_count > 0:

            focus = (
                "Focus on improving data quality "
                "and completing missing information."
            )

        else:

            focus = (
                f"Focus on maintaining and improving "
                f"{selected_metric} performance."
            )

        # =================================================
        # DISPLAY VALUES
        # =================================================

        st.subheader(
            f"📊 Decision Analysis: {selected_metric}"
        )

        d1, d2, d3, d4 = st.columns(4)

        with d1:
            st.metric(
                "Total",
                f"{total_value:,.2f}"
            )

        with d2:
            st.metric(
                "Average",
                f"{average_value:,.2f}"
            )

        with d3:
            st.metric(
                "Highest",
                f"{maximum_value:,.2f}"
            )

        with d4:
            st.metric(
                "Lowest",
                f"{minimum_value:,.2f}"
            )

        st.divider()

        # TREND
        st.subheader("📈 Business Trend")

        st.info(
            f"**{selected_metric} Trend: {trend}**"
        )

        st.write(
            f"First recorded value: "
            f"**{first_value:,.2f}**"
        )

        st.write(
            f"Latest recorded value: "
            f"**{last_value:,.2f}**"
        )

        # RISK
        st.subheader("⚠️ Risk / Problem")

        st.warning(
            f"**{risk}**"
        )

        if missing_count > 0:

            st.write(
                f"Missing values in {selected_metric}: "
                f"**{missing_count}**"
            )

        if duplicate_count > 0:

            st.write(
                f"Duplicate rows: **{duplicate_count}**"
            )

        st.write(
            f"Variation: **{variation:.2f}%**"
        )

        # ACTION
        st.subheader("🎯 Recommended Action")

        st.success(
            action
        )

        # FOCUS
        st.subheader("🔍 Expected Focus Area")

        st.info(
            focus
        )

        # SUMMARY
        st.subheader("🧠 Decision-Support Summary")

        st.markdown(
            f"""
            <div class="decision">

            <b>Business Metric:</b>
            {selected_metric}

            <br><br>

            <b>Current Trend:</b>
            {trend}

            <br><br>

            <b>Average Performance:</b>
            {average_value:,.2f}

            <br><br>

            <b>Risk:</b>
            {risk}

            <br><br>

            <b>Recommended Action:</b>
            {action}

            <br><br>

            <b>Focus Area:</b>
            {focus}

            </div>
            """,
            unsafe_allow_html=True
        )

        # TREND CHART
        st.subheader("📉 Metric Trend")

        trend_df = pd.DataFrame({
            "Record": range(1, len(values) + 1),
            selected_metric: values.values
        })

        fig = px.line(
            trend_df,
            x="Record",
            y=selected_metric,
            markers=True,
            title=f"{selected_metric} Trend"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# FOOTER
# =========================================================

st.sidebar.divider()

st.sidebar.caption(
    "InsightAI | AI-Powered Data Analysis"
)