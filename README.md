# SIR Model - Epidemic Spread Simulation

## Description
This is a Streamlit-based simulation of an SIR (Susceptible, Infected, Recovered) model for epidemic spread, like the coronavirus. Users can adjust parameters such as transmission rate, recovery rate, and mortality rate, and choose predefined scenarios to observe the effect of different measures (e.g., lockdown, vaccination).

[Try the SIR Simulation App](https://sir-epidemic-simulation.streamlit.app)

## Features
- Interactive plot of SIR (or SIRD) model with configurable parameters.
- Simulation of various scenarios: strict lockdown, no measures, and progressive vaccination.
- Visualization of the effective reproduction rate (Rₑ(t)).
- Numerical summaries of the simulation (e.g., peak infection, final number of infected, recovered, and deceased).

## Installation

To run this project locally, you need to install the necessary dependencies. Create a Python virtual environment and install the dependencies from `requirements.txt`.

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/sir-epidemic-simulation.git
    cd sir-epidemic-simulation
    ```

2. Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Usage
Run the Streamlit Application:
To start the simulation, run the following command:

```bash
streamlit run app.py
```

This will launch a local Streamlit server, and you can interact with the SIR model in your web browser at:

http://localhost:8501

## Adjust Model Parameters:

- Use the sidebar to adjust the model parameters, such as the transmission rate (β), recovery rate (γ), and mortality rate (μ).

- You can also select from predefined scenarios like "Strict lockdown" or "No measures."

## Interpret Results:
- The simulation will plot the time evolution of the epidemic, including:

- The number of susceptible, infected, recovered, and deceased individuals.

- The effective reproduction rate (Rₑ), which is an important indicator of the epidemic's potential to spread.

- The peak infection and final attack rate at the end of the simulation.

## Predefined Scenarios
- Strict lockdown: Low transmission rate, high recovery rate, moderate mortality.

- No measures: High transmission rate, low recovery rate, higher mortality.

- Progressive vaccination: Medium transmission rate, moderate recovery rate, lower mortality rate.

- Custom: Define your own parameters for transmission, recovery, and mortality rates.

## Contributing
Feel free to fork this repository and submit pull requests if you have improvements or bug fixes.

## License
This project is open-source and available under the MIT License.


