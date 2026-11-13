#!/usr/bin/env node
// tools/test-table.js — browser tests for the terminal's "table" commands (MEET, PACKET, SAY, REST, SLEEP, LEAVE, SAVE, OFFER).
// Needs: playwright (and, optionally, axe-core); the site served at http://localhost:8123 (python3 -m http.server 8123 in this repo);
// and a keeper running with a stand-in model, no cost:
//   cd ../theinfinitecorridor/engine && KEEPER_MODE=open KEEPER_ORIGINS=http://localhost:8123 KEEPER_RPM_IP=500 KEEPER_RPM_SESSION=60 PORT=8790 node keeper.js
// Then: node tools/test-table.js
const { chromium } = require('playwright');
const assert = require('assert').strict;
const fs = require('fs');
let axe = null; try { axe = fs.readFileSync(require.resolve('axe-core/axe.min.js'), 'utf8'); } catch (e) {}
const BASE = 'http://localhost:8123/terminal/';
let n = 0; const ok = (m) => { n++; console.log('  ok  ' + m); };
async function type(page, line) { await page.fill('#in', line); await page.press('#in', 'Enter'); await page.waitForTimeout(450); }
const outText = (page) => page.evaluate(() => document.getElementById('out').innerText);
(async () => {
  const b = await chromium.launch();
  // 1. no keeper: nothing changes
  let ctx = await b.newContext({ acceptDownloads: true }); let page = await ctx.newPage();
  await page.goto(BASE); await page.waitForTimeout(900);
  await type(page, 'HELP'); let t = await outText(page);
  assert(!/The table/.test(t) && !/MEET/.test(t)); ok('no keeper: HELP does not mention the table');
  await type(page, 'MEET'); t = await outText(page);
  assert(/The table is not set/.test(t)); ok('no keeper: MEET says the table is not set');
  await type(page, 'REST'); await type(page, 'PACKET'); t = await outText(page);
  assert((t.match(/The table is not set/g) || []).length >= 3); ok('no keeper: REST and PACKET say so too');
  await ctx.close();

  // 2. a bad address is ignored
  ctx = await b.newContext(); page = await ctx.newPage();
  await page.goto(BASE + '?keeper=https://evil.example'); await page.waitForTimeout(700);
  await type(page, 'MEET'); t = await outText(page); assert(/The table is not set/.test(t)); ok('a link cannot point the terminal at a server that is not on the list');
  await ctx.close();

  // 3. the full visit
  ctx = await b.newContext({ acceptDownloads: true }); page = await ctx.newPage();
  let alerted = false; page.on('dialog', (d) => { alerted = true; d.dismiss(); });
  await page.goto(BASE + '?keeper=http://localhost:8790'); await page.waitForTimeout(900);
  await type(page, 'HELP'); t = await outText(page); assert(/The table/.test(t) && /MEET/.test(t)); ok('with a keeper: HELP lists the table');
  await type(page, 'MEET'); t = await outText(page);
  assert(/Two chairs\. One table\. Coffee\./.test(t) && /At the table: stand-in/.test(t) && !/SESSION:/.test(t) && /The table is at localhost:8790/.test(t)); ok('MEET shows the notice, says where it is talking, hides the session id');
  assert.equal(await page.evaluate(() => document.getElementById('ps').textContent), 'VISITOR> '); ok('the prompt changes to VISITOR> while seated');
  assert.equal(await page.evaluate(() => document.getElementById('in').autocapitalize), 'sentences'); ok('typing is no longer forced into capitals while seated');
  await type(page, 'Hello. Who are you?'); t = await outText(page); assert(/STAND-IN> /.test(t) && /\(about|I don't know/.test(t)); ok('plain words are speech; the table answers');
  await type(page, '<img src=x onerror="window.__xss=1"> hi'); t = await outText(page);
  const injected = await page.evaluate(() => ({ imgs: document.querySelectorAll('#out img').length, xss: window.__xss === 1 }));
  assert.equal(injected.imgs, 0); assert(!injected.xss && !alerted); ok('a reply that echoes HTML is shown as text and nothing runs');
  await type(page, 'read me a poem'); t = await outText(page); assert(/STAND-IN> /.test(t) && !/Opening/.test(t)); ok('while seated, "read me a poem" is speech, not the READ command');
  await type(page, 'PACKET'); t = await outText(page); assert(/You are a language model/.test(t) && /THE COMPASS ROSE/.test(t)); ok('PACKET shows every word the model is given');
  await type(page, 'REST'); t = await outText(page); assert(/Nothing is asked and nothing is spent/.test(t)); ok('REST');
  const dl = page.waitForEvent('download', { timeout: 4000 });
  await type(page, 'SAVE'); const d = await dl; assert(/the-table_/.test(d.suggestedFilename())); ok('SAVE downloads a copy');
  await type(page, 'OFFER'); t = await outText(page); assert(/Offered/.test(t)); ok('OFFER');
  if (axe) { await page.evaluate(axe);
  const r = await page.evaluate(async () => await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag22aa'] } }));
  assert.equal(r.violations.length, 0, r.violations.map((v) => v.id).join(',')); ok('axe: no WCAG A/AA violations while seated'); }
  await type(page, 'LEAVE PRIVATE'); t = await outText(page); assert(/Nothing of this visit is kept/.test(t)); ok('LEAVE PRIVATE takes everything back');
  assert.match(await page.evaluate(() => document.getElementById('ps').textContent), /INFINITE_CORRIDOR/); ok('the prompt returns after leaving');
  await type(page, 'SAY hi'); t = await outText(page); assert(/No one is sitting here/.test(t)); ok('after leaving, the seat is empty');
  // remembered across a reload; forgotten with ?keeper=off
  await page.goto(BASE); await page.waitForTimeout(700); await type(page, 'HELP'); t = await outText(page); assert(/MEET/.test(t)); ok('the keeper address is remembered in this browser');
  await page.goto(BASE + '?keeper=off'); await page.waitForTimeout(700); await type(page, 'MEET'); t = await outText(page); assert(/not set/.test(t)); ok('?keeper=off forgets it');
  await ctx.close();

  // 4. an unreachable keeper fails gently; LEAVE with no seat is still EXIT
  ctx = await b.newContext(); page = await ctx.newPage();
  await page.goto(BASE + '?keeper=http://localhost:8799'); await page.waitForTimeout(700);
  await type(page, 'MEET'); t = await outText(page); assert(/can't be reached right now/.test(t)); ok('an unreachable keeper fails gently');
  await type(page, 'LEAVE'); await page.waitForTimeout(900); assert(/home\.html|\/$/.test(page.url()) || /room remains open/i.test(await outText(page))); ok('LEAVE with no seat still behaves as EXIT');
  await ctx.close();

  // 5. phone width
  ctx = await b.newContext({ viewport: { width: 390, height: 844 } }); page = await ctx.newPage();
  await page.goto(BASE + '?keeper=http://localhost:8790'); await page.waitForTimeout(900);
  await type(page, 'MEET'); await type(page, 'Hello'); t = await outText(page); assert(/STAND-IN> /.test(t)); ok('works at phone width');
  await ctx.close();
  await b.close();
  console.log('\nterminal table: ' + n + ' checks passed');
})().catch((e) => { console.error('FAIL:', e.message.slice(0, 300)); process.exit(1); });
