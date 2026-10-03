// Pure date, input, and drawing functions shared by the page and its tests.
export const MAX_GAMES = 80;
export const COLORS = ['#285b47', '#b26439', '#53699a', '#8b5677', '#787336', '#367e85'];
export const normalize = value => value.trim().toLocaleLowerCase().normalize('NFKC');
export function parseDate(value) {
  const match = /^(\d{4})(?:-(\d{1,2}))?$/.exec(value.trim());
  if (!match) throw new Error('Use YYYY or YYYY-MM for both dates.');
  const year = Number(match[1]), month = Number(match[2] || 1);
  if (year < 1900 || year > 2100 || month < 1 || month > 12) throw new Error('Use a year from 1900 to 2100 and a month from 01 to 12.');
  return year * 12 + month - 1;
}
export function dateLabel(value) {
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  return `${months[value % 12]} ${Math.floor(value / 12)}`;
}
export function validateEntry(entry) {
  const name = String(entry.name || '').trim();
  if (!name || name.length > 160) throw new Error('Enter a game name of 1–160 characters.');
  const start = String(entry.start || '').trim(), end = String(entry.end || '').trim();
  const from = parseDate(start), to = parseDate(end);
  if (to < from) throw new Error('The end date must be on or after the start date.');
  return {name, start, end, from, to, gameId: /^\d+$/.test(String(entry.gameId)) ? String(entry.gameId) : null};
}
export function parseDump(text) {
  let data;
  try { data = JSON.parse(text); } catch { throw new Error('This file is not valid JSON.'); }
  if (data?.format !== 'gaming-history' || data.version !== 1) throw new Error('Choose a Gaming History Creator inputs file (version 1).');
  const string = (value, limit, label) => {
    if (typeof value !== 'string' || value.length > limit) throw new Error(`Invalid ${label} in the file.`);
    return value;
  };
  if (!Array.isArray(data.entries) || data.entries.length > MAX_GAMES) throw new Error(`The file must contain a list of at most ${MAX_GAMES} games.`);
  const entries = data.entries.map((entry, index) => {
    try {
      if (!entry || typeof entry !== 'object') throw new Error('Invalid game entry.');
      for (const key of ['name','start','end']) string(entry[key], key === 'name' ? 160 : 7, key);
      if (entry.gameId != null && (typeof entry.gameId !== 'string' || !/^\d{1,20}$/.test(entry.gameId))) throw new Error('Invalid game library ID.');
      return validateEntry(entry);
    } catch (error) { throw new Error(`Game ${index + 1}: ${error.message}`); }
  });
  const title = string(data.title, 90, 'timeline title');
  if (typeof data.covers !== 'boolean') throw new Error('Invalid cover preference in the file.');
  const raw = data.draft ?? {name:'', start:'', end:'', bulk:'', editing:-1, selected:null};
  const draft = {};
  for (const [key, limit] of [['name',160],['start',7],['end',7],['bulk',50000]]) draft[key] = string(raw[key], limit, `unfinished ${key}`);
  if (!Number.isInteger(raw.editing) || raw.editing < -1 || raw.editing >= entries.length) throw new Error('Invalid editing position in the file.');
  draft.editing = raw.editing;
  draft.selected = null;
  if (raw.selected != null) {
    if (raw.selected.name !== draft.name || typeof raw.selected.gameId !== 'string' || !/^\d{1,20}$/.test(raw.selected.gameId)) throw new Error('Invalid game selection in the file.');
    draft.selected = {name: draft.name, gameId: raw.selected.gameId};
  }
  return {entries, title, covers: data.covers, draft};
}
// A small CSV/TSV reader: quoted names and escaped double quotes are supported.
export function parseList(text) {
  const lines = text.split(/\r?\n/).map((line, index) => ({line, index})).filter(({line}) => line.trim());
  if (!lines.length) throw new Error('Paste at least one game.');
  if (lines.length > MAX_GAMES) throw new Error(`Use at most ${MAX_GAMES} games.`);
  return lines.map(({line, index}) => {
    const delimiter = line.includes('\t') ? '\t' : ',';
    const fields = []; let field = '', quoted = false, closed = false;
    for (let i = 0; i < line.length; i++) {
      const char = line[i];
      if (char === '"') {
        if (quoted && line[i + 1] === '"') { field += '"'; i++; }
        else if (quoted) { quoted = false; closed = true; }
        else if (!field.trim() && !closed) { quoted = true; field = ''; }
        else throw new Error(`Line ${index + 1}: unexpected quotation mark.`);
      } else if (char === delimiter && !quoted) { fields.push(field.trim()); field = ''; closed = false; }
      else if (closed && char.trim()) throw new Error(`Line ${index + 1}: add a separator after the quoted name.`);
      else field += char;
    }
    fields.push(field.trim());
    if (quoted || fields.length !== 3) throw new Error(`Line ${index + 1}: use Game name, start, end.`);
    try { return validateEntry({name: fields[0], start: fields[1], end: fields[2]}); }
    catch (error) { throw new Error(`Line ${index + 1}: ${error.message}`); }
  });
}
// GameDB's original-title buckets use the first two ASCII characters, or the
// first character for titles such as "A Short Hike". Other prefixes use @.
export function bucketFor(name) {
  const value = normalize(name);
  if (/^[a-z0-9]{2}/.test(value)) return value.slice(0, 2);
  if (/^[a-z0-9] /.test(value)) return value[0];
  return '@';
}
export function searchBucket(data, query) {
  const needle = normalize(query);
  return Object.entries(data).filter(([, item]) => typeof item?.name === 'string' && normalize(item.name).startsWith(needle))
    .map(([gameId, item]) => ({gameId, name: item.name}))
    .sort((a, b) => Number(normalize(b.name) === needle) - Number(normalize(a.name) === needle) || a.name.length - b.name.length || a.name.localeCompare(b.name))
    .slice(0, 12);
}
export function layout(entries) {
  if (!entries.length || entries.length > MAX_GAMES) throw new Error(`Add between 1 and ${MAX_GAMES} games.`);
  const rows = entries.map(validateEntry).sort((a,b) => a.from - b.from || a.to - b.to);
  const firstYear = Math.floor(Math.min(...rows.map(row => row.from)) / 12);
  const lastYear = Math.floor(Math.max(...rows.map(row => row.to)) / 12) + 1;
  const yearWidth = Math.max(72, 680 / (lastYear - firstYear));
  const axisWidth = (lastYear - firstYear) * yearWidth;
  const width = Math.ceil(axisWidth + 360), height = 164 + rows.length * 88;
  const x = value => 64 + (value - firstYear * 12) / 12 * yearWidth;
  return {rows, firstYear, lastYear, width, height, x, axisY: height - 72};
}
export const xml = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
function wrapTitle(title, max = 42) {
  const parts = []; let remaining = title;
  while (remaining.length > max && parts.length < 3) {
    let split = remaining.lastIndexOf(' ', max);
    if (split < max / 2) split = max;
    parts.push(remaining.slice(0, split)); remaining = remaining.slice(split).trim();
  }
  if (remaining) parts.push(remaining);
  return parts;
}
export function renderSVG(entries, title, covers = new Map()) {
  const {rows, firstYear, lastYear, width, height, x, axisY} = layout(entries);
  const parts = [`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="figure-title figure-description">`,
    `<title id="figure-title">${xml(title || 'My gaming history')}</title><desc id="figure-description">Gaming history with year ticks and month-accurate intervals. ${rows.map(row => xml(`${row.name}: ${dateLabel(row.from)} to ${dateLabel(row.to)}.`)).join(' ')}</desc>`,
    `<rect width="${width}" height="${height}" fill="#fffefb"/><g font-family="Arial, Helvetica, sans-serif" fill="#233b34">`,
    `<text x="42" y="44" font-size="${Math.min(25, (width - 84) / (Math.max(1, (title || 'My gaming history').length) * 0.65))}" font-weight="600">${xml(title || 'My gaming history')}</text>`,
    `<text x="42" y="68" font-size="11" fill="#64716a">${rows.length} ${rows.length === 1 ? 'game' : 'games'} · ${firstYear}–${Math.floor(Math.max(...rows.map(row => row.to)) / 12)}</text>`];
  for (let year = firstYear; year <= lastYear; year++) {
    const pos = x(year * 12);
    parts.push(`<line x1="${pos}" x2="${pos}" y1="87" y2="${axisY}" stroke="#e7e8df"/><line x1="${pos}" x2="${pos}" y1="${axisY}" y2="${axisY + 7}" stroke="#859488"/><text x="${pos}" y="${axisY + 28}" text-anchor="middle" font-size="12" fill="#64716a">${year}</text>`);
  }
  parts.push(`<line x1="64" x2="${x(lastYear * 12)}" y1="${axisY}" y2="${axisY}" stroke="#859488"/>`);
  rows.forEach((row, index) => {
    const y = 130 + index * 88, start = x(row.from), end = x(row.to), color = COLORS[index % COLORS.length];
    const data = covers.get(row.gameId || normalize(row.name));
    const image = typeof data === 'string' && /^data:image\/(png|jpeg|webp);base64,[A-Za-z0-9+/=]+$/.test(data) ? data : null;
    const lines = wrapTitle(row.name);
    // Titles are set above their segment and can extend into the right margin.
    const labelX = Math.min(start, width - 330);
    const labelY = y - 24;
    parts.push(`<g><title>${xml(row.name)}: ${dateLabel(row.from)}–${dateLabel(row.to)}</title>`);
    // Long titles use two compact lines, with full names in the SVG title/desc.
    const display = lines.length > 2 ? [lines[0], `${lines[1].slice(0, 39)}…`] : lines;
    display.forEach((line, j) => parts.push(`<text x="${labelX}" y="${labelY - (display.length - j - 1) * 17}" font-size="14" font-weight="600">${xml(line)}</text>`));
    parts.push(`<line class="play-segment" x1="${start}" x2="${end}" y1="${y}" y2="${y}" stroke="${color}" stroke-width="4" stroke-linecap="round"/><circle cx="${end}" cy="${y}" r="4" fill="${color}"/>`);
    if (image) parts.push(`<rect x="${start - 15}" y="${y - 20}" width="30" height="40" rx="2" fill="#fffefb"/><image href="${image}" x="${start - 13}" y="${y - 18}" width="26" height="36" preserveAspectRatio="xMidYMid meet"/>`);
    else parts.push(`<circle cx="${start}" cy="${y}" r="5" fill="#fffefb" stroke="${color}" stroke-width="2"/>`);
    parts.push('</g>');
  });
  parts.push(`<text x="42" y="${height - 17}" font-size="10" fill="#64716a">Each tick marks January${covers.size ? ' · Covers: IGDB via LizardByte GameDB' : ''}</text></g></svg>`);
  return parts.join('');
}
