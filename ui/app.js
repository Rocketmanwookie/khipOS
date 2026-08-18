const $ = (q) => document.querySelector(q);
let recognition;

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
  recognition.onstart = () => { $('#listen').classList.add('listening'); $('#listen').setAttribute('aria-pressed','true'); $('#listen span').textContent='Listening…'; $('#mic-note').textContent='Microphone is active and visible.'; };
  recognition.onresult = e => { $('#intent').value = Array.from(e.results).map(r=>r[0].transcript).join(''); };
  recognition.onend = () => { $('#listen').classList.remove('listening'); $('#listen').setAttribute('aria-pressed','false'); $('#listen span').textContent='Start listening'; $('#mic-note').textContent='Microphone is off.'; };
  $('#listen').addEventListener('click', () => recognition.start());
} else { $('#listen').disabled=true; $('#mic-note').textContent='Speech recognition is unavailable in this browser; keyboard input works.'; }

load().catch(error => { $('#result').className='result approval'; $('#result').textContent=error.message; });
