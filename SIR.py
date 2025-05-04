import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="SIR Simulation",
    page_icon="🧪",               
)

st.title("SIR Model - Epidemic Spread Simulation")

st.write("""
This SIR model simulates the spread of an epidemic like the coronavirus.
You can adjust the parameters or choose predefined scenarios to observe their effects.
""")

# Sidebar parameters
st.sidebar.header("Model Parameters")

N = st.sidebar.number_input("Total population (N)", value=1000, min_value=100, max_value=1000000)

# Predefined scenarios
scenario = st.sidebar.selectbox("Scenario", [
    "Custom",
    "Strict lockdown",
    "No measures",
    "Progressive vaccination"
])

# Default values based on scenario
if scenario == "Strict lockdown":
    beta_def = 0.2
    gamma_def = 0.2
    mu_def = 0.01
elif scenario == "No measures":
    beta_def = 0.7
    gamma_def = 0.1
    mu_def = 0.02
elif scenario == "Progressive vaccination":
    beta_def = 0.5
    gamma_def = 0.15
    mu_def = 0.015
else:  # Custom
    beta_def = 0.3
    gamma_def = 0.05
    mu_def = 0.02

# Always visible sliders with defaults based on scenario
beta = st.sidebar.slider("Transmission rate (β)", 0.0, 1.0, beta_def, 0.01)
gamma = st.sidebar.slider("Recovery rate (γ)", 0.0, 1.0, gamma_def, 0.01)
mu = st.sidebar.slider("Mortality rate (μ)", 0.0, 0.1, mu_def, 0.001)

# Optional no-mortality setting
no_mortality = st.sidebar.checkbox("Ignore mortality (μ=0)", value=False)
if no_mortality:
    mu = 0.0

# Duration of the simulation
days = st.sidebar.slider("Simulation duration (days)", 1, 365, 160)

# Initial conditions
I0 = st.sidebar.slider("Initial number of infected (I₀)", 1, N, 1)
S0 = N - I0
R0 = 0
D0 = 0

# SIRD model function
def SIR_model(y, t, N, beta, gamma, mu):
    S, I, R, D = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I - mu * I
    dRdt = gamma * I
    dDdt = mu * I
    return dSdt, dIdt, dRdt, dDdt

# Time grid
t = np.linspace(0, days, days * 10)  # 10 points per day

# Solving the differential equations
y0 = S0, I0, R0, D0
sol = odeint(SIR_model, y0, t, args=(N, beta, gamma, mu))
S, I, R, D = sol.T

# Peak infection stats
max_infected = np.max(I)
day_of_peak = t[np.argmax(I)]

# Effective reproduction rate Rₑ(t)
Re = (beta / (gamma + mu)) * (S / N)

# Display results
st.subheader("Simulation Results")

# Plot: S, I, R, D
# Create interactive SIRD plot
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(go.Scatter(x=t, y=S, name='Susceptible', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=t, y=I, name='Infected', line=dict(color='red')))
fig.add_trace(go.Scatter(x=t, y=R, name='Recovered', line=dict(color='green')))
if not no_mortality:
    fig.add_trace(go.Scatter(x=t, y=D, name='Deceased', line=dict(color='black')))

# Add peak infection marker
fig.add_trace(go.Scatter(
    x=[day_of_peak], 
    y=[max_infected],
    mode='markers',
    marker=dict(size=10, color='red', symbol='star'),
    name='Peak Infection',
    hoverinfo='text',
    text=f'Peak: {int(max_infected)} on day {int(day_of_peak)}'
))

fig.update_layout(
    title=f'SIR{"D" if not no_mortality else ""} Model - {scenario}',
    xaxis_title='Time (days)',
    yaxis_title='Number of people',
    hovermode='x unified',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
)

st.plotly_chart(fig, use_container_width=True)

# Plot: Rₑ(t)
fig2 = make_subplots()
fig2.add_trace(go.Scatter(x=t, y=Re, name="Rₑ(t)", line=dict(color='purple')))
fig2.add_shape(type="line", line=dict(dash="dash", color="gray", width=1.5), x0=0, y0=1, x1=days, y1=1)
fig2.add_annotation(x=days/4, y=1.05, text="Epidemic threshold (Rₑ = 1)", showarrow=False, font=dict(color="gray"))
fig2.update_layout(
    title="Effective Reproduction Number (Rₑ)",
    xaxis_title='Time (days)',
    yaxis_title='Rₑ(t)',
    hovermode='x unified',
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
)

st.plotly_chart(fig2, use_container_width=True)



# Numeric summaries
st.write(f"**Final number of susceptible:** {int(S[-1])}")
st.write(f"**Final number of infected:** {int(I[-1])}")
st.write(f"**Final number of recovered:** {int(R[-1])}")
if not no_mortality:
    st.write(f"**Final number of deceased:** {int(D[-1])}")
st.write(f"**Peak infection:** {int(max_infected)} infected on day {int(day_of_peak)}")
st.write(f"**Final attack rate:** {round((1 - S[-1]/N)*100, 2)}% of the population")

# Sidebar explanation
st.sidebar.write("""
### Parameter Explanation:
- **β (Transmission rate)**: Probability of disease transmission per contact.
- **γ (Recovery rate)**: Rate at which infected individuals recover.
- **μ (Mortality rate)**: Rate at which infected individuals die.
""")
