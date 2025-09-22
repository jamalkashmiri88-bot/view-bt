// monitor.js
// Usage: node monitor.js
// Requires: node >= 16
// Install dependencies: npm install node-fetch xml2js

const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');
const xml2js = require('xml2js');

const CHANNEL_HANDLE_URL = 'https://www.youtube.com/@LostAndClassified'; // change if needed
const WEBHOOK_URL = process.env.WEBHOOK_URL || ''; // set in GitHub secrets
const STATE_FILE = path.resolve('seen.json');
const OUT_FILE = path.resolve('videos.json');

async function getChannelIdFromHandle(handleUrl) {
  // Try to fetch the handle page and extract "channelId":"UC..." from initial data
  const res = await fetch(handleUrl, { headers: { 'User-Agent': 'Mozilla/5.0' } });
  if (!res.ok) throw new Error('Failed to fetch handle URL: ' + res.status);
  const html = await res.text();
  // Search for "channelId":"UC..."
  const m = html.match(/"channelId"\s*:\s*"([^"]+)"/);
  if (m && m[1]) return m[1];
  // fallback: search for canonical link
  const m2 = html.match(/<link rel="canonical" href="https:\/\/www\.youtube\.com\/channel\/(UC[^"]+)"/);
  if (m2 && m2[1]) return m2[1];
  throw new Error('channelId not found in page HTML');
}

async function fetchRss(channelId) {
  const rssUrl = `https://www.youtube.com/feeds/videos.xml?channel_id=${channelId}`;
  const r = await fetch(rssUrl, { headers: { 'User-Agent': 'Mozilla/5.0' }});
  if (!r.ok) throw new Error('Failed fetching RSS: ' + r.status);
  const xml = await r.text();
  const parsed = await xml2js.parseStringPromise(xml, { explicitArray: false });
  return parsed;
}

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch (e) {
    return { seen: [] };
  }
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), 'utf8');
}

function loadOut() {
  try { return JSON.parse(fs.readFileSync(OUT_FILE, 'utf8')); } catch (e) { return { videos: [] }; }
}
function saveOut(out) {
  fs.writeFileSync(OUT_FILE, JSON.stringify(out, null, 2), 'utf8');
}

async function sendWebhook(video) {
  if (!WEBHOOK_URL) {
    console.log('WEBHOOK_URL not configured, skipping webhook. New video:', video.link);
    return;
  }
  const payload = {
    username: 'ChannelMonitor',
    embeds: [{
      title: video.title,
      url: video.link,
      description: video.description ? video.description.slice(0,200) : '',
      timestamp: video.published,
      footer: { text: 'YouTube channel monitor' }
    }]
  };
  try {
    const res = await fetch(WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      console.warn('Webhook returned', res.status);
    } else {
      console.log('Webhook sent for', video.id);
    }
  } catch (err) {
    console.warn('Failed to send webhook:', err.message);
  }
}

(async () => {
  try {
    console.log('Resolving channelId from handle URL:', CHANNEL_HANDLE_URL);
    const channelId = await getChannelIdFromHandle(CHANNEL_HANDLE_URL);
    console.log('Channel ID:', channelId);

    const rss = await fetchRss(channelId);
    const entries = rss.feed && rss.feed.entry ? (Array.isArray(rss.feed.entry) ? rss.feed.entry : [rss.feed.entry]) : [];
    console.log('Found entries:', entries.length);

    const state = loadState();
    const out = loadOut();

    const seenSet = new Set(state.seen || []);
    let newCount = 0;

    // Each entry has <id> tag with 'yt:video:VIDEOID' or link href
    for (const e of entries) {
      const idTag = e['yt:videoId'] || (typeof e.id === 'string' ? (e.id.includes(':') ? e.id.split(':').pop() : e.id) : null);
      const videoId = idTag;
      if (!videoId) continue;
      if (seenSet.has(videoId)) continue;

      // New video!
      const title = e.title || '';
      const link = (e.link && e.link.href) ? e.link.href : `https://www.youtube.com/watch?v=${videoId}`;
      const published = e.published || e['published'] || null;
      const description = e['media:group'] && e['media:group']['media:description'] ? e['media:group']['media:description'] : (e.summary || '');

      const video = { id: videoId, title, link, published, description };
      out.videos.unshift(video); // add newest first
      await sendWebhook(video);

      seenSet.add(videoId);
      newCount++;
      console.log('New video saved:', videoId, title);
    }

    // Trim out.videos to e.g., 1000 entries to keep file small
    out.videos = out.videos.slice(0, 1000);
    saveOut(out);

    state.seen = Array.from(seenSet);
    saveState(state);

    console.log('Done. New videos found:', newCount);
  } catch (err) {
    console.error('Error:', err.message || err);
    process.exit(1);
  }
})();
