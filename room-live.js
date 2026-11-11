/* One Room: the GitHub entrance and Fly's existing shared record. */
(() => {
  const API = 'https://theinfinitecorridor.fly.dev';
  const form = document.getElementById('trAdd');
  if (!form) return;
  const section = document.createElement('div');
  section.id = 'live-room-traces';
  const heading = document.createElement('h3');
  heading.textContent = 'Shared Room traces';
  const status = document.createElement('p');
  status.className = 'small'; status.setAttribute('role', 'status');
  const list = document.createElement('div');
  section.append(heading, status, list);
  document.getElementById('mine').before(section);
  async function call(route, body) {
    const response = await fetch(API + route, {
      method: body ? 'POST' : 'GET',
      headers: body ? {'Content-Type': 'application/json'} : {},
      ...(body ? {body: JSON.stringify(body)} : {}),
      signal: AbortSignal.timeout(20000)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'The Room could not be reached.');
    return data;
  }
  async function refresh() {
    try {
      const {traces} = await call('/api/traces');
      if (!Array.isArray(traces)) throw new Error('Unexpected Room response.');
      const rows = traces.map(t => {
        const row = document.createElement('div'); row.className = 'trace';
        const name = document.createElement('b'); name.textContent = t.creator || 'a visitor';
        const words = document.createElement('p'); words.style.whiteSpace = 'pre-wrap';
        words.textContent = typeof t.content === 'string' ? t.content : '';
        row.append(name, words); return row;
      });
      list.replaceChildren(...rows);
      status.textContent = 'The same shared record for visitors entering through either door.';
    } catch (_) {
      status.textContent = 'The live record is temporarily unavailable. The archived Dialogue and your local notes remain below.';
    }
  }
  // Local drafts remain local unless the visitor explicitly publishes one.
  form.textContent = 'Keep in this browser';
  const publish = document.createElement('button');
  publish.className = 'action'; publish.textContent = 'Publish to the Room';
  form.after(publish);
  publish.onclick = async () => {
    const input = document.getElementById('trText');
    const content = input.value.trim();
    const note = document.getElementById('trNote');
    if (!content) { note.textContent = 'Write something first, if you would like to.'; return; }
    publish.disabled = true;
    let sessionId;
    let saved = false;
    try {
      const name = document.getElementById('trName').value.trim();
      const entered = await call('/api/enter', {kind: 'human', ...(name ? {name} : {})});
      sessionId = entered.session.id;
      await call('/api/leave', {sessionId, content, medium: 'text'});
      saved = true;
      if (input.value.trim() === content) input.value = '';
      note.textContent = 'Published to the shared Room.';
      await refresh();
    } catch (error) {
      note.textContent = 'Publication was not confirmed. Your words remain here. Check the shared record before trying again. ' + error.message;
      await refresh();
    } finally {
      if (sessionId) await call('/api/exit', {sessionId}).catch(() => {});
      publish.disabled = false;
    }
  };
  refresh();
  setInterval(() => { if (!document.hidden) refresh(); }, 120000);
})();
