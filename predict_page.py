import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    # Import and apply the dropdown fix
    from fix_dropdowns import fix_dropdowns
    fix_dropdowns()

    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")


    countries = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )

    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )

    # Add custom styling for the dropdowns
    st.markdown("""
    <style>
    /* Ensure country and education dropdowns are clearly visible */
    div[data-testid="stSelectbox"] > div[data-baseweb="select"] {
        background-color: #ffffff !important;
        border: 2px solid #3b82f6 !important;
    }

    div[data-testid="stSelectbox"] > div[data-baseweb="select"] span {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* Make dropdown menu items visible */
    div[data-baseweb="popover"] div[data-baseweb="menu"] {
        background-color: #ffffff !important;
    }

    div[data-baseweb="popover"] div[data-baseweb="menu"] ul {
        background-color: #ffffff !important;
    }

    div[data-baseweb="popover"] div[data-baseweb="menu"] li {
        color: #000000 !important;
        background-color: #ffffff !important;
    }

    /* Fix for dropdown option text */
    div[role="listbox"] ul li {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Add a container with custom styling for the country dropdown
    with st.container():
        country = st.selectbox("Country", countries)

    education = st.selectbox("Education Level", education)
    job_title = st.text_input("Job Title", "Software Developer")
    industry = st.selectbox("Industry", ["Tech", "Finance", "Healthcare", "Education", "Other"])


    expericence = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button("Calculate Salary")
    st.write("### Additional Information")
    st.write(f"Job Title: {job_title}")
    st.write(f"Industry: {industry}")

    if ok:
        X = np.array([[country, education, expericence ]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X = X.astype(float)

        salary = regressor.predict(X)
        annual_salary = salary[0]
        monthly_salary = annual_salary / 12
        hourly_salary = annual_salary / (52 * 40)  # Assuming 52 weeks per year and 40 hours per week

        # Display the salary information with a nice format
        st.subheader("Salary Breakdown")

        # Create columns for better layout
        col1, col2 = st.columns(2)

        with col1:
            st.metric(label="Annual Salary", value=f"${annual_salary:.2f}")
            st.metric(label="Monthly Salary", value=f"${monthly_salary:.2f}")

        with col2:
            st.metric(label="Hourly Rate", value=f"${hourly_salary:.2f}")
            st.metric(label="Weekly Salary", value=f"${annual_salary/52:.2f}")

        # Add some additional context
        st.info("""
        💡 **Note:**
        - Monthly salary is calculated by dividing annual salary by 12 months
        - Hourly rate is calculated based on a 40-hour work week
        - Actual take-home pay may vary based on taxes and other deductions
        """)

        # Add a visual separator
        st.markdown("---")

        # Add a visual representation of the salary breakdown
        st.subheader("Salary Visualization")

        # Create data for the chart
        import pandas as pd

        # Calculate values for visualization
        take_home = monthly_salary * 0.65
        taxes = monthly_salary * 0.25
        benefits = monthly_salary * 0.10

        # Create a DataFrame for the chart
        chart_data = pd.DataFrame({
            'Amount': [take_home, taxes, benefits],
            'Category': ['Take Home Pay', 'Taxes (est.)', 'Benefits (est.)']
        })

        # Display the bar chart
        st.bar_chart(chart_data, y='Amount')

        # Add explanation of the visualization
        st.caption("""
        This is an estimated breakdown of a typical monthly salary.
        Actual values may vary based on your location, tax bracket, and employer benefits.
        """)

        # Add salary comparison section
        st.markdown("---")
        st.subheader("Salary Comparison")

        # Create a simple comparison with industry averages (these are example values)
        industry_averages = {
            "Tech": 95000,
            "Finance": 105000,
            "Healthcare": 85000,
            "Education": 75000,
            "Other": 80000
        }

        # Get the average for the selected industry
        selected_industry_avg = industry_averages.get(industry, 85000)

        # Calculate the difference
        difference = annual_salary - selected_industry_avg
        percentage_diff = (difference / selected_industry_avg) * 100

        # Display the comparison
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label=f"Average {industry} Industry Salary",
                value=f"${selected_industry_avg:,.2f}"
            )

        with col2:
            st.metric(
                label="Your Predicted Salary",
                value=f"${annual_salary:,.2f}",
                delta=f"{percentage_diff:+.1f}% vs industry average"
            )

        # Add context about the comparison
        if percentage_diff > 0:
            st.success(f"Your predicted salary is ${difference:,.2f} higher than the industry average!")
        elif percentage_diff < 0:
            st.warning(f"Your predicted salary is ${abs(difference):,.2f} lower than the industry average.")
        else:
            st.info("Your predicted salary matches the industry average.")

        # Add future salary projection section
        st.markdown("---")
        st.subheader("Future Salary Projection")

        # Calculate projected salaries for the next 5 years (assuming 5% annual growth)
        years = list(range(1, 6))
        projected_salaries = [annual_salary * (1.05 ** year) for year in years]

        # Create a DataFrame for the projection chart
        projection_data = pd.DataFrame({
            'Year': [f"Year {year}" for year in years],
            'Projected Salary': projected_salaries
        })

        # Display the projection chart
        st.line_chart(projection_data, x='Year', y='Projected Salary')

        # Add explanation of the projection
        st.caption("""
        This projection assumes an average annual salary growth of 5%.
        Actual growth may vary based on performance, industry trends, and economic factors.
        """)

        # Add tips for salary negotiation
        st.markdown("### 💡 Tips for Salary Negotiation")
        st.markdown("""
        - Research the salary range for your position in your location
        - Highlight your unique skills and experience during negotiations
        - Consider the total compensation package, not just the base salary
        - Be prepared to discuss your achievements and value to the company
        - Practice your negotiation conversation beforehand
        """)
