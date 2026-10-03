import {MAX_GAMES, normalize, validateEntry, parseList, parseDump, bucketFor, searchBucket, renderSVG} from './gaming-timeline-core.mjs';

const $ = id => document.getElementById(id);
const BASE = 'https://app.lizardbyte.dev/GameDB/';
const STORAGE = 'gaming-timeline-v1';
const bucketCache = new Map(), recordCache = new Map(), coverCache = new Map();
let entries = [], selected = null, editing = -1, suggestions = [], active = -1;
let searchVersion = 0, revision = 0, svg = '', timer, busy = false, lastFigure = null;

function status(id, message, error = false) {
  $(id).textContent = message;
  $(id).classList.toggle('error', error);
}
async function fetchJSON(url, signal) {
  const response = await fetch(url, {signal: signal || AbortSignal.timeout(8000), credentials: 'omit'});
  if (!response.ok) throw new Error(`Lookup unavailable (${response.status}).`);
  return response.json();
}
async function bucket(name) {
  const key = bucketFor(name);
  if (!bucketCache.has(key)) {
    bucketCache.set(key, fetchJSON(`${BASE}buckets/${encodeURIComponent(key)}.json`).catch(error => {
      bucketCache.delete(key); throw error;
    }));
  }
  return bucketCache.get(key);
}
async function gameRecord(id, signal) {
  if (!recordCache.has(id)) {
    recordCache.set(id, fetchJSON(`${BASE}games/${id}.json`, signal).catch(error => {
      recordCache.delete(id); throw error;
    }));
  }
  return recordCache.get(id);
}
function currentInputs() {
  return {
    entries, title: $('timeline-title').value, covers: $('show-covers').checked,
    draft: {name: $('game-name').value, start: $('start-date').value, end: $('end-date').value, selected, editing, bulk: $('bulk-input').value},
  };
}
function persist() {
  const saved = {...currentInputs(), figure: lastFigure};
  try { localStorage.setItem(STORAGE, JSON.stringify(saved)); }
  catch {
    // If embedded artwork exceeds the storage quota, still preserve all input.
    try {
      localStorage.setItem(STORAGE, JSON.stringify({...saved, figure: null}));
      status('save-status', 'Draft saved. The preview is too large to save; generate again after refreshing.');
    } catch { status('save-status', 'Browser storage is unavailable. Keep this tab open or download your timeline.', true); }
  }
}
function invalidate() {
  revision++; svg = ''; lastFigure = null;
  $('download-svg').disabled = $('download-png').disabled = true;
  if ($('preview').querySelector('svg')) status('render-status', 'Entries changed. Generate again to update the preview and downloads.');
  persist();
}
function closeSuggestions() {
  $('suggestions').hidden = true;
  $('game-name').setAttribute('aria-expanded', 'false');
  $('game-name').removeAttribute('aria-activedescendant');
  active = -1;
}
function choose(index) {
  selected = suggestions[index];
  if (!selected) return;
  $('game-name').value = selected.name;
  searchVersion++;
  closeSuggestions();
  status('search-status', 'Matched in GameDB. Its cover will be fetched when you generate.');
  persist();
}
function showSuggestions(items) {
  suggestions = items; active = -1; $('suggestions').replaceChildren();
  for (const [index, item] of items.entries()) {
    const option = document.createElement('li');
    option.id = `game-option-${index}`; option.role = 'option';
    option.setAttribute('aria-selected', 'false');
    option.textContent = item.name;
    const note = document.createElement('small'); note.textContent = 'GameDB'; option.append(note);
    if (items.filter(other => normalize(other.name) === normalize(item.name)).length > 1) {
      note.textContent = 'Loading edition details…';
      gameRecord(item.gameId).then(record => {
        if (!option.isConnected) return;
        const years = (record.release_dates || []).map(date => date.y).filter(year => Number.isInteger(year) && year > 1900);
        const summary = String(record.summary || '').slice(0, 140);
        note.textContent = `${years.length ? `${Math.min(...years)} · ` : ''}${summary || 'Edition details unavailable'}`;
      }).catch(() => { note.textContent = 'Edition details unavailable'; });
    }
    option.addEventListener('pointerdown', event => event.preventDefault());
    option.addEventListener('click', () => choose(index));
    $('suggestions').append(option);
  }
  $('suggestions').hidden = !items.length;
  $('game-name').setAttribute('aria-expanded', String(Boolean(items.length)));
  $('game-name').removeAttribute('aria-activedescendant');
}
$('game-name').addEventListener('input', () => {
  selected = null; closeSuggestions(); clearTimeout(timer);
  const version = ++searchVersion, query = $('game-name').value.trim();
  if (query.length < 2) { status('search-status', 'Type at least two characters to search by the beginning of a title.'); return; }
  status('search-status', 'Searching GameDB…');
  timer = setTimeout(async () => {
    try {
      const results = searchBucket(await bucket(query), query);
      if (version !== searchVersion || document.activeElement !== $('game-name')) return;
      showSuggestions(results);
      status('search-status', results.length ? 'Choose a match, or keep your own title.' : 'No match. Try the full title from its beginning, or add it as a custom game.');
    } catch {
      if (version === searchVersion) status('search-status', 'The game library is unavailable. You can still add any title.');
    }
  }, 300);
});
$('game-name').addEventListener('keydown', event => {
  if (event.key === 'Escape') { searchVersion++; closeSuggestions(); return; }
  if ($('suggestions').hidden) return;
  if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
    event.preventDefault();
    active = active < 0 ? (event.key === 'ArrowDown' ? 0 : suggestions.length - 1) : (active + (event.key === 'ArrowDown' ? 1 : -1) + suggestions.length) % suggestions.length;
    [...$('suggestions').children].forEach((node, i) => node.setAttribute('aria-selected', String(i === active)));
    $('game-name').setAttribute('aria-activedescendant', `game-option-${active}`);
    $('suggestions').children[active].scrollIntoView({block: 'nearest'});
  } else if (event.key === 'Enter' && active >= 0) { event.preventDefault(); choose(active); }
});
$('game-name').addEventListener('blur', closeSuggestions);

function resetForm() {
  $('game-form').reset(); selected = null; editing = -1; searchVersion++; closeSuggestions();
  $('add-game').textContent = '+ Add game'; $('cancel-edit').hidden = true;
  status('search-status', 'Search the library by the beginning of a title, or use any name.');
}
function showEntries() {
  $('entries').replaceChildren(); $('empty-list').hidden = entries.length > 0;
  entries.forEach((entry, index) => {
    const li = document.createElement('li'), text = document.createElement('div'), name = document.createElement('strong'), dates = document.createElement('small');
    text.className = 'entry-text'; name.textContent = entry.name; dates.textContent = `${entry.start} → ${entry.end}`;
    text.append(name, dates); li.append(text);
    const actions = document.createElement('div'); actions.className = 'entry-actions';
    const edit = document.createElement('button'); edit.type = 'button'; edit.textContent = 'Edit'; edit.setAttribute('aria-label', `Edit ${entry.name}`);
    edit.addEventListener('click', () => {
      searchVersion++; closeSuggestions();
      editing = index; selected = entry.gameId ? {gameId: entry.gameId, name: entry.name} : null;
      $('game-name').value = entry.name; $('start-date').value = entry.start; $('end-date').value = entry.end;
      $('add-game').textContent = 'Save changes'; $('cancel-edit').hidden = false; $('game-name').focus();
      status('entry-status', `Editing ${entry.name}.`);
      persist();
    });
    const remove = document.createElement('button'); remove.type = 'button'; remove.textContent = '×'; remove.setAttribute('aria-label', `Remove ${entry.name}`);
    remove.addEventListener('click', () => {
      entries.splice(index, 1); resetForm(); showEntries(); invalidate();
      status('entry-status', `Removed ${entry.name}.`);
      $('game-name').focus();
    });
    actions.append(edit, remove); li.append(actions); $('entries').append(li);
  });
}
$('game-form').addEventListener('submit', event => {
  event.preventDefault();
  try {
    if (editing < 0 && entries.length >= MAX_GAMES) throw new Error(`A timeline can contain at most ${MAX_GAMES} games.`);
    const entry = validateEntry({name: $('game-name').value, start: $('start-date').value, end: $('end-date').value, gameId: selected?.gameId});
    if (editing >= 0) entries[editing] = entry; else entries.push(entry);
    resetForm(); showEntries(); invalidate(); status('entry-status', `${entry.name} saved.`); $('game-name').focus();
  } catch (error) { status('entry-status', error.message, true); }
});
$('cancel-edit').addEventListener('click', () => { resetForm(); persist(); status('entry-status', 'Edit cancelled.'); });
$('import').addEventListener('click', () => {
  try {
    const added = parseList($('bulk-input').value);
    if (entries.length + added.length > MAX_GAMES) throw new Error(`A timeline can contain at most ${MAX_GAMES} games.`);
    entries.push(...added); showEntries(); $('bulk-input').value = ''; invalidate();
    status('import-status', `Added ${added.length} games. Exact library matches will get covers when you generate.`);
  } catch (error) { status('import-status', error.message, true); }
});
$('timeline-title').addEventListener('input', invalidate);
$('show-covers').addEventListener('change', invalidate);
for (const id of ['game-name', 'start-date', 'end-date', 'bulk-input']) $(id).addEventListener('input', persist);

async function loadCover(entry, signal) {
  let id = entry.gameId;
  if (!id) {
    const matches = searchBucket(await bucket(entry.name), entry.name).filter(game => normalize(game.name) === normalize(entry.name));
    if (matches.length !== 1) return null; // Never guess artwork for ambiguous names.
    id = matches[0].gameId;
  }
  if (signal.aborted) throw new Error('Artwork lookup timed out.');
  if (coverCache.has(id)) return coverCache.get(id);
  const record = await gameRecord(id, signal);
  if (!record.cover?.url) return null;
  const url = new URL(record.cover.url, 'https://images.igdb.com');
  if (url.protocol !== 'https:' || url.hostname !== 'images.igdb.com') return null;
  url.pathname = url.pathname.replace('/t_thumb/', '/t_cover_small/');
  const response = await fetch(url.href, {signal, credentials: 'omit'});
  if (!response.ok) return null;
  const blob = await response.blob();
  if (!/^image\/(jpeg|png|webp)$/.test(blob.type) || blob.size > 2_000_000) return null;
  const data = await new Promise((resolve, reject) => {
    const reader = new FileReader(); reader.onload = () => resolve(reader.result); reader.onerror = reject; reader.readAsDataURL(blob);
  });
  // Decode before embedding so a bad remote image cannot break PNG export.
  await decodeImage(data);
  coverCache.set(id, data);
  return data;
}
function decodeImage(url) {
  return new Promise((resolve, reject) => {
    const image = new Image();
    const timeout = setTimeout(() => { image.src = ''; reject(new Error('Image decoding timed out.')); }, 8000);
    image.onload = () => { clearTimeout(timeout); resolve(image); };
    image.onerror = () => { clearTimeout(timeout); reject(new Error('Image could not be decoded.')); };
    image.src = url;
  });
}
async function generate() {
  if (busy) return;
  if (!entries.length) { status('render-status', 'Add at least one game to generate a timeline.', true); return; }
  busy = true; $('generate').disabled = true; $('generate').textContent = 'Generating…';
  $('download-svg').disabled = $('download-png').disabled = true;
  const version = revision, snapshot = entries.map(entry => ({...entry})), covers = new Map(), includeCovers = $('show-covers').checked;
  const controller = new AbortController();
  const deadline = setTimeout(() => controller.abort(), 15000);
  try {
    if (includeCovers) {
      let next = 0, complete = 0;
      const worker = async () => {
        while (next < snapshot.length && !controller.signal.aborted) {
          const entry = snapshot[next++];
          try {
            const cover = await loadCover(entry, controller.signal);
            if (cover) covers.set(entry.gameId || normalize(entry.name), cover);
          } catch { /* Remote lookup is optional; the figure always works without it. */ }
          complete++;
          status('render-status', `Fetching covers… ${complete} of ${snapshot.length}`);
        }
      };
      status('render-status', 'Fetching game covers…');
      await Promise.all(Array.from({length: Math.min(4, snapshot.length)}, worker));
    }
    if (version !== revision) { status('render-status', 'Entries changed while generating. Generate again to use the latest version.'); return; }
    lastFigure = {entries: snapshot, title: $('timeline-title').value.trim(), covers: [...covers], includeCovers};
    showFigure(lastFigure); persist();
  } catch (error) { status('render-status', `Could not generate: ${error.message}`, true); }
  finally { clearTimeout(deadline); controller.abort(); busy = false; $('generate').disabled = false; $('generate').textContent = 'Generate timeline ↗'; }
}
function showFigure(figure) {
  const covers = new Map(figure.covers);
  svg = renderSVG(figure.entries, figure.title, covers);
  // renderSVG escapes user text and only embeds validated raster data URLs.
  $('preview').innerHTML = svg;
  const figureNode = $('preview').firstElementChild;
  figureNode.style.minWidth = `${Math.max(800, Number(figureNode.getAttribute('width')) * 0.8)}px`;
  $('download-svg').disabled = $('download-png').disabled = false;
  const missing = figure.entries.filter(entry => !covers.has(entry.gameId || normalize(entry.name))).length;
  status('render-status', figure.includeCovers && missing ? `Ready. ${missing} ${missing === 1 ? 'cover was' : 'covers were'} unavailable and skipped.` : 'Ready to download.');
  $('figure-meta').textContent = `${figure.entries.length} ${figure.entries.length === 1 ? 'GAME' : 'GAMES'} / MONTH PRECISION`;
}
$('generate').addEventListener('click', generate);
$('example').addEventListener('click', () => {
  entries = [
    {name: 'Minecraft', gameId: '135400', start: '2012-06', end: '2016'},
    {name: 'Stardew Valley', gameId: '17000', start: '2016-03', end: '2020-09'},
    {name: 'Hollow Knight', gameId: '14593', start: '2018', end: '2019-04'},
    {name: 'Elden Ring', gameId: '119133', start: '2022-02', end: '2024-08'},
  ].map(validateEntry);
  resetForm(); showEntries(); invalidate(); status('entry-status', 'Example loaded. Change the games and dates to make it yours.'); generate();
});
function download(blob, extension, filename = 'gaming-timeline') {
  const url = URL.createObjectURL(blob), link = document.createElement('a');
  link.href = url; link.download = `${filename}.${extension}`; document.body.append(link); link.click(); link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 60000);
}
$('save-inputs').addEventListener('click', () => {
  const inputs = currentInputs();
  const data = {format: 'gaming-history', version: 1, ...inputs,
    entries: inputs.entries.map(({name,start,end,gameId}) => ({name,start,end,gameId})),
  };
  download(new Blob([JSON.stringify(data, null, 2) + '\n'], {type:'application/json'}), 'json', 'gaming-history-inputs');
  status('file-status', 'Inputs saved. Use Load inputs to restore this file later.');
});
$('load-inputs').addEventListener('click', () => $('inputs-file').click());
$('inputs-file').addEventListener('change', async () => {
  const file = $('inputs-file').files[0];
  if (!file) return;
  try {
    if (file.size > 1_000_000) throw new Error('Choose an inputs file smaller than 1 MB.');
    const before = JSON.stringify(currentInputs());
    const loaded = parseDump(await file.text());
    if (JSON.stringify(currentInputs()) !== before) throw new Error('Your draft changed while reading the file. Please load it again.');
    // Validate the entire file before changing any current input or saved state.
    resetForm(); entries = loaded.entries;
    $('timeline-title').value = loaded.title; $('show-covers').checked = loaded.covers;
    restoreDraft(loaded.draft); showEntries(); invalidate();
    const note = document.createElement('p'); note.className = 'placeholder'; note.textContent = 'Inputs loaded. Generate your timeline when you’re ready.';
    $('preview').replaceChildren(note); $('figure-meta').textContent = 'READY TO GENERATE';
    status('render-status', 'Inputs loaded. Generate to render the timeline.');
    status('entry-status', 'Restored inputs from file.');
    status('file-status', `Loaded ${entries.length} ${entries.length === 1 ? 'game' : 'games'}, settings, and unfinished input.`);
  } catch (error) { status('file-status', `${error.message} Your current draft was kept.`, true); }
  finally { $('inputs-file').value = ''; }
});
$('download-svg').addEventListener('click', () => { if (svg) download(new Blob([svg], {type: 'image/svg+xml;charset=utf-8'}), 'svg'); });
$('download-png').addEventListener('click', async () => {
  if (!svg) return;
  const source = svg, version = revision;
  $('download-png').disabled = true; status('render-status', 'Preparing PNG…');
  const url = URL.createObjectURL(new Blob([source], {type: 'image/svg+xml;charset=utf-8'}));
  try {
    const image = await decodeImage(url), canvas = document.createElement('canvas');
    // Keep large timelines within common browser canvas dimension/memory limits.
    const scale = Math.min(2, 16000 / image.width, 16000 / image.height, Math.sqrt(24_000_000 / (image.width * image.height)));
    canvas.width = Math.floor(image.width * scale); canvas.height = Math.floor(image.height * scale);
    const context = canvas.getContext('2d');
    if (!context) throw new Error('This browser cannot create a canvas. Try SVG instead.');
    context.drawImage(image, 0, 0, canvas.width, canvas.height);
    const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
    if (!blob) throw new Error('This browser could not create the PNG. Try SVG instead.');
    if (version !== revision) return;
    download(blob, 'png'); status('render-status', `PNG downloaded (${canvas.width} × ${canvas.height}).`);
  } catch (error) { status('render-status', error.message, true); }
  finally { URL.revokeObjectURL(url); $('download-png').disabled = !svg; }
});
try {
  const saved = JSON.parse(localStorage.getItem(STORAGE));
  if (saved && Array.isArray(saved.entries) && saved.entries.length <= MAX_GAMES) {
    entries = saved.entries.map(validateEntry);
    if (typeof saved.title === 'string') $('timeline-title').value = saved.title.slice(0, 90);
    if (typeof saved.covers === 'boolean') $('show-covers').checked = saved.covers;
    if (saved.draft) restoreDraft(saved.draft);
    if (entries.length || saved.draft?.name || saved.draft?.bulk) status('entry-status', 'Restored your saved draft.');
    if (saved.figure && Array.isArray(saved.figure.entries) && Array.isArray(saved.figure.covers) && typeof saved.figure.title === 'string') {
      try { showFigure(saved.figure); lastFigure = saved.figure; status('render-status', 'Saved timeline restored. Ready to download.'); }
      catch { status('render-status', 'Draft restored. Generate again to restore the preview.'); }
    }
  }
} catch { /* A private browser or old draft should not prevent using the tool. */ }
showEntries();
function restoreDraft(draft) {
  for (const [id, key, limit] of [['game-name','name',160],['start-date','start',7],['end-date','end',7],['bulk-input','bulk',50000]]) {
    if (typeof draft[key] === 'string') $(id).value = draft[key].slice(0,limit);
  }
  if (draft.selected?.name === $('game-name').value && /^\d+$/.test(draft.selected?.gameId)) selected = draft.selected;
  if (Number.isInteger(draft.editing) && draft.editing >= 0 && draft.editing < entries.length) {
    editing = draft.editing; $('add-game').textContent = 'Save changes'; $('cancel-edit').hidden = false;
  }
  document.querySelector('.bulk').open = Boolean($('bulk-input').value);
}
