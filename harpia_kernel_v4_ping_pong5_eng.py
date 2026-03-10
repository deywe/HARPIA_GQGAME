import cirq
from ursina import *
import asyncio
import aiohttp
import random
import threading

# --- INITIAL CONFIGURATION (THERMAL NOISE INPUT) ---
print("--- HARPIA QUANTUM FIELD DUEL ---")
try:
    val = input("Set the initial Thermal Noise level (0.0 to 1.0): ")
    thermal_noise_level = float(val)
    thermal_noise_level = max(0.0, min(1.0, thermal_noise_level))
except ValueError:
    thermal_noise_level = 0.1
    print("Invalid value. Starting with 0.1")

# --- SETTINGS ---
API_URL = "http://161.153.0.202:6060/resolver_fopt"
app = Ursina(title="HARPIA :: QUANTUM FIELD DUEL")
window.color = color.black
camera.orthographic = True
camera.fov = 14 

# Physics Constants
INITIAL_SPEED = Vec2(0.07, 0.03)
MAX_SPEED = INITIAL_SPEED * 4.0
ball_speed = Vec2(0.07, 0.03)
boost_kernel = 1.0

# --- ENTITIES ---
ball = Entity(model='sphere', color=color.green, scale=0.56, collider='box', z=0)
paddle_harpia = Entity(model='quad', color=color.yellow, scale=(0.5, 3), x=-7, z=0, collider='box')
paddle_deywe = Entity(model='quad', color=color.cyan, scale=(0.5, 3), x=7, z=0, collider='box')

score_player = 0
score_ai = 0
score_text = Text(text='Harpia  0 : 0  Deywe', position=(0, 0.45), scale=1.5, origin=(0,0))

# --- PROMOTIONAL MESSAGE ---
promo_text = Text(
    text='HARPIA GRAVITO-QUANTUM CIRQ PING PONG GAME | DOWNLOAD NOW: https://github.com/deywe/HARPIA_GQGAME',
    position=(0, 0.38), 
    scale=0.7, 
    origin=(0,0), 
    color=color.yellow
)

info_text = Text(text='', position=(0, -0.45), scale=1, origin=(0,0))

def apply_cirq_circuit():
    qubit = cirq.NamedQubit('q0')
    circuit = cirq.Circuit(cirq.rx(random.uniform(0, 1)).on(qubit))
    result = cirq.Simulator().simulate(circuit)
    return (result.final_state_vector[0].real) * 0.4 - 0.2

def reset_ball():
    global ball_speed
    ball.position = (0, 0)
    ball_speed = Vec2(0.07 * (1 if random.random() > 0.5 else -1), 0.03)
    ball.visible = False
    invoke(setattr, ball, 'visible', True, delay=0.5)

def update():
    global ball_speed, score_player, score_ai, thermal_noise_level, boost_kernel
    
    # 1. Movement
    ball.position += ball_speed
    
    # 2. Deywe Controls
    paddle_deywe.y += (held_keys['up arrow'] - held_keys['down arrow']) * 0.15
    paddle_deywe.y = clamp(paddle_deywe.y, -3.5, 3.5)
    
    # 3. AI Harpia
    target_y = ball.y + (random.uniform(-1, 1) * thermal_noise_level * 2)
    paddle_harpia.y = lerp(paddle_harpia.y, target_y, 0.12)
    paddle_harpia.y = clamp(paddle_harpia.y, -3.5, 3.5)
    
    # 4. Collision with Cirq Logic and Safety Offset
    hit_info = ball.intersects()
    if hit_info.hit:
        entity = hit_info.entity
        if (entity == paddle_harpia and ball_speed.x < 0) or (entity == paddle_deywe and ball_speed.x > 0):
            q_variation = apply_cirq_circuit()
            ball_speed.y += q_variation
            ball_speed.x *= -1.05
            
            # Safety offset to prevent sticking
            if entity == paddle_harpia: ball.x = paddle_harpia.x + 0.6
            else: ball.x = paddle_deywe.x - 0.6
            
    # Speed Limit
    if ball_speed.length() > MAX_SPEED.length():
        ball_speed = ball_speed.normalized() * MAX_SPEED.length()
            
    # Walls
    if abs(ball.y) > 4: ball_speed.y *= -1

    # 5. Scoring
    if ball.x > 8:
        score_ai += 1
        reset_ball()
    elif ball.x < -8:
        score_player += 1
        reset_ball()
    
    score_text.text = f'Harpia  {score_ai} : {score_player}  Deywe'
    info_text.text = f'Thermal Noise: {thermal_noise_level:.2f} | Kernel: {boost_kernel:.2f}'

# --- KERNEL ---
async def run_kernel():
    global boost_kernel
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.post(API_URL, json={"T": thermal_noise_level}, timeout=1) as r:
                    data = await r.json()
                    boost_kernel = data.get("f_opt", 1.0)
            except: boost_kernel = 0.1
            await asyncio.sleep(0.5)

threading.Thread(target=lambda: asyncio.run(run_kernel()), daemon=True).start()
app.run()
