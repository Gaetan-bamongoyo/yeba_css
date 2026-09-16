(function () {
    "use strict";

    var root = document.getElementById("game-root");
    if (!root) {
        return;
    }

    var levels = JSON.parse(document.getElementById("game-levels").textContent);
    var serverProgress = JSON.parse(document.getElementById("game-progress").textContent);
    var progressManager = window.NayekolaProgress.createProgressManager({
        slug: root.dataset.gameSlug,
        syncUrl: root.dataset.syncUrl,
        serverProgress: serverProgress,
        statusEl: document.getElementById("sync-status")
    });

    var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
        mode: "css",
        lineNumbers: true,
        theme: "default",
        extraKeys: {
            "Ctrl-Space": "autocomplete",
            "Cmd-Space": "autocomplete"
        },
        hintOptions: {
            hint: flexboxAwareHint,
            completeSingle: false
        }
    });

    var FLEX_PROPERTIES = [
        "align-content",
        "align-items",
        "align-self",
        "display",
        "flex",
        "flex-basis",
        "flex-direction",
        "flex-flow",
        "flex-grow",
        "flex-shrink",
        "flex-wrap",
        "gap",
        "column-gap",
        "row-gap",
        "justify-content",
        "justify-items",
        "justify-self",
        "order"
    ];

    var FLEX_VALUES = {
        "display": ["flex", "inline-flex", "block", "inline-block", "none"],
        "justify-content": [
            "flex-start",
            "flex-end",
            "center",
            "space-between",
            "space-around",
            "space-evenly",
            "start",
            "end"
        ],
        "align-items": [
            "flex-start",
            "flex-end",
            "center",
            "stretch",
            "baseline",
            "start",
            "end"
        ],
        "align-content": [
            "flex-start",
            "flex-end",
            "center",
            "stretch",
            "space-between",
            "space-around",
            "space-evenly"
        ],
        "flex-direction": ["row", "row-reverse", "column", "column-reverse"],
        "flex-wrap": ["nowrap", "wrap", "wrap-reverse"],
        "flex-flow": [
            "row nowrap",
            "row wrap",
            "column nowrap",
            "column wrap",
            "row-reverse wrap",
            "column-reverse wrap"
        ],
        "gap": ["8px", "12px", "16px", "18px", "24px", "32px"],
        "row-gap": ["8px", "12px", "16px", "24px"],
        "column-gap": ["8px", "12px", "16px", "24px"]
    };

    function getWordAround(cm) {
        var cursor = cm.getCursor();
        var line = cm.getLine(cursor.line) || "";
        var start = cursor.ch;
        var end = cursor.ch;

        while (start > 0 && /[a-zA-Z0-9-]/.test(line.charAt(start - 1))) {
            start -= 1;
        }
        while (end < line.length && /[a-zA-Z0-9-]/.test(line.charAt(end))) {
            end += 1;
        }

        return {
            from: CodeMirror.Pos(cursor.line, start),
            to: CodeMirror.Pos(cursor.line, end),
            text: line.slice(start, end),
            line: line,
            cursor: cursor
        };
    }

    function currentPropertyName(line, cursorCh) {
        var before = line.slice(0, cursorCh);
        var match = before.match(/([a-zA-Z-]+)\s*:\s*[^;]*$/);
        return match ? match[1].toLowerCase() : "";
    }

    function isTypingValue(line, cursorCh) {
        var before = line.slice(0, cursorCh);
        var colon = before.lastIndexOf(":");
        var semi = before.lastIndexOf(";");
        return colon > semi;
    }

    function uniqueHintList(items) {
        var seen = {};
        var result = [];
        var i;
        var key;
        for (i = 0; i < items.length; i++) {
            key = typeof items[i] === "string" ? items[i] : items[i].text;
            if (!seen[key]) {
                seen[key] = true;
                result.push(items[i]);
            }
        }
        return result;
    }

    function flexboxAwareHint(cm) {
        var word = getWordAround(cm);
        var token = word.text.toLowerCase();
        var list = [];
        var propertyName;
        var values;
        var cssHint;
        var i;
        var prop;

        if (isTypingValue(word.line, word.cursor.ch)) {
            propertyName = currentPropertyName(word.line, word.cursor.ch);
            values = FLEX_VALUES[propertyName] || [];
            for (i = 0; i < values.length; i++) {
                if (!token || values[i].toLowerCase().indexOf(token) === 0) {
                    list.push(values[i]);
                }
            }
        } else {
            for (i = 0; i < FLEX_PROPERTIES.length; i++) {
                prop = FLEX_PROPERTIES[i];
                if (!token || prop.indexOf(token) === 0) {
                    list.push({
                        text: prop + ": ",
                        displayText: prop
                    });
                }
            }
        }

        if (CodeMirror.hint && typeof CodeMirror.hint.css === "function") {
            cssHint = CodeMirror.hint.css(cm);
            if (cssHint && cssHint.list && cssHint.list.length) {
                list = list.concat(cssHint.list);
            }
        }

        list = uniqueHintList(list);

        return {
            list: list,
            from: word.from,
            to: word.to
        };
    }

    function maybeShowHints(cm, change) {
        var typed;
        if (!change || !change.text || !change.text[0]) {
            return;
        }
        typed = change.text[0];
        if (!/[a-zA-Z-]/.test(typed)) {
            return;
        }
        if (cm.state.completionActive) {
            return;
        }
        CodeMirror.commands.autocomplete(cm);
    }

    editor.on("inputRead", maybeShowHints);

    var saved = progressManager.getState();
    var currentLevel = Math.min(saved.currentLevel || 0, Math.max(levels.length - 1, 0));
    var hasFinishedGame = !!saved.isFinished;
    var failedAttempts = 0;
    var hintRevealed = false;
    var protectedMarks = [];

    var hintBtn = document.getElementById("hint-btn");
    var hintText = document.getElementById("hint-text");
    var enigmaText = document.getElementById("enigma-text");
    var sceneTag = document.getElementById("scene-tag");
    var stabilityValue = document.getElementById("stability-value");
    var stabilityFill = document.getElementById("stability-fill");
    var gameArea = document.querySelector(".game-area");

    function clearProtectedMarks() {
        var i;
        for (i = 0; i < protectedMarks.length; i++) {
            protectedMarks[i].clear();
        }
        protectedMarks = [];
    }

    function setupProtectedStarter(starterCode) {
        var code = starterCode || "";
        var closeIdx = code.lastIndexOf("}");
        var before;
        var after;
        var full;
        var editableLine;
        var lastLine;
        var doc;

        clearProtectedMarks();

        if (closeIdx === -1) {
            editor.setValue(code);
            return;
        }

        before = code.slice(0, closeIdx);
        after = code.slice(closeIdx);

        if (!before.endsWith("\n")) {
            before += "\n";
        }

        // Ligne éditable réservée à l'utilisateur, avant le "}" protégé.
        full = before + "  \n" + after;
        editor.setValue(full);

        editableLine = editor.lineCount() - 2;
        lastLine = editor.lineCount() - 1;
        doc = editor.getDoc();

        if (editableLine > 0) {
            protectedMarks.push(
                doc.markText(
                    { line: 0, ch: 0 },
                    { line: editableLine, ch: 0 },
                    {
                        readOnly: true,
                        atomic: false,
                        inclusiveLeft: true,
                        inclusiveRight: false,
                        className: "cm-protected"
                    }
                )
            );
        }

        protectedMarks.push(
            doc.markText(
                { line: lastLine, ch: 0 },
                { line: lastLine, ch: editor.getLine(lastLine).length },
                {
                    readOnly: true,
                    atomic: false,
                    inclusiveLeft: true,
                    inclusiveRight: true,
                    className: "cm-protected"
                }
            )
        );

        editor.setCursor({ line: editableLine, ch: 2 });
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
    }

    function resetHintState() {
        failedAttempts = 0;
        hintRevealed = false;
        if (hintText) {
            hintText.classList.add("is-hidden");
            hintText.innerHTML = "";
        }
        if (hintBtn) {
            hintBtn.disabled = false;
            hintBtn.textContent = "Révéler un indice";
        }
    }

    function revealHint(auto) {
        var level = levels[currentLevel];
        if (!level || !hintText || !hintBtn) {
            return;
        }
        hintRevealed = true;
        hintText.innerHTML = "<strong>Indice :</strong> " + (level.hint || "Observe les axes horizontal et vertical.");
        hintText.classList.remove("is-hidden");
        hintBtn.disabled = true;
        hintBtn.textContent = auto ? "Indice débloqué" : "Indice révélé";
    }

    function loadLevel(index) {
        var level = levels[index];
        var targetContainer = document.querySelector(".target-container");
        var itemsContainer = document.querySelector(".items-container");
        var feedback = document.querySelector(".level-feedback");
        var itemCount = level.itemCount || 1;

        currentLevel = index;
        resetHintState();
        gameArea.classList.remove("is-repaired");
        gameArea.classList.toggle("compact-squares", itemCount >= 4);
        renderSquares(itemCount);

        document.querySelector(".level-title").textContent = level.title;
        document.querySelector(".level-difficulty").textContent = level.difficulty;
        document.querySelector(".level-progress").textContent =
            (index + 1) + " / " + levels.length;

        if (sceneTag) {
            sceneTag.textContent = level.scene || "Zone inconnue";
        }
        if (enigmaText) {
            enigmaText.textContent = level.objective || "";
        }

        resetFlexStyles(targetContainer);
        resetFlexStyles(itemsContainer);
        applyFlexStyles(targetContainer, level.target || {});

        feedback.textContent = "";
        feedback.classList.remove("error", "success");
        document.querySelector(".validate-btn").textContent = hasFinishedGame
            ? "RELANCER LE PROTOCOLE"
            : "RÉSOUDRE L'ÉNIGME";

        setupProtectedStarter(level.starterCode || "");
        applyCSS();
        updateStability();

        progressManager.save({
            currentLevel: currentLevel,
            isFinished: hasFinishedGame
        });
    }

    function renderSquares(count) {
        var targetContainer = document.querySelector(".target-container");
        var itemsContainer = document.querySelector(".items-container");
        var targetHtml = "";
        var itemHtml = "";
        var i;

        for (i = 0; i < count; i++) {
            targetHtml += '<div class="target"><span class="ghost-label">?</span></div>';
            itemHtml += '<div class="item"><span class="shard-label">' + (i + 1) + "</span></div>";
        }

        targetContainer.innerHTML = targetHtml;
        itemsContainer.innerHTML = itemHtml;
    }

    function resetFlexStyles(element) {
        element.style.flexFlow = "";
        element.style.flexDirection = "";
        element.style.flexWrap = "";
        element.style.justifyContent = "";
        element.style.alignItems = "";
        element.style.alignContent = "";
        element.style.gap = "";
    }

    function applyFlexStyles(element, styles) {
        if (styles.flexFlow) {
            element.style.flexFlow = styles.flexFlow;
        } else {
            element.style.flexDirection = styles.flexDirection || "row";
            element.style.flexWrap = styles.flexWrap || "nowrap";
        }

        element.style.justifyContent = styles.justifyContent || "flex-start";
        element.style.alignItems = styles.alignItems || "stretch";
        element.style.alignContent = styles.alignContent || "stretch";
        element.style.gap = styles.gap || "12px";
    }

    function applyCSS() {
        document.getElementById("dynamic-styles").innerHTML = editor.getValue();
        window.setTimeout(checkWin, 50);
    }

    function checkWin() {
        var isCompleted = isLevelCompleted();
        var items = document.querySelectorAll(".item");
        var i;

        if (!items.length) {
            return false;
        }

        for (i = 0; i < items.length; i++) {
            if (isCompleted) {
                items[i].classList.add("success");
            } else {
                items[i].classList.remove("success");
            }
        }

        if (isCompleted) {
            gameArea.classList.add("is-repaired");
        } else {
            gameArea.classList.remove("is-repaired");
        }

        return isCompleted;
    }

    function isLevelCompleted() {
        var items = document.querySelectorAll(".item");
        var targets = document.querySelectorAll(".target");
        var i;

        if (!items.length || items.length !== targets.length) {
            return false;
        }

        for (i = 0; i < items.length; i++) {
            var itemRect = items[i].getBoundingClientRect();
            var targetRect = targets[i].getBoundingClientRect();

            if (
                Math.abs(itemRect.top - targetRect.top) >= 2 ||
                Math.abs(itemRect.left - targetRect.left) >= 2
            ) {
                return false;
            }
        }

        return true;
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

    function showVictoryModal() {
        var modal = document.getElementById("victory-modal");
        if (!modal) {
            return;
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
        var validateButton = document.querySelector(".validate-btn");

        applyCSS();

        window.setTimeout(function () {
            if (!isLevelCompleted()) {
                failedAttempts += 1;
                feedback.classList.remove("success");
                feedback.classList.add("error");

                if (failedAttempts >= 2 && !hintRevealed) {
                    revealHint(true);
                    feedback.textContent =
                        "Le fragment résiste… Un indice vient d'apparaître.";
                } else {
                    feedback.textContent =
                        "Pas encore. Le fragment n'a pas rejoint son ancre fantôme.";
                }
                checkWin();
                return;
            }

            feedback.classList.remove("error");
            feedback.classList.add("success");
            markLevelCompleted(currentLevel);
            gameArea.classList.add("is-repaired");

            if (currentLevel < levels.length - 1) {
                feedback.textContent = "Énigme résolue. Un panneau se rallume…";
                currentLevel += 1;
                progressManager.save({ currentLevel: currentLevel });

                window.setTimeout(function () {
                    loadLevel(currentLevel);
                }, 900);
            } else {
                hasFinishedGame = true;
                feedback.textContent =
                    "Protocole terminé. Nayekola est réveillé. Le site n'est plus fantôme.";
                validateButton.textContent = "RELANCER LE PROTOCOLE";
                progressManager.save({
                    currentLevel: currentLevel,
                    isFinished: true
                });
                updateStability();
                progressManager.syncNow();
                window.setTimeout(showVictoryModal, 450);
            }
        }, 80);
    }

    function restartGame() {
        hideVictoryModal();
        currentLevel = 0;
        hasFinishedGame = false;

        if (typeof progressManager.reset === "function") {
            progressManager.reset();
        } else {
            progressManager.save({
                currentLevel: 0,
                completedLevels: [],
                isFinished: false
            });
        }

        // Force le serveur à oublier l'ancien état "terminé", puis recharge.
        progressManager.syncNow({ reset: true }, function () {
            window.location.reload();
        });
    }

    function handleValidateClick() {
        if (hasFinishedGame) {
            showVictoryModal();
            return;
        }
        validateLevel();
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

    editor.on("change", applyCSS);
    document.querySelector(".validate-btn").addEventListener("click", handleValidateClick);
    loadLevel(currentLevel);

    if (hasFinishedGame) {
        window.setTimeout(showVictoryModal, 300);
    }
})();
