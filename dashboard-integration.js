// LIVE CHAT WITH REAL BACKEND
const chatLog = document.getElementById('chat-log');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');

async function sendChatToKernel(userText) {
  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userText })
    });
    if (!res.ok) throw new Error('Server error');
    return await res.json();
  } catch (err) {
    return { reply: '[Backend error: ' + err.message + ']', kernelState: null };
  }
}

function addMsg(sender, text) {
  const div = document.createElement('div');
  div.className = 'chat-msg';
  div.innerHTML = `<span class="sender">${sender}:</span> ${text}`;
  chatLog.appendChild(div);
  chatLog.scrollTop = chatLog.scrollHeight;
}

chatForm.addEventListener('submit', async e => {
  e.preventDefault();
  const val = chatInput.value.trim();
  if (!val) return;
  addMsg('You', val);
  chatInput.value = '';
  const aiData = await sendChatToKernel(val);
  addMsg('AI', aiData.reply);
  if (aiData.kernelState) updateKernelState(aiData.kernelState);
});

// KERNEL STATE 3D CHART WITH REAL BACKEND
let scene, camera, renderer, animationId, kernelParticles = [];
const canvas = document.getElementById('three-canvas');
const chartModeSelect = document.getElementById('chart-mode');
const resetBtn = document.getElementById('reset-chart-btn');
let kernelStateColor = 0x00e5ff;

function updateKernelState(state) {
  if (!scene || !scene.children.length) return;
  const kernelCore = scene.children[0];
  let trust = state.trust ?? 0.5;
  let harmony = state.harmony ?? 0.5;
  const c = new THREE.Color().setHSL(0.5 + trust * 0.25, 0.9, 0.6);
  kernelStateColor = c.getHex();
  kernelCore.material.color.setHex(kernelStateColor);
  let scale = 1 + 0.6 * harmony;
  kernelCore.scale.set(scale, scale, scale);
}

async function fetchKernelState() {
  try {
    const res = await fetch('/api/kernel/state');
    if (!res.ok) throw new Error('Server error');
    return await res.json();
  } catch (e) { return { trust: 0.5, harmony: 0.5 }; }
}

function init3DChart(mode = 'network', kernelState = {trust:0.5, harmony:0.5}) {
  if (renderer) {
    cancelAnimationFrame(animationId);
    renderer.dispose();
    renderer.forceContextLoss();
    canvas.width = canvas.width;
  }
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(70, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
  renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
  renderer.setClearColor(0xf7fafc, 1);
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.setSize(canvas.clientWidth, canvas.clientHeight, false);
  camera.position.z = 13;
  const geometry = new THREE.SphereGeometry(2, 32, 32);
  const material = new THREE.MeshBasicMaterial({ color: 0x00e5ff, transparent: true, opacity: 0.13 });
  const kernelCore = new THREE.Mesh(geometry, material);
  scene.add(kernelCore);
  kernelParticles = [];
  const numParticles = 220;
  const pGeom = new THREE.SphereGeometry(0.19, 10, 10);
  for (let i = 0; i < numParticles; i++) {
    const pm = new THREE.MeshBasicMaterial({ color: 0x0f766e, opacity: 0.8, transparent: true });
    const p = new THREE.Mesh(pGeom, pm);
    let phi = Math.random() * Math.PI * 2;
    let theta = Math.random() * Math.PI;
    let r = 5.7 + Math.random() * 1.6;
    if (mode === 'network') {
      r = 5.7 + Math.random() * 1.6;
    } else {
      r = 6.3;
      phi = 2 * Math.PI * (i / numParticles);
      theta = Math.acos(2 * (i / numParticles) - 1);
    }
    p.position.set(
      r * Math.sin(theta) * Math.cos(phi),
      r * Math.sin(theta) * Math.sin(phi),
      r * Math.cos(theta)
    );
    kernelParticles.push(p);
    scene.add(p);
  }
  let t = 0;
  function animate() {
    t += 0.01;
    kernelCore.rotation.y += 0.004;
    for (let i = 0; i < kernelParticles.length; i++) {
      const p = kernelParticles[i];
      if (mode === 'network') {
        p.position.x += Math.sin(t + i) * 0.002;
        p.position.y += Math.cos(t - i) * 0.002;
      } else {
        p.position.x += Math.sin(t + i) * 0.001;
      }
    }
    renderer.render(scene, camera);
    animationId = requestAnimationFrame(animate);
  }
  updateKernelState(kernelState);
  animate();
}

window.addEventListener('resize', () => {
  if (!renderer || !camera) return;
  const width = canvas.clientWidth, height = canvas.clientHeight;
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setSize(width, height, false);
});

chartModeSelect.addEventListener('change', async e => {
  const state = await fetchKernelState();
  init3DChart(e.target.value, state);
});
resetBtn.addEventListener('click', async () => {
  const state = await fetchKernelState();
  init3DChart(chartModeSelect.value, state);
});

(async function() {
  const state = await fetchKernelState();
  init3DChart('network', state);
})();