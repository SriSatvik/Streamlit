import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import time
import numpy as np

#set page
st.set_page_config(page_title="BMI Calaculator",page_icon="📊",layout="wide")
# Title
st.title("💪 Interactive BMI Visualizer ")

st.write("This app calculates your **BMI** and shows it dynamically ")

# User inputs
weight = st.number_input("Enter your weight (kg)", step=0.5)
height = st.number_input("Enter your height (cm)",  step=0.5)

if st.button("Calculate BMI"):
    if height > 0:
        bmi = weight / ((height/100) ** 2)
        st.success(f"Your BMI is: {bmi:.2f}")

        # BMI ranges, colors, categories
        bmi_ranges = [0, 18.5, 25, 30, 70]
        colors = ["yellow", "green", "orange", "red"]
        categories = ["Underweight", "Normal", "Overweight", "Obese"]
        
        if bmi > 70: # Check for potentially wrong input resulting in high BMI
            st.error("You have entered wrong values. Please check your weight and height.")
            st.stop() # Stop execution if values are absurd

        # Determine user category
        user_category = ""
        user_color = ""
        lower_bound = 0
        upper_bound = 0
        for i in range(len(bmi_ranges)-1):
            if bmi < bmi_ranges[i+1]:
                user_category = categories[i]
                user_color = colors[i]
                lower_bound = bmi_ranges[i]
                upper_bound = bmi_ranges[i+1]
                break

        st.write(f"📊 Category: **{user_category}**")

        # ---- Setup Figure ----
        fig, ax = plt.subplots(figsize=(10, 3))

        # Draw category bar above chart
        for i in range(len(colors)):
            ax.barh(1, bmi_ranges[i+1]-bmi_ranges[i], left=bmi_ranges[i],
                    color=colors[i], edgecolor='black', height=0.3)
            # ax.text((bmi_ranges[i]+bmi_ranges[i+1])/2, 1, categories[i],
                    # ha='center', va='top', fontsize=10, fontweight='bold', color='black')

        # Formatting
        ax.set_xlim(0, 70)
        ax.set_ylim(-0.5, 1.5)
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["Your BMI", "BMI Categories"])
        ax.set_xlabel("BMI Value")

        # Create legend with colors
        legend_elements = [Patch(facecolor=colors[i], edgecolor='black', label=categories[i]) for i in range(len(categories))]
        legend_elements.append(plt.Line2D([0], [0], marker='o', color='k', label=f'Your BMI: {bmi:.1f}', markersize=10, linestyle=''))
        ax.legend(handles=legend_elements, loc="upper center", bbox_to_anchor=(0.5, 1.4), ncol=5)

        # ---- Animation of BMI bar ----
        bmi_steps = np.linspace(lower_bound, bmi, 50)  # 50 steps for smooth animation
        
        # Initialize bar and marker
        bmi_bar = ax.barh(0, 0, left=lower_bound, color=user_color, alpha=0.3)  # initial bar
        marker, = ax.plot(lower_bound, 0, "ko", markersize=12)  # initial marker

        # Use an empty Streamlit container to update the plot
        plot_placeholder = st.empty()

        for val in bmi_steps:
            bmi_bar[0].set_width(val - lower_bound)  # update bar width
            marker.set_data([val],[0])  # Update both x and y data for the marker
            
            # Re-render the plot in Streamlit
            with plot_placeholder.container():
                st.pyplot(fig)
            time.sleep(0.02)  # small delay for animation

        plt.close(fig) # Close the figure to prevent Matplotlib warning

    else:
        st.error("Height must be greater than 0!")
