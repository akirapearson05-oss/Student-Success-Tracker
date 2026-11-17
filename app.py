
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Student Success Tracker",
    page_icon="📚",
    layout="wide"
)


with open("style.css", "r") as css_file:
    css = css_file.read()

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.title("📚 Student Success Tracker")
st.write("Your academic progress, organized in one place.")

# Sample data
sample_data = [
    {"Student": "S001", "Course": "Accounting",
     "Average_Grade": 82, "Study_Hours": 5,
     "Missing_Assignments": 1},
    {"Student": "S001", "Course": "Statistics",
     "Average_Grade": 75, "Study_Hours": 4,
     "Missing_Assignments": 2},
    {"Student": "S002", "Course": "Accounting",
     "Average_Grade": 91, "Study_Hours": 7,
     "Missing_Assignments": 0},
    {"Student": "S002", "Course": "Statistics",
     "Average_Grade": 86, "Study_Hours": 6,
     "Missing_Assignments": 1},
    {"Student": "S003", "Course": "Accounting",
     "Average_Grade": 68, "Study_Hours": 3,
     "Missing_Assignments": 3},
    {"Student": "S003", "Course": "Statistics",
     "Average_Grade": 72, "Study_Hours": 4,
     "Missing_Assignments": 2}
]

if "student_data" not in st.session_state:
    st.session_state.student_data = sample_data.copy()

# Add student information
st.sidebar.header("Add Student Record")

with st.sidebar.form("student_form"):
    student_id = st.text_input("Student ID", value="S004")
    course = st.selectbox(
        "Course",
        ["Accounting", "Statistics", "Economics",
         "Finance", "Marketing", "Other"]
    )
    if course == "Other":
        course = st.text_input("Enter course name")

    grade = st.number_input(
        "Average Grade (%)", min_value=0.0,
        max_value=100.0, value=80.0
    )
    hours = st.number_input(
        "Study Hours per Week", min_value=0.0,
        max_value=168.0, value=5.0
    )
    missing = st.number_input(
        "Missing Assignments", min_value=0,
        step=1, value=0
    )

    submitted = st.form_submit_button("Add Student Record")

if submitted:
    if not student_id.strip() or not course.strip():
        st.sidebar.error("Enter a student ID and course.")
    else:
        st.session_state.student_data.append({
            "Student": student_id.strip(),
            "Course": course.strip(),
            "Average_Grade": grade,
            "Study_Hours": hours,
            "Missing_Assignments": int(missing)
        })
        st.sidebar.success("Student record added!")
        st.rerun()

df = pd.DataFrame(st.session_state.student_data)

st.caption(
    "Demonstration project using fictional sample data. "
    "Records entered here are kept for this active session."
)

# Dashboard
st.subheader("📊 Academic Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Overall Average Grade",
    f"{df['Average_Grade'].mean():.1f}%"
)
col2.metric(
    "Average Study Hours",
    f"{df['Study_Hours'].mean():.1f} hrs/week"
)
col3.metric(
    "Missing Assignments",
    int(df["Missing_Assignments"].sum())
)

st.divider()

# Course analysis
st.subheader("📚 Average Grade by Course")

course_averages = df.groupby("Course")["Average_Grade"].mean()
st.bar_chart(course_averages)

# Study analysis
st.subheader("⏰ Study Hours vs. Grades")

st.scatter_chart(
    df,
    x="Study_Hours",
    y="Average_Grade",
    color="Course"
)

# Missing assignments
st.subheader("📝 Missing Assignments by Course")

missing_by_course = df.groupby("Course")[
    "Missing_Assignments"
].sum()
st.bar_chart(missing_by_course)

# Recommendations
st.subheader("💡 Student Success Insights")

lowest_course = course_averages.idxmin()
lowest_grade = course_averages.min()
highest_course = course_averages.idxmax()
highest_grade = course_averages.max()

st.write(
    f"**Course needing the most attention:** {lowest_course} "
    f"({lowest_grade:.1f}% average)"
)
st.write(
    f"**Highest-performing course:** {highest_course} "
    f"({highest_grade:.1f}% average)"
)

if lowest_grade < 80:
    st.info(
        f"Consider reviewing study strategies for {lowest_course}."
    )
else:
    st.success("All course averages are at least 80%.")

if df["Missing_Assignments"].sum() > 0:
    st.warning(
        "Review missing assignments and plan time to complete them."
    )
else:
    st.success("No missing assignments are recorded.")

# View and download records
with st.expander("View All Student Records"):
    st.dataframe(df, use_container_width=True)

csv_data = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Student Data (CSV)",
    data=csv_data,
    file_name="student_success_data.csv",
    mime="text/csv"
)