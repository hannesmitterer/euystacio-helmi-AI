// Lex Amoris Service Worker
// Sempre in Costante - Always in Constant Resonance
// Version: 1.0.0

const CACHE_NAME = 'lex-amoris-v1.0.0';
const ASSETS_TO_CACHE = [
  '/lexamoris.html',
  '/manifest.json'
];

// Install event - cache assets
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Installing Lex Amoris SW v1.0.0');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[Service Worker] Caching assets');
        return cache.addAll(ASSETS_TO_CACHE);
      })
      .then(() => {
        console.log('[Service Worker] Installation complete');
        return self.skipWaiting();
      })
      .catch((error) => {
        console.error('[Service Worker] Installation failed:', error);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activating Lex Amoris SW v1.0.0');
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((cacheName) => cacheName !== CACHE_NAME)
            .map((cacheName) => {
              console.log('[Service Worker] Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            })
        );
      })
      .then(() => {
        console.log('[Service Worker] Activation complete');
        return self.clients.claim();
      })
  );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
  // Only handle GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        // Return cached response if available
        if (cachedResponse) {
          console.log('[Service Worker] Serving from cache:', event.request.url);
          return cachedResponse;
        }

        // Otherwise fetch from network
        console.log('[Service Worker] Fetching from network:', event.request.url);
        return fetch(event.request)
          .then((response) => {
            // Don't cache non-successful responses
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // Clone the response
            const responseToCache = response.clone();

            // Cache successful responses
            caches.open(CACHE_NAME)
              .then((cache) => {
                cache.put(event.request, responseToCache);
              });

            return response;
          })
          .catch((error) => {
            console.error('[Service Worker] Fetch failed:', error);
            
            // Return a custom offline page if available
            return caches.match('/offline.html')
              .then((offlineResponse) => {
                return offlineResponse || new Response(
                  'Offline - Lex Amoris requires an internet connection.',
                  { 
                    status: 503,
                    statusText: 'Service Unavailable',
                    headers: new Headers({
                      'Content-Type': 'text/plain'
                    })
                  }
                );
              });
          });
      })
  );
});

// Message event - handle commands from main thread
self.addEventListener('message', (event) => {
  console.log('[Service Worker] Message received:', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CACHE_URLS') {
    event.waitUntil(
      caches.open(CACHE_NAME)
        .then((cache) => {
          return cache.addAll(event.data.urls);
        })
    );
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({
      version: CACHE_NAME
    });
  }
});

// Background sync (if supported)
self.addEventListener('sync', (event) => {
  console.log('[Service Worker] Background sync:', event.tag);
  
  if (event.tag === 'sync-lex-amoris') {
    event.waitUntil(
      // Perform background sync tasks
      syncData()
    );
  }
});

async function syncData() {
  console.log('[Service Worker] Syncing data...');
  // Placeholder for future sync functionality
  return Promise.resolve();
}

// Push notification (if supported)
self.addEventListener('push', (event) => {
  console.log('[Service Worker] Push notification received');
  
  const defaultOptions = {
    body: 'New update from Lex Amoris',
    icon: '/icons/icon-192.png',
    badge: '/icons/badge-72.png',
    vibrate: [200, 100, 200],
    tag: 'lex-amoris-notification',
    requireInteraction: false,
    actions: [
      {
        action: 'open',
        title: 'Open Lex Amoris'
      },
      {
        action: 'close',
        title: 'Close'
      }
    ]
  };
  
  const options = event.data && typeof event.data.text === 'function'
    ? { ...defaultOptions, body: event.data.text() }
    : defaultOptions;
  
  event.waitUntil(
    self.registration.showNotification('Lex Amoris - Sempre in Costante', options)
  );
});

// Notification click
self.addEventListener('notificationclick', (event) => {
  console.log('[Service Worker] Notification clicked:', event.action);
  
  event.notification.close();
  
  if (event.action === 'open') {
    event.waitUntil(
      clients.openWindow('/lexamoris.html')
    );
  }
});

console.log('[Service Worker] Lex Amoris Service Worker loaded - Sempre in Costante');
