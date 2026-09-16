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

    function emptyProgress() {
        return {
            currentLevel: 0,
            completedLevels: [],
            isFinished: false,
            updatedAt: null
        };
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
            currentLevel: Number(progress.currentLevel) || 0,
            completedLevels: Array.isArray(progress.completedLevels)
                ? progress.completedLevels
                : [],
            isFinished: progress.isFinished === true,
            updatedAt: new Date().toISOString()
        };
        window.localStorage.setItem(storageKey(slug), JSON.stringify(payload));
        return payload;
    }

    function removeLocal(slug) {
        try {
            window.localStorage.removeItem(storageKey(slug));
        } catch (error) {
            /* ignore */
        }
    }

    function mergeProgress(localProgress, serverProgress) {
        var local = localProgress || emptyProgress();
        var server = serverProgress || emptyProgress();
        var localTime = local.updatedAt ? Date.parse(local.updatedAt) : 0;
        var serverTime = server.updatedAt ? Date.parse(server.updatedAt) : 0;

        // Si le local est un reset plus récent, ne pas réimporter un "terminé" serveur.
        if (
            localTime &&
            local.isFinished === false &&
            (local.completedLevels || []).length === 0 &&
            (local.currentLevel || 0) === 0 &&
            localTime >= serverTime
        ) {
            return {
                currentLevel: 0,
                completedLevels: [],
                isFinished: false,
                updatedAt: local.updatedAt
            };
        }

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
        var syncUrl = options.syncUrl || "";
        var statusEl = options.statusEl;
        var aliasSlugs = options.aliasSlugs || [];
        var local = readLocal(slug);
        var state;

        if (!syncUrl) {
            state = local || emptyProgress();
            if (!local) {
                writeLocal(slug, state);
            }
        } else {
            state = mergeProgress(local, options.serverProgress);
            writeLocal(slug, state);
        }

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

        function reset() {
            var i;
            removeLocal(slug);
            for (i = 0; i < aliasSlugs.length; i++) {
                removeLocal(aliasSlugs[i]);
            }
            state = writeLocal(slug, emptyProgress());
            if (syncTimer) {
                window.clearTimeout(syncTimer);
                syncTimer = null;
            }
            return state;
        }

        function scheduleSync() {
            if (!syncUrl) {
                return;
            }
            if (syncTimer) {
                window.clearTimeout(syncTimer);
            }
            syncTimer = window.setTimeout(function () {
                syncNow();
            }, 1200);
        }

        function syncNow(extraPayload, callback) {
            var done = typeof callback === "function" ? callback : function () {};
            var body;

            if (!syncUrl) {
                done(state);
                return;
            }
            if (syncing) {
                done(state);
                return;
            }
            if (!window.navigator.onLine) {
                done(state);
                return;
            }

            syncing = true;
            setStatus("Sync…");
            body = Object.assign({}, state, extraPayload || {});

            fetch(syncUrl, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify(body)
            })
                .then(function (response) {
                    if (!response.ok) {
                        throw new Error("sync failed");
                    }
                    return response.json();
                })
                .then(function (serverState) {
                    if (extraPayload && extraPayload.reset) {
                        state = writeLocal(slug, emptyProgress());
                    } else {
                        state = mergeProgress(state, serverState);
                        writeLocal(slug, state);
                    }
                    setStatus("Sauvé");
                    window.setTimeout(function () {
                        setStatus("");
                    }, 1500);
                    done(state);
                })
                .catch(function () {
                    setStatus("Hors ligne");
                    done(state);
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

        window.addEventListener("online", function () {
            syncNow();
        });

        return {
            getState: getState,
            save: save,
            reset: reset,
            syncNow: syncNow
        };
    }

    window.NayekolaProgress = {
        createProgressManager: createProgressManager,
        mergeProgress: mergeProgress
    };
})(window);
