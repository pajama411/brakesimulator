import streamlit as st
import base64
import streamlit.components.v1 as components

# --------------------------
# 타이틀
# --------------------------
st.markdown("""
<div style="
    background-color:#1f2937; 
    padding:20px; 
    border-radius:12px; 
    text-align:center;
">
    <h1 style="color:#facc15; font-family:'Segoe UI', sans-serif; font-weight:700; margin:0;">
        ⚡ EDDY BRAKE SIMULATOR
    </h1>
    <p style="color:#e5e7eb; font-size:18px; margin-top:5px;">
        전자기 유도 기반 비접촉식 제동 시뮬레이션
    </p>
</div>
""", unsafe_allow_html=True)

# --------------------------
# 사이드바 입력
# --------------------------
st.sidebar.header("⚙️ 시뮬레이터 설정")
speed = st.sidebar.slider("차량 초기 속도 (km/h)", 0, 150, 50, key="speed_slider")
mass = st.sidebar.slider("차량 질량 (kg)", 800, 2000, 1400, key="mass_slider")

base_B = 0.8
max_speed = 150
dt = 0.03

# --------------------------
# wheel.png를 base64로 읽기
# --------------------------
with open("wheel.PNG", "rb") as f:
    img_bytes = f.read()
img_b64 = base64.b64encode(img_bytes).decode()

# --------------------------
# HTML + JS 렌더링
# --------------------------
components.html(f"""
<div style="display:flex;">
    <canvas id="wheelCanvas" width="300" height="300" style="border:1px solid #ccc;"></canvas>
    <canvas id="forceGraph" width="500" height="300" style="border:1px solid #ccc; margin-left:20px;"></canvas>
</div>

<script>
const wheelCanvas = document.getElementById("wheelCanvas");
const wheelCtx = wheelCanvas.getContext("2d");
const graphCanvas = document.getElementById("forceGraph");
const graphCtx = graphCanvas.getContext("2d");

const img = new Image();
img.src = "data:image/png;base64,{img_b64}";

let angle = 0;
let speed = {speed};
let mass = {mass};
let base_B = {base_B};
let max_speed = {max_speed};
let dt = {dt};

function eddy_force(v, m) {{
    let B = base_B * (v / max_speed);  // 속도 비례 자기장
    return 0.004 * B*B * v * m;        // 제동력
}}

function drawWheel() {{
    wheelCtx.fillStyle = '#fff';
    wheelCtx.fillRect(0,0,wheelCanvas.width,wheelCanvas.height);
    angle += 2 + speed/10;
    wheelCtx.save();
    wheelCtx.translate(wheelCanvas.width/2, wheelCanvas.height/2);
    wheelCtx.rotate(angle * Math.PI/180);
    wheelCtx.drawImage(img, -img.width/2, -img.height/2);
    wheelCtx.restore();
}}

function drawGraph(currentSpeed) {{
    graphCtx.fillStyle = '#fff';
    graphCtx.fillRect(0,0,graphCanvas.width,graphCanvas.height);

    // 모눈
    graphCtx.strokeStyle = '#eee';
    graphCtx.lineWidth = 1;
    for(let x=40;x<graphCanvas.width;x+=50){{
        graphCtx.beginPath();
        graphCtx.moveTo(x,0);
        graphCtx.lineTo(x,graphCanvas.height);
        graphCtx.stroke();
    }}
    for(let y=0;y<graphCanvas.height;y+=50){{
        graphCtx.beginPath();
        graphCtx.moveTo(40,y);
        graphCtx.lineTo(graphCanvas.width,y);
        graphCtx.stroke();
    }}

    // 축
    graphCtx.strokeStyle = '#000';
    graphCtx.lineWidth = 2;
    graphCtx.beginPath();
    graphCtx.moveTo(40,0);
    graphCtx.lineTo(40,graphCanvas.height); 
    graphCtx.moveTo(40,graphCanvas.height);
    graphCtx.lineTo(graphCanvas.width,graphCanvas.height); 
    graphCtx.stroke();

    // 속도(x축) vs 제동력(y축)
    const maxForce = eddy_force(max_speed, mass);
    const x1 = 40 + (graphCanvas.width-50-40)*(currentSpeed/max_speed);
    const y1 = graphCanvas.height - (eddy_force(currentSpeed, mass)/maxForce)*(graphCanvas.height-40);

    graphCtx.beginPath();
    graphCtx.strokeStyle = 'red';
    graphCtx.lineWidth = 2;
    graphCtx.moveTo(40, graphCanvas.height);
    graphCtx.lineTo(x1, y1);
    graphCtx.stroke();

    // 레이블
    graphCtx.fillStyle='#000';
    graphCtx.font = "14px sans-serif";
    graphCtx.fillText("속도 (km/h)", graphCanvas.width-70, graphCanvas.height-5);
    graphCtx.fillText("제동력 (N)", 5,15);
}}

function animate(){{
    const force = eddy_force(speed, mass);
    const a = force/mass;
    speed = Math.max(0, speed - a*dt);

    drawWheel();
    drawGraph(speed);
    requestAnimationFrame(animate);
}}

img.onload = animate;
</script>
""", height=400)

# --------------------------
# 해석 가이드
# --------------------------
st.markdown("""
---
# 📘 해석 가이드

### 1) 속도가 높을수록 제동력이 증가
그래프는 속도에 비례해 제동력이 커지는 형태를 보입니다.  
이는 페러데이 전자기 유도 법칙에서 유도 기전력이 속도에 비례하기 때문입니다.

### 2) 자기장 세기(B)가 강할수록 제동력이 증가
속도가 높아질수록 자기장 세기도 증가하여 더 큰 제동력이 만들어집니다.

### 3) 질량이 커질수록 필요한 제동력도 커짐
큰 질량은 더 큰 운동 에너지를 가지므로 동일 속도에서도 더 큰 제동력이 요구됩니다.

### 4) 비접촉식 제동의 장점
- 마찰 없음 → 브레이크 패드 마모 없음  
- 열에 강함  
- 고속에서 안정적  
- 기계적 소음 없음  

### 5) 단점
- 저속에서는 제동력이 약함  
- 차량을 완전히 정지시키기 어렵기 때문에 실제 자동차에서는 기계식 브레이크와 병행 사용
""")

