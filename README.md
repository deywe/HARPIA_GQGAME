HARPIA :: QUANTUM FIELD DUEL

The HARPIA :: QUANTUM FIELD DUEL is an experimental physics-based game that integrates quantum computing logic (via Google Cirq) with real-time distributed optimization. The game uses thermal noise parameters to influence the ball's trajectory, connecting to a remote kernel to dynamically adjust the game's physics.
🚀 Key Features

    Quantum Logic Integration: Uses quantum circuit rotations (cirq.rx) to inject stochastic behavior into game physics.

    Distributed Processing: Connects to a remote API kernel (f_opt) to synchronize game stability and difficulty in real-time.

    Physics Engine: Built with the Ursina Engine for high-performance 2D/3D interactions.

    Thermal Noise Control: Users can define thermal noise levels, impacting AI decision-making and ball "tunneling" effects.

🛠 Prerequisites

You need Python 3.8+ installed. Install the required dependencies:
Bash

pip install -r requirements.txt

📋 requirements.txt

Create a file named requirements.txt in your project folder with the following content:
Plaintext

cirq
ursina
aiohttp

🎮 How to Run

    Clone the repository:
    Bash

    git clone https://github.com/deywe/HARPIA_GQGAME

    Navigate to the project directory and run the script:
    Bash

    python harpia_kernel_v4_ping_pong5_eng.py

    Enter the Thermal Noise Level (between 0.0 and 1.0) in the terminal to initialize the quantum field.

🌐 Technical Architecture

    Engine: Ursina Engine

    Quantum Simulation: Google Cirq

    Communication: AsyncIO and Aiohttp for non-blocking server communication.

    Optimization Kernel: Custom f_opt API integration.

🔗 Project Official Page

For more details, research updates, and new releases, visit our official repository:
https://github.com/deywe/HARPIA_GQGAME

Developed by Deywe - HARPIA GRAVITO-QUANTUM RESEARCH
