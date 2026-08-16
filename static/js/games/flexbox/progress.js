(function (window) {
    "use strict";

    function storageKey(slug) {
        return "nayekola:progress:" + slug;
    }

    function getCookie(name) {
        var cookies = document.cookie ? document.cookie.split(";") : [];
        var i;
        for (i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.indexOf(name + "=") === 0) {
                return decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
        return "";
    }

    function readLocal(slug) {
        try {
            var raw = window.localStorage.getItem(storageKey(slug));
            return raw ? JSON.parse(raw) : null;
        } catch (error) {
            return null;
        }
    }

    function writeLocal(slug, progress) {
        var payload = {
            currentLevel: progress.currentLevel || 0,
            completedLevels: progress.completedLevels || [],
            isFinished: !!progress.isFinished,
            updatedAt: new Date().toISOString()
        };
        window.localStorage.setItem(storageKey(slug), JSON.stringify(payload));
        return payload;
    }

    function mergeProgress(localProgress, serverProgress) {
        var local = localProgress || {
            currentLevel: 0,
            completedLevels: [],
            isFinished: false,
            updatedAt: null
        };
        var server = serverProgress || {
            currentLevel: 0,
            completedLevels: [],
            isFinished: false,
            updatedAt: null
        };

        var completed = [];
        (local.completedLevels || []).concat(server.completedLevels || []).forEach(function (index) {
            if (completed.indexOf(index) === -1) {
                completed.push(index);
            }
        });
        completed.sort(function (a, b) {
            return a - b;
        });

        return {
            currentLevel: Math.max(local.currentLevel || 0, server.currentLevel || 0),
            completedLevels: completed,
            isFinished: !!(local.isFinished || server.isFinished),
            updatedAt: local.updatedAt || server.updatedAt || null
        };
    }

    function createProgressManager(options) {
        var slug = options.slug;
        var syncUrl = options.syncUrl;
        var statusEl = options.statusEl;
        var state = mergeProgress(readLocal(slug), options.serverProgress);
        writeLocal(slug, state);

        var syncTimer = null;
        var syncing = false;

        function setStatus(text) {
            if (statusEl) {
                statusEl.textContent = text || "";
            }
        }

        function getState() {
            return state;
        }

        function save(partial) {
            state = writeLocal(slug, Object.assign({}, state, partial || {}));
            scheduleSync();
            return state;
        }

        function scheduleSync() {
            if (syncTimer) {
                window.clearTimeout(syncTimer);
            }
            syncTimer = window.setTimeout(syncNow, 1200);
        }

        function syncNow() {
            if (!syncUrl || syncing || !window.navigator.onLine) {
                return;
            }

            syncing = true;
            setStatus("Sync…");

            fetch(syncUrl, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify(state)
            })
                .then(function (response) {
                    if (!response.ok) {
                        throw new Error("sync failed");
                    }
                    return response.json();
                })
                .then(function (serverState) {
                    state = mergeProgress(state, serverState);
                    writeLocal(slug, state);
                    setStatus("Sauvé");
                    window.setTimeout(function () {
                        setStatus("");
                    }, 1500);
                })
                .catch(function () {
                    setStatus("Hors ligne");
                })
                .finally(function () {
                    syncing = false;
                });
        }

        document.addEventListener("visibilitychange", function () {
            if (document.visibilityState === "hidden") {
                syncNow();
            }
        });

        window.addEventListener("online", syncNow);

        return {
            getState: getState,
            save: save,
            syncNow: syncNow
        };
    }

    window.NayekolaProgress = {
        createProgressManager: createProgressManager,
        mergeProgress: mergeProgress
    };
})(window);
