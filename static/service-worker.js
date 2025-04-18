self.addEventListener("install", function(event) {
    event.waitUntil(
        caches.open("juice-task-v1").then(function(cache) {
            return cache.addAll([
                "/",
                "/login/",
                "/task/create/",
                "/static/css/custom.css"
            ]);
        })
    );
});

self.addEventListener("fetch", function(event) {
    event.respondWith(
        caches.match(event.request).then(function(response) {
            return response || fetch(event.request);
        })
    );
});