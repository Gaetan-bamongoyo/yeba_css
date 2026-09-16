(function () {
    "use strict";

    var root = document.getElementById("game-root");
    if (!root || typeof alasql === "undefined") {
        return;
    }

    var levels = JSON.parse(document.getElementById("game-levels").textContent);
    var dataset = JSON.parse(document.getElementById("sql-dataset").textContent);
    var serverProgress = JSON.parse(document.getElementById("game-progress").textContent);
    var victoryConfig = {};
    var victoryEl = document.getElementById("mission-victory");
    if (victoryEl) {
        victoryConfig = JSON.parse(victoryEl.textContent);
    }
    var progressSlug =
        root.getAttribute("data-progress-slug") ||
        root.dataset.progressSlug ||
        root.getAttribute("data-game-slug") ||
        root.dataset.gameSlug;
    var stabilityLabel =
        root.getAttribute("data-stability-label") ||
        root.dataset.stabilityLabel ||
        "Enquête";

    var progressAliases = {
        "sql-mission-enfant-retrouve": [
            "sql:mission:enfant-retrouve",
            "sql:enfant-retrouve",
            "sql"
        ],
        "sql-mission-annee-academique": [
            "sql:mission:annee-academique",
            "sql:annee-academique"
        ]
    };
    var aliasSlugs = progressAliases[progressSlug] || [];
    var progressStoragePrefix = "nayekola:progress:";
    var resetFlagKey = "nayekola:just-reset:" + progressSlug;

    function emptyProgressPayload() {
        return {
            currentLevel: 0,
            completedLevels: [],
            isFinished: false,
            updatedAt: new Date().toISOString()
        };
    }

    function wipeMissionProgress() {
        var empty = JSON.stringify(emptyProgressPayload());
        var known = {};
        var i;
        var key;
        var shortName;
        var keys = [];

        known[progressSlug] = true;
        for (i = 0; i < aliasSlugs.length; i++) {
            known[aliasSlugs[i]] = true;
        }

        for (i = 0; i < window.localStorage.length; i++) {
            keys.push(window.localStorage.key(i));
        }
        for (i = 0; i < keys.length; i++) {
            key = keys[i];
            if (!key || key.indexOf(progressStoragePrefix) !== 0) {
                continue;
            }
            shortName = key.slice(progressStoragePrefix.length);
            if (known[shortName]) {
                try {
                    window.localStorage.removeItem(key);
                } catch (error) {
                    /* ignore */
                }
            }
        }
        try {
            window.localStorage.setItem(progressStoragePrefix + progressSlug, empty);
        } catch (error) {
            /* ignore */
        }
    }

    // Si on revient juste après "Rejouer", force l'état vierge.
    if (window.sessionStorage.getItem(resetFlagKey) === "1") {
        window.sessionStorage.removeItem(resetFlagKey);
        wipeMissionProgress();
    }

    var progressManager = window.NayekolaProgress.createProgressManager({
        slug: progressSlug,
        syncUrl: "",
        serverProgress: emptyProgressPayload(),
        aliasSlugs: aliasSlugs,
        statusEl: document.getElementById("sync-status")
    });

    var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
        mode: "text/x-sql",
        lineNumbers: true,
        theme: "default",
        extraKeys: {
            "Ctrl-Space": "autocomplete",
            "Cmd-Space": "autocomplete",
            "Ctrl-Enter": function () {
                runQuery();
            }
        },
        hintOptions: {
            tables: {},
            completeSingle: false
        }
    });

    var saved = progressManager.getState();
    var currentLevel = Math.min(saved.currentLevel || 0, Math.max(levels.length - 1, 0));
    var hasFinishedGame = !!saved.isFinished;
    var failedAttempts = 0;
    var hintRevealed = false;
    var hintLevel = 0;
    var protectedMarks = [];
    var lastRows = null;
    var activeTables = [];

    var hintBtn = document.getElementById("hint-btn");
    var hintText = document.getElementById("hint-text");
    var enigmaText = document.getElementById("enigma-text");
    var sceneTag = document.getElementById("scene-tag");
    var stabilityValue = document.getElementById("stability-value");
    var stabilityFill = document.getElementById("stability-fill");
    var resultBox = document.getElementById("sql-result");
    var previewBox = document.getElementById("sql-table-preview");
    var chipsBox = document.getElementById("sql-table-chips");

    function getLevelTables(level) {
        var names = ((level && level.target) || {}).tables;
        if (names && names.length) {
            return names.filter(function (name) {
                return Object.prototype.hasOwnProperty.call(dataset, name);
            });
        }
        return Object.keys(dataset);
    }

    function buildHintTables(tableNames) {
        var tables = {};
        (tableNames || []).forEach(function (name) {
            var rows = dataset[name] || [];
            tables[name] = rows.length ? Object.keys(rows[0]) : [];
        });
        return tables;
    }

    function syncDatabase(tableNames) {
        Object.keys(dataset).forEach(function (tableName) {
            alasql("DROP TABLE IF EXISTS " + tableName);
        });
        (tableNames || []).forEach(function (tableName) {
            alasql("CREATE TABLE " + tableName);
            alasql.tables[tableName].data = (dataset[tableName] || []).map(function (row) {
                return Object.assign({}, row);
            });
        });
    }

    function renderTableChips(tableNames) {
        if (!chipsBox) {
            return;
        }
        chipsBox.innerHTML = "";
        if (!tableNames.length) {
            chipsBox.innerHTML =
                '<p class="sql-result-empty">Aucune table débloquée pour cette énigme.</p>';
            if (previewBox) {
                previewBox.innerHTML = "";
            }
            return;
        }
        tableNames.forEach(function (name) {
            var chip = document.createElement("button");
            chip.type = "button";
            chip.className = "sql-chip";
            chip.setAttribute("data-table", name);
            chip.textContent = name;
            chip.addEventListener("click", function () {
                showTablePreview(name);
            });
            chipsBox.appendChild(chip);
        });
        showTablePreview(tableNames[0]);
    }

    function unlockTablesForLevel(level) {
        activeTables = getLevelTables(level);
        syncDatabase(activeTables);
        editor.setOption("hintOptions", {
            tables: buildHintTables(activeTables),
            completeSingle: false
        });
        renderTableChips(activeTables);
    }

    function clearProtectedMarks() {
        protectedMarks.forEach(function (mark) {
            mark.clear();
        });
        protectedMarks = [];
    }

    function setupProtectedStarter(starterCode) {
        var code = (starterCode || "").trim();
        var editableLine;
        var doc;

        clearProtectedMarks();

        // SQL : l'utilisateur écrit toute la requête (pas de code prérempli).
        if (!code) {
            editor.setValue("");
            editor.setCursor({ line: 0, ch: 0 });
            return;
        }

        if (!code.endsWith("\n")) {
            code += "\n";
        }
        code += " ";
        editor.setValue(code);

        editableLine = editor.lineCount() - 1;
        doc = editor.getDoc();

        if (editableLine > 0) {
            protectedMarks.push(
                doc.markText(
                    { line: 0, ch: 0 },
                    { line: editableLine, ch: 0 },
                    {
                        readOnly: true,
                        inclusiveLeft: true,
                        inclusiveRight: false,
                        className: "cm-protected"
                    }
                )
            );
        }

        editor.setCursor({ line: editableLine, ch: editor.getLine(editableLine).length });
    }

    function updateStability() {
        var state = progressManager.getState();
        var completed = (state.completedLevels || []).length;
        var total = Math.max(levels.length, 1);
        var percent = Math.round((completed / total) * 100);
        if (hasFinishedGame) {
            percent = 100;
        }
        if (stabilityValue) {
            stabilityValue.textContent = percent + "%";
        }
        if (stabilityFill) {
            stabilityFill.style.width = percent + "%";
        }
        var meterLabel = document.querySelector(".stability-meter-top span");
        if (meterLabel && stabilityLabel) {
            meterLabel.textContent = stabilityLabel;
        }
    }

    function resetHintState() {
        failedAttempts = 0;
        hintRevealed = false;
        hintLevel = 0;
        if (hintText) {
            hintText.classList.add("is-hidden");
            hintText.innerHTML = "";
        }
        if (hintBtn) {
            hintBtn.disabled = false;
            hintBtn.textContent = "Révéler un indice";
        }
    }

    function getLevelHints(level) {
        if (level && level.hints && level.hints.length) {
            return level.hints;
        }
        if (level && level.hint) {
            return [level.hint];
        }
        return ["Vérifie le nom des tables et la clause WHERE."];
    }

    function revealHint(auto) {
        var level = levels[currentLevel];
        var hints;
        if (!level || !hintText || !hintBtn) {
            return;
        }
        hints = getLevelHints(level);
        hintRevealed = true;
        hintText.innerHTML =
            "<strong>Indice " +
            (hintLevel + 1) +
            "/" +
            hints.length +
            " :</strong> " +
            hints[Math.min(hintLevel, hints.length - 1)];
        hintText.classList.remove("is-hidden");
        hintBtn.disabled = hintLevel >= hints.length - 1;
        hintBtn.textContent = hintLevel >= hints.length - 1
            ? (auto ? "Indice débloqué" : "Indice révélé")
            : "Indice suivant";
        hintLevel += 1;
    }

    function normalizeValue(value) {
        if (value === null || value === undefined) {
            return "";
        }
        return String(value).trim().toLowerCase();
    }

    function parseNumeric(value) {
        if (value === null || value === undefined || value === "") {
            return null;
        }
        var num = Number(value);
        return Number.isFinite(num) ? num : null;
    }

    function valuesMatch(actual, expected, tolerance) {
        var actualNum = parseNumeric(actual);
        var expectedNum = parseNumeric(expected);
        if (actualNum !== null && expectedNum !== null) {
            return Math.abs(actualNum - expectedNum) <= (tolerance || 0.001);
        }
        return normalizeValue(actual) === normalizeValue(expected);
    }

    function rowMatches(row, match, tolerance) {
        var key;
        if (!row || !match) {
            return false;
        }
        for (key in match) {
            if (!Object.prototype.hasOwnProperty.call(match, key)) {
                continue;
            }
            if (!valuesMatch(row[key], match[key], tolerance)) {
                return false;
            }
        }
        return true;
    }

    function findMatchingRow(rows, expected, tolerance, usedIndexes) {
        var i;
        for (i = 0; i < rows.length; i++) {
            if (usedIndexes.indexOf(i) !== -1) {
                continue;
            }
            if (rowMatches(rows[i], expected, tolerance)) {
                return i;
            }
        }
        return -1;
    }

    function renderTable(rows, target) {
        var html;
        var columns;
        var i;
        var j;

        if (!target) {
            return;
        }
        if (!rows || !rows.length) {
            target.innerHTML = '<p class="sql-result-empty">Aucune ligne retournée.</p>';
            return;
        }

        columns = Object.keys(rows[0]);
        html = "<table><thead><tr>";
        for (i = 0; i < columns.length; i++) {
            html += "<th>" + columns[i] + "</th>";
        }
        html += "</tr></thead><tbody>";
        for (i = 0; i < rows.length; i++) {
            html += "<tr>";
            for (j = 0; j < columns.length; j++) {
                html += "<td>" + String(rows[i][columns[j]]) + "</td>";
            }
            html += "</tr>";
        }
        html += "</tbody></table>";
        target.innerHTML = html;
    }

    function showTablePreview(tableName) {
        var rows = dataset[tableName] || [];
        var sample = rows.slice(0, 5);
        if (!previewBox) {
            return;
        }
        previewBox.innerHTML =
            "<p class=\"sql-preview-title\">Aperçu : <strong>" +
            tableName +
            "</strong> (" +
            rows.length +
            " lignes)</p>";
        var holder = document.createElement("div");
        previewBox.appendChild(holder);
        renderTable(sample, holder);
    }

    function runQuery(options) {
        var opts = options || {};
        var sql = editor.getValue().trim();
        var feedback = document.querySelector(".level-feedback");
        var rows;

        syncDatabase(activeTables);

        if (!sql) {
            lastRows = null;
            if (resultBox) {
                resultBox.innerHTML =
                    '<p class="sql-result-empty">Écris une requête SQL, puis clique sur Exécuter.</p>';
            }
            if (feedback && !opts.silentFeedback) {
                feedback.classList.remove("error", "success");
                feedback.textContent = "Le terminal est vide.";
            }
            return null;
        }

        try {
            rows = alasql(sql);
            if (!Array.isArray(rows)) {
                rows = [{ result: rows }];
            }
            lastRows = rows;
            renderTable(rows, resultBox);
            if (feedback && !opts.silentFeedback) {
                feedback.classList.remove("error", "success");
                feedback.textContent =
                    "Test : " +
                    rows.length +
                    " ligne" +
                    (rows.length > 1 ? "s" : "") +
                    " — affine ta requête ou valide l'énigme.";
            }
            return rows;
        } catch (error) {
            lastRows = null;
            if (resultBox) {
                resultBox.innerHTML =
                    '<p class="sql-result-error">Erreur SQL : ' +
                    (error.message || "requête invalide") +
                    "</p>";
            }
            if (feedback && !opts.silentFeedback) {
                feedback.classList.add("error");
                feedback.classList.remove("success");
                feedback.textContent = "La requête a échoué. Corrige-la et réessaie (Exécuter).";
            }
            return null;
        }
    }

    function validateResult(rows, validation) {
        var i;
        var tolerance = validation.numeric_tolerance || validation.numericTolerance || 0.001;
        var usedIndexes;

        if (!validation) {
            return false;
        }
        if (!rows) {
            return false;
        }

        if (validation.type === "row_count") {
            return rows.length === validation.count;
        }

        if (validation.type === "contains_row") {
            for (i = 0; i < rows.length; i++) {
                if (rowMatches(rows[i], validation.match, tolerance)) {
                    return true;
                }
            }
            return false;
        }

        if (validation.type === "first_row") {
            return rows.length > 0 && rowMatches(rows[0], validation.match, tolerance);
        }

        if (validation.type === "exact_result" || validation.type === "ordered_result") {
            if (!validation.rows || rows.length !== validation.rows.length) {
                return false;
            }
            for (i = 0; i < validation.rows.length; i++) {
                if (!rowMatches(rows[i], validation.rows[i], tolerance)) {
                    return false;
                }
            }
            return true;
        }

        if (validation.type === "result_set") {
            if (!validation.rows || rows.length !== validation.rows.length) {
                return false;
            }
            usedIndexes = [];
            for (i = 0; i < validation.rows.length; i++) {
                var matchIndex = findMatchingRow(rows, validation.rows[i], tolerance, usedIndexes);
                if (matchIndex === -1) {
                    return false;
                }
                usedIndexes.push(matchIndex);
            }
            return true;
        }

        return false;
    }

    function loadLevel(index) {
        var level = levels[index];
        var feedback = document.querySelector(".level-feedback");

        currentLevel = index;
        lastRows = null;
        resetHintState();

        document.querySelector(".level-title").textContent = level.title;
        document.querySelector(".level-difficulty").textContent = level.difficulty;
        document.querySelector(".level-progress").textContent =
            index + 1 + " / " + levels.length;

        if (sceneTag) {
            sceneTag.textContent = level.scene || "Dossier";
        }
        if (enigmaText) {
            if (level.objectiveHtml) {
                enigmaText.innerHTML = level.objectiveHtml;
            } else {
                enigmaText.textContent = level.objective || "";
            }
        }
        if (feedback) {
            feedback.textContent = "";
            feedback.classList.remove("error", "success");
        }
        if (resultBox) {
            resultBox.innerHTML =
                '<p class="sql-result-empty">Exécute une requête pour voir les lignes.</p>';
        }

        document.getElementById("check-btn").textContent = hasFinishedGame
            ? "VOIR LA FIN"
            : "VALIDER L'ÉNIGME";

        setupProtectedStarter(level.starterCode || "");
        unlockTablesForLevel(level);
        updateStability();
        progressManager.save({
            currentLevel: currentLevel,
            isFinished: hasFinishedGame
        });
    }

    function markLevelCompleted(index) {
        var state = progressManager.getState();
        var completed = (state.completedLevels || []).slice();
        if (completed.indexOf(index) === -1) {
            completed.push(index);
        }
        progressManager.save({
            currentLevel: index,
            completedLevels: completed,
            isFinished: hasFinishedGame
        });
        updateStability();
    }

    function applyVictoryConfig() {
        var kicker = document.querySelector(".victory-kicker");
        var title = document.getElementById("victory-title");
        var text = document.querySelector(".victory-text");
        var note = document.querySelector(".victory-note");
        if (kicker && victoryConfig.kicker) {
            kicker.textContent = victoryConfig.kicker;
        }
        if (title && victoryConfig.title) {
            title.textContent = victoryConfig.title;
        }
        if (text && victoryConfig.text) {
            text.textContent = victoryConfig.text;
        }
        if (note && victoryConfig.note) {
            note.textContent = victoryConfig.note;
        }
    }

    function showVictoryModal() {
        var modal = document.getElementById("victory-modal");
        if (!modal) {
            return;
        }
        applyVictoryConfig();
        if (lastRows && lastRows.length && document.getElementById("victory-result")) {
            renderTable(lastRows, document.getElementById("victory-result"));
        }
        modal.hidden = false;
        modal.classList.remove("is-hidden");
        document.body.classList.add("victory-open");
    }

    function hideVictoryModal() {
        var modal = document.getElementById("victory-modal");
        if (!modal) {
            return;
        }
        modal.hidden = true;
        modal.classList.add("is-hidden");
        document.body.classList.remove("victory-open");
    }

    function validateLevel() {
        var feedback = document.querySelector(".level-feedback");
        var level = levels[currentLevel];
        var validation = (level.target || {}).validation || {};
        var rows = runQuery({ silentFeedback: true });

        if (rows === null) {
            return;
        }

        if (!validateResult(rows, validation)) {
            failedAttempts += 1;
            feedback.classList.add("error");
            feedback.classList.remove("success");
            if (failedAttempts >= 2 && !hintRevealed) {
                revealHint(true);
                feedback.textContent =
                    "Ce n'est pas encore la bonne piste… Un indice apparaît.";
            } else {
                feedback.textContent =
                    "Résultat incorrect. Relis l'énigme et affine ta requête.";
            }
            return;
        }

        feedback.classList.remove("error");
        feedback.classList.add("success");
        markLevelCompleted(currentLevel);

        if (currentLevel < levels.length - 1) {
            feedback.textContent = level.successMessage || "Étape validée. Mission suivante…";
            currentLevel += 1;
            progressManager.save({ currentLevel: currentLevel });
            window.setTimeout(function () {
                loadLevel(currentLevel);
            }, 800);
        } else {
            hasFinishedGame = true;
            feedback.textContent = victoryConfig.title || "Mission terminée !";
            document.getElementById("check-btn").textContent = "VOIR LA FIN";
            progressManager.save({
                currentLevel: currentLevel,
                isFinished: true
            });
            updateStability();
            progressManager.syncNow();
            window.setTimeout(showVictoryModal, 400);
        }
    }

    function restartGame() {
        // Efface toutes les clés de cette mission, marque le reset, puis recharge.
        try {
            window.sessionStorage.setItem(resetFlagKey, "1");
        } catch (error) {
            /* ignore */
        }
        wipeMissionProgress();
        if (progressManager && typeof progressManager.reset === "function") {
            try {
                progressManager.reset();
            } catch (error) {
                /* ignore */
            }
        }
        window.location.reload();
    }

    function handleCheckClick() {
        if (hasFinishedGame) {
            showVictoryModal();
            return;
        }
        validateLevel();
    }

    function maybeShowHints(cm, change) {
        if (!change || !change.text || !change.text[0]) {
            return;
        }
        if (!/[a-zA-Z_]/.test(change.text[0])) {
            return;
        }
        if (cm.state.completionActive) {
            return;
        }
        CodeMirror.commands.autocomplete(cm);
    }

    if (hintBtn) {
        hintBtn.addEventListener("click", function () {
            revealHint(false);
        });
    }

    var victoryRestart = document.getElementById("victory-restart");
    if (victoryRestart) {
        victoryRestart.addEventListener("click", restartGame);
    }

    document.querySelectorAll("[data-victory-close]").forEach(function (el) {
        el.addEventListener("click", hideVictoryModal);
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            hideVictoryModal();
        }
    });

    editor.on("inputRead", maybeShowHints);
    document.getElementById("run-btn").addEventListener("click", runQuery);
    document.getElementById("check-btn").addEventListener("click", handleCheckClick);

    applyVictoryConfig();
    loadLevel(currentLevel);
    if (hasFinishedGame) {
        window.setTimeout(showVictoryModal, 300);
    }
})();
