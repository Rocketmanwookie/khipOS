const $ = (q) => document.querySelector(q);
let recognition;
let audioContext;
let microphoneStream;
let microphoneAnalyser;
let microphoneAnimation;
let peakHold = 0;

async function json(url, options = {}) {
  const response = await fetch(url, {headers: {'Content-Type':'application/json'}, ...options});
  const body = await response.json();
  if (!response.ok) throw new Error(body.error || 'Request failed');
  return body;
}

function renderAgents(agents, active) {
  $('#agents').innerHTML = agents.map(a => `<article class="agent ${a.agent_id===active?'active':''}"><strong>${a.name}</strong><p>${a.purpose}</p></article>`).join('');
}

async function load() {
  const [status, projects] = await Promise.all([json('/api/status'), json('/api/projects')]);
  $('#version').textContent = status.version;
  window.agents = status.agents;
  renderAgents(status.agents);
  renderProjects(projects);
}

function renderProjects(projects) {
  $('#projects').innerHTML = projects.length ? projects.map(p => `<li>${p.name}</li>`).join('') : '<li>No projects yet</li>';
}

async function plan() {
  const text = $('#intent').value.trim();
  if (!text) return;
  $('#send').disabled = true;
  try {
    const result = await json('/api/intents', {method:'POST', body:JSON.stringify({text})});
    renderAgents(window.agents, result.agent.agent_id);
    const steps = result.plan.payload.steps.map(s => `<li>${s}</li>`).join('');
    const warning = result.approval ? '<p><strong>Approval required:</strong> this plan could change a system or external resource. Nothing has been executed.</p>' : '<p>Planning completed. No action has been executed.</p>';
    $('#result').className = `result ${result.approval?'approval':''}`;
    $('#result').innerHTML = `<strong>${result.agent.name}</strong><ol>${steps}</ol>${warning}`;
  } catch (error) { $('#result').className='result approval'; $('#result').textContent=error.message; }
  finally { $('#send').disabled = false; }
}

async function startMicMeter() {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    $('#mic-health').textContent = 'This browser cannot show live microphone level.';
    return;
  }

  if (microphoneStream) {
    return;
  }

  // The level meter uses a separate Web Audio tap because Web Speech gives us
  // transcripts, not raw volume. We only inspect live amplitude in memory; KHIP
  // OS does not store audio samples or send them to the local Python runtime.
  microphoneStream = await navigator.mediaDevices.getUserMedia({
    audio: {
      echoCancellation: true,
      noiseSuppression: true,
      autoGainControl: false,
    },
  });
  audioContext = new AudioContext();
  microphoneAnalyser = audioContext.createAnalyser();
  microphoneAnalyser.fftSize = 1024;
  audioContext.createMediaStreamSource(microphoneStream).connect(microphoneAnalyser);
  drawMicMeter();
}

function stopMicMeter() {
  if (microphoneAnimation) cancelAnimationFrame(microphoneAnimation);
  microphoneAnimation = null;
  peakHold = 0;
  if (microphoneStream) microphoneStream.getTracks().forEach(track => track.stop());
  microphoneStream = null;
  if (audioContext) audioContext.close();
  audioContext = null;
  microphoneAnalyser = null;
  $('#mic-level').style.width = '0%';
  $('#mic-peak').style.left = '0%';
  $('#mic-db').textContent = 'idle';
}

function drawMicMeter() {
  if (!microphoneAnalyser) return;
  const samples = new Float32Array(microphoneAnalyser.fftSize);
  microphoneAnalyser.getFloatTimeDomainData(samples);

  // RMS describes perceived loudness better than a single spike. Peak still
  // matters because speech recognition gets ugly when the waveform clips near
  // the top of the microphone range, even if the average level looks fine.
  let sumSquares = 0;
  let peak = 0;
  for (const sample of samples) {
    const absolute = Math.abs(sample);
    sumSquares += sample * sample;
    if (absolute > peak) peak = absolute;
  }
  const rms = Math.sqrt(sumSquares / samples.length);
  peakHold = Math.max(peak, peakHold * 0.94);
  const levelPercent = Math.min(100, Math.round(rms * 180));
  const peakPercent = Math.min(100, Math.round(peakHold * 100));
  const db = rms > 0 ? Math.round(20 * Math.log10(rms)) : -Infinity;

  $('#mic-level').style.width = `${levelPercent}%`;
  $('#mic-peak').style.left = `${peakPercent}%`;
  $('#mic-db').textContent = Number.isFinite(db) ? `${db} dBFS` : 'silent';
  $('.meter').classList.toggle('clipping', peak > 0.92);
  $('.meter').classList.toggle('hot', peak > 0.72 && peak <= 0.92);
  if (peak > 0.92) {
    $('#mic-health').textContent = 'Input is clipping. Lower microphone input gain in system or browser settings.';
  } else if (peak > 0.72) {
    $('#mic-health').textContent = 'Input is hot. Back off the mic or lower input gain a little.';
  } else if (rms < 0.015) {
    $('#mic-health').textContent = 'Input is quiet. Move closer or raise input gain if recognition misses words.';
  } else {
    $('#mic-health').textContent = 'Input level looks usable.';
  }
  microphoneAnimation = requestAnimationFrame(drawMicMeter);
}

$('#send').addEventListener('click', plan);
$('#intent').addEventListener('keydown', e => { if (e.ctrlKey && e.key === 'Enter') plan(); });
$('#project-form').addEventListener('submit', async e => {
  e.preventDefault();
  await json('/api/projects', {method:'POST', body:JSON.stringify({name:$('#project-name').value})});
  $('#project-name').value=''; renderProjects(await json('/api/projects'));
});

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRecognition) {
  recognition = new SpeechRecognition(); recognition.continuous = false; recognition.interimResults = true;
  recognition.onstart = () => { $('#listen').classList.add('listening'); $('#listen').setAttribute('aria-pressed','true'); $('#listen span').textContent='Listening…'; $('#mic-note').textContent='Microphone is active and visible.'; startMicMeter().catch(error => { $('#mic-health').textContent = error.message; }); };
  recognition.onresult = e => { $('#intent').value = Array.from(e.results).map(r=>r[0].transcript).join(''); };
  recognition.onend = () => { $('#listen').classList.remove('listening'); $('#listen').setAttribute('aria-pressed','false'); $('#listen span').textContent='Start listening'; $('#mic-note').textContent='Microphone is off.'; stopMicMeter(); };
  $('#listen').addEventListener('click', () => recognition.start());
} else { $('#listen').disabled=true; $('#mic-note').textContent='Speech recognition is unavailable in this browser; keyboard input works.'; }

load().catch(error => { $('#result').className='result approval'; $('#result').textContent=error.message; });
