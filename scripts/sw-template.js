const PREFIX='resus-'+encodeURIComponent(self.registration.scope)+'-';const CACHE=PREFIX+__CACHE__;const ASSETS=__ASSETS__;
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS))));
// User explicitly activates updates. Existing windows reload after controller changes.
self.addEventListener('message',e=>{if(e.data?.type==='ACTIVATE')self.skipWaiting()});
self.addEventListener('activate',e=>e.waitUntil((async()=>{await self.clients.claim();const keys=await caches.keys();await Promise.all(keys.filter(k=>k.startsWith(PREFIX)&&k!==CACHE).map(k=>caches.delete(k)));const clients=await self.clients.matchAll({type:'window'});for(const c of clients)c.postMessage({type:'UPDATED'})})()));
self.addEventListener('fetch',e=>{if(e.request.method!=='GET'||new URL(e.request.url).origin!==self.location.origin)return;e.respondWith((async()=>{const cache=await caches.open(CACHE);const url=new URL(e.request.url);if(e.request.mode==='navigate')return await cache.match('./index.html')||fetch(e.request);return await cache.match(url.href)||fetch(e.request)})())});
