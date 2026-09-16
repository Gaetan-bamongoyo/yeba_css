(function () {
    "use strict";

    var root = document.getElementById("game-root");
    if (!root) {
        return;
    }

    var levels = JSON.parse(document.getElementById("game-levels").textContent);
    var serverProgress = JSON.parse(document.getElementById("game-progress").textContent);
    var siteHtml = JSON.parse(document.getElementById("technova-site-html").textContent);
    var referenceCssEl = document.getElementById("technova-reference-css");
    var referenceCss = referenceCssEl ? JSON.parse(referenceCssEl.textContent) : "";
    var progressSlug =
        root.getAttribute("data-progress-slug") ||
        root.dataset.progressSlug ||
        root.getAttribute("data-game-slug") ||
        root.dataset.gameSlug ||
        "css-technova";
    var cssStorageKey = "nayekola:css-code:" + progressSlug;
    try {
        var progressKey = "nayekola:progress:" + progressSlug;
        if (!window.localStorage.getItem(progressKey)) {
            var legacyProgress = window.localStorage.getItem("nayekola:progress:css-technova");
            if (legacyProgress) {
                window.localStorage.setItem(progressKey, legacyProgress);
            }
        }
        if (!window.localStorage.getItem(cssStorageKey)) {
            var legacyCss = window.localStorage.getItem("nayekola:css-code:css-technova");
            if (legacyCss) {
                window.localStorage.setItem(cssStorageKey, legacyCss);
            }
        }
    } catch (error) {
        /* ignore */
    }

    var progressManager = window.NayekolaProgress.createProgressManager({
        slug: progressSlug,
        syncUrl: root.getAttribute("data-sync-url") || root.dataset.syncUrl || "",
        serverProgress: serverProgress,
        statusEl: document.getElementById("sync-status"),
        aliasSlugs: ["css-technova"]
    });

    function prettySiteHtml(html) {
        return String(html || "")
            .replace(/src="data:image\/[^"]+"/g, 'src="…"')
            .replace(/^\s+|\s+$/g, "");
    }

    function extractSelectors(html) {
        var classes = {};
        var ids = {};
        var tags = {};
        var classMatch;
        var idMatch;
        var tagMatch;
        var parts;
        var i;
        var classRe = /class\s*=\s*["']([^"']+)["']/gi;
        var idRe = /id\s*=\s*["']([^"']+)["']/gi;
        var tagRe = /<\/?([a-zA-Z][a-zA-Z0-9]*)\b/g;
        var baseTags = [
            "html",
            "body",
            "header",
            "nav",
            "main",
            "section",
            "article",
            "footer",
            "div",
            "a",
            "img",
            "h1",
            "h2",
            "h3",
            "p",
            "form",
            "label",
            "input",
            "textarea",
            "button",
            "strong",
            "span"
        ];

        while ((classMatch = classRe.exec(html))) {
            parts = classMatch[1].split(/\s+/);
            for (i = 0; i < parts.length; i++) {
                if (parts[i]) {
                    classes["." + parts[i]] = true;
                }
            }
        }
        while ((idMatch = idRe.exec(html))) {
            if (idMatch[1]) {
                ids["#" + idMatch[1]] = true;
            }
        }
        while ((tagMatch = tagRe.exec(html))) {
            if (tagMatch[1] && tagMatch[1].toLowerCase() !== "svg") {
                tags[tagMatch[1].toLowerCase()] = true;
            }
        }
        for (i = 0; i < baseTags.length; i++) {
            tags[baseTags[i]] = true;
        }

        return {
            classes: Object.keys(classes).sort(),
            ids: Object.keys(ids).sort(),
            tags: Object.keys(tags).sort(),
            all: Object.keys(classes)
                .concat(Object.keys(ids), Object.keys(tags), ["*", ":hover", ":focus", "@media"])
                .sort()
        };
    }

    var siteSelectors = extractSelectors(siteHtml);
    var htmlView = document.getElementById("technova-html-view");
    if (htmlView) {
        htmlView.textContent = prettySiteHtml(siteHtml);
    }

    function uniqueHintList(items) {
        var seen = {};
        var result = [];
        var i;
        var key;
        var item;
        for (i = 0; i < items.length; i++) {
            item = items[i];
            key = typeof item === "string" ? item : item.text || item.displayText || "";
            if (!key || seen[key]) {
                continue;
            }
            seen[key] = true;
            result.push(item);
        }
        return result;
    }

    function getWordAround(cm) {
        var cursor = cm.getCursor();
        var line = cm.getLine(cursor.line) || "";
        var start = cursor.ch;
        var end = cursor.ch;
        while (start && /[a-zA-Z0-9_@#.:*-]/.test(line.charAt(start - 1))) {
            start -= 1;
        }
        while (end < line.length && /[a-zA-Z0-9_@#.:*-]/.test(line.charAt(end))) {
            end += 1;
        }
        return {
            text: line.slice(start, end),
            line: line,
            cursor: cursor,
            from: CodeMirror.Pos(cursor.line, start),
            to: CodeMirror.Pos(cursor.line, end)
        };
    }

    function isTypingValue(line, ch) {
        var before = line.slice(0, ch);
        var colon = before.lastIndexOf(":");
        var brace = before.lastIndexOf("{");
        var semi = before.lastIndexOf(";");
        return colon > brace && colon > semi;
    }

    function isTypingSelector(line, ch) {
        var before = line.slice(0, ch);
        var open = before.lastIndexOf("{");
        var close = before.lastIndexOf("}");
        if (open > close) {
            return false;
        }
        return !isTypingValue(line, ch);
    }

    function technovaAwareHint(cm) {
        var word = getWordAround(cm);
        var token = word.text.toLowerCase();
        var list = [];
        var cssHint;
        var i;
        var item;
        var pool;

        if (isTypingSelector(word.line, word.cursor.ch)) {
            if (token.indexOf(".") === 0) {
                pool = siteSelectors.classes;
            } else if (token.indexOf("#") === 0) {
                pool = siteSelectors.ids;
            } else {
                pool = siteSelectors.all;
            }
            for (i = 0; i < pool.length; i++) {
                item = pool[i];
                if (!token || item.toLowerCase().indexOf(token) === 0) {
                    list.push({
                        text: item,
                        displayText: item
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
        if (!/[a-zA-Z0-9_@#.:-]/.test(typed)) {
            return;
        }
        if (cm.state.completionActive) {
            return;
        }
        CodeMirror.commands.autocomplete(cm);
    }

    var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
        mode: "css",
        lineNumbers: true,
        theme: "default",
        extraKeys: {
            "Ctrl-Space": "autocomplete",
            "Cmd-Space": "autocomplete"
        },
        hintOptions: {
            hint: technovaAwareHint,
            completeSingle: false
        }
    });

    editor.on("inputRead", maybeShowHints);

    var saved = progressManager.getState();
    var currentLevel = Math.min(saved.currentLevel || 0, Math.max(levels.length - 1, 0));
    var hasFinishedGame = !!saved.isFinished;
    var failedAttempts = 0;
    var hintLevel = 0;
    var hintRevealed = false;

    var previewFrame = document.getElementById("technova-preview");
    var previewModal = document.getElementById("preview-modal");
    var previewModeLabel = document.getElementById("preview-mode-label");
    var previewModalTitle = document.getElementById("preview-modal-title");
    var hintBtn = document.getElementById("hint-btn");
    var hintText = document.getElementById("hint-text");
    var enigmaText = document.getElementById("enigma-text");
    var sceneTag = document.getElementById("scene-tag");
    var stabilityValue = document.getElementById("stability-value");
    var stabilityFill = document.getElementById("stability-fill");
    var feedbackEl = document.querySelector(".level-feedback");
    var validateBtn = document.getElementById("check-btn");
    var runPreviewBtn = document.getElementById("run-preview-btn");
    var viewportBtns = document.querySelectorAll("[data-preview-width]");
    var previewMode = "student";

    function readSavedCss() {
        try {
            return window.localStorage.getItem(cssStorageKey) || "";
        } catch (error) {
            return "";
        }
    }

    function writeSavedCss(css) {
        try {
            window.localStorage.setItem(cssStorageKey, css);
        } catch (error) {
            /* ignore */
        }
    }

    function clearSavedCss() {
        try {
            window.localStorage.removeItem(cssStorageKey);
        } catch (error) {
            /* ignore */
        }
    }

    function previewDoc() {
        return previewFrame && previewFrame.contentDocument
            ? previewFrame.contentDocument
            : null;
    }

    var brokenBaseCss =
        "/* état initial : site cassé */" +
        "img{display:block;}" +
        ".hero-image,.about-image{width:1100px;max-width:none;}" +
        ".nav a{display:list-item;margin-left:1.25rem;}";

    function renderPreview(onReady, options) {
        var opts = options || {};
        var css =
            opts.mode === "mockup" && referenceCss
                ? referenceCss
                : editor.getValue();
        if (opts.mode !== "mockup") {
            writeSavedCss(editor.getValue());
        }
        var html =
            "<!DOCTYPE html><html lang=\"fr\"><head><meta charset=\"UTF-8\">" +
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">" +
            (opts.mode === "mockup" ? "" : "<style>" + brokenBaseCss + "</style>") +
            "<style>" + css + "</style></head><body>" + siteHtml + "</body></html>";
        if (typeof onReady === "function") {
            previewFrame.onload = function () {
                previewFrame.onload = null;
                onReady();
            };
        }
        previewFrame.srcdoc = html;
    }

    function openPreviewModal(mode) {
        previewMode = mode || "student";
        if (previewModeLabel) {
            previewModeLabel.textContent =
                previewMode === "mockup" ? "Maquette client" : "Ton rendu";
        }
        if (previewModalTitle) {
            previewModalTitle.textContent =
                previewMode === "mockup"
                    ? "Référence visuelle (sans code solution)"
                    : "Aperçu du site";
        }
        if (previewModal) {
            previewModal.hidden = false;
            previewModal.classList.remove("is-hidden");
            document.body.classList.add("preview-open");
        }
        renderPreview(null, { mode: previewMode });
    }

    function hidePreviewModal() {
        if (!previewModal) {
            return;
        }
        previewModal.hidden = true;
        previewModal.classList.add("is-hidden");
        document.body.classList.remove("preview-open");
    }

    var htmlModal = document.getElementById("html-modal");

    function openHtmlModal() {
        if (!htmlModal) {
            return;
        }
        htmlModal.hidden = false;
        htmlModal.classList.remove("is-hidden");
        document.body.classList.add("preview-open");
    }

    function hideHtmlModal() {
        if (!htmlModal) {
            return;
        }
        htmlModal.hidden = true;
        htmlModal.classList.add("is-hidden");
        if (!previewModal || previewModal.hidden) {
            document.body.classList.remove("preview-open");
        }
    }

    function parseRgb(value) {
        var match = String(value || "").match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/i);
        if (!match) {
            return null;
        }
        return [Number(match[1]), Number(match[2]), Number(match[3])];
    }

    function rgbClose(a, b, tol) {
        var t = tol == null ? 8 : tol;
        return (
            Math.abs(a[0] - b[0]) <= t &&
            Math.abs(a[1] - b[1]) <= t &&
            Math.abs(a[2] - b[2]) <= t
        );
    }

    function computed(doc, selector, prop) {
        var el = doc.querySelector(selector);
        if (!el) {
            return null;
        }
        return doc.defaultView.getComputedStyle(el).getPropertyValue(prop);
    }

    function runCheck(doc, cssSource, check) {
        var display;
        var a;
        var b;
        var cards;
        var i;
        var ra;
        var rb;
        var pad;
        var radius;
        var shadow;
        var imgs;
        var maxW;
        var box;
        var font;

        if (check.type === "computed") {
            a = parseRgb(computed(doc, check.selector, check.prop));
            return !!(a && rgbClose(a, check.rgb));
        }
        if (check.type === "font_sans") {
            font = (computed(doc, check.selector, "font-family") || "").toLowerCase();
            return /arial|helvetica|sans-serif|system-ui|segoe/.test(font);
        }
        if (check.type === "box_border_box") {
            box = computed(doc, "body", "box-sizing") || "";
            if (box.indexOf("border-box") !== -1) {
                return true;
            }
            box = computed(doc, "html", "box-sizing") || "";
            return box.indexOf("border-box") !== -1 || /box-sizing\s*:\s*border-box/i.test(cssSource);
        }
        if (check.type === "display_flex") {
            display = (computed(doc, check.selector, "display") || "").trim();
            return display === "flex" || display === "inline-flex";
        }
        if (check.type === "display_flex_or_grid") {
            display = (computed(doc, check.selector, "display") || "").trim();
            return (
                display === "flex" ||
                display === "inline-flex" ||
                display === "grid" ||
                display === "inline-grid"
            );
        }
        if (check.type === "row_layout" || check.type === "side_by_side") {
            a = doc.querySelector(check.child_a);
            b = doc.querySelector(check.child_b);
            if (!a || !b) {
                return false;
            }
            ra = a.getBoundingClientRect();
            rb = b.getBoundingClientRect();
            return rb.left > ra.left + 20 && Math.abs(ra.top - rb.top) < 80;
        }
        if (check.type === "min_padding") {
            a = doc.querySelector(check.selector);
            if (!a) {
                return false;
            }
            pad = doc.defaultView.getComputedStyle(a);
            return (
                parseFloat(pad.paddingTop) >= check.min ||
                parseFloat(pad.paddingBottom) >= check.min ||
                parseFloat(pad.paddingLeft) >= check.min
            );
        }
        if (check.type === "min_radius") {
            a = doc.querySelector(check.selector);
            if (!a) {
                return false;
            }
            radius = parseFloat(doc.defaultView.getComputedStyle(a).borderTopLeftRadius) || 0;
            return radius >= check.min;
        }
        if (check.type === "has_shadow") {
            a = doc.querySelector(check.selector);
            if (!a) {
                return false;
            }
            shadow = doc.defaultView.getComputedStyle(a).boxShadow || "";
            return shadow && shadow !== "none";
        }
        if (check.type === "cards_row") {
            cards = doc.querySelectorAll((check.selector || "") + " " + check.card);
            if (!cards.length) {
                cards = doc.querySelectorAll(check.card);
            }
            if (cards.length < (check.count || 3)) {
                return false;
            }
            ra = cards[0].getBoundingClientRect();
            rb = cards[1].getBoundingClientRect();
            return rb.left > ra.left + 10 && Math.abs(ra.top - rb.top) < 40;
        }
        if (check.type === "img_contained") {
            imgs = doc.querySelectorAll(check.selector || "img");
            if (!imgs.length) {
                return false;
            }
            if (/max-width\s*:\s*100%/i.test(cssSource) || /img\s*\{[^}]*max-width/i.test(cssSource)) {
                return true;
            }
            for (i = 0; i < imgs.length; i++) {
                maxW = doc.defaultView.getComputedStyle(imgs[i]).maxWidth || "";
                if (maxW === "100%" || parseFloat(maxW) >= 90) {
                    continue;
                }
                if (imgs[i].clientWidth > (imgs[i].parentElement ? imgs[i].parentElement.clientWidth + 4 : 9999)) {
                    return false;
                }
                return false;
            }
            return true;
        }
        if (check.type === "css_source") {
            return new RegExp(check.pattern, "i").test(cssSource);
        }
        if (check.type === "mobile_stack") {
            return checkMobileStack(cssSource, check.width || 390);
        }
        return false;
    }

    function checkMobileStack(cssSource, width) {
        var iframe = document.createElement("iframe");
        var ok = false;
        var doc;
        var hero;
        var grid;
        var a;
        var b;
        iframe.style.cssText = "position:absolute;left:-9999px;top:0;width:" + width + "px;height:800px;border:0;";
        document.body.appendChild(iframe);
        iframe.srcdoc =
            "<!DOCTYPE html><html><head><meta charset='UTF-8'>" +
            "<meta name='viewport' content='width=device-width, initial-scale=1'>" +
            "<style>" + cssSource + "</style></head><body>" + siteHtml + "</body></html>";
        // Synchronous-ish wait is not possible; validation will call after load.
        // For sync checks we use a temporary approach with contentDocument after brief wait in validateLevel.
        iframe.setAttribute("data-mobile-check", "1");
        // Fallback source check if async not ready: require column in media
        ok = /@media[\s\S]*flex-direction\s*:\s*column/i.test(cssSource);
        document.body.removeChild(iframe);
        if (ok) {
            return true;
        }
        // Secondary: stacked selectors in media
        return /@media[\s\S]*(hero|services-grid|about|contact-layout)[\s\S]*flex-direction\s*:\s*column/i.test(
            cssSource
        );
    }

    function validateLevelChecks(checks) {
        var doc = previewDoc();
        var cssSource = editor.getValue();
        var i;
        var failed = [];
        if (!doc || !doc.body) {
            return { ok: false, failed: ["La prévisualisation n'est pas prête. Réessaie."] };
        }
        for (i = 0; i < checks.length; i++) {
            if (!runCheck(doc, cssSource, checks[i])) {
                failed.push(describeCheck(checks[i]));
            }
        }
        return { ok: failed.length === 0, failed: failed };
    }

    function describeCheck(check) {
        if (check.type === "computed" && check.selector === "body" && check.prop === "background-color") {
            return "Le fond général de la page n'utilise pas encore la couleur claire de la charte.";
        }
        if (check.type === "computed" && check.selector === "body" && check.prop === "color") {
            return "La couleur du texte principal n'est pas encore conforme à la charte.";
        }
        if (check.type === "font_sans") {
            return "La police générale n'est pas encore une sans-serif lisible.";
        }
        if (check.type === "box_border_box") {
            return "Le modèle de boîte border-box n'est pas encore en place.";
        }
        if (check.type === "display_flex" && check.selector === ".header-inner") {
            return "Le header n'organise pas encore logo et menu sur une ligne flexible.";
        }
        if (check.type === "row_layout" || check.type === "side_by_side") {
            return "Les blocs ne sont pas encore correctement placés côte à côte.";
        }
        if (check.type === "cards_row") {
            return "Les cartes services ne sont pas encore alignées sur une même ligne.";
        }
        if (check.type === "has_shadow" || check.type === "min_radius") {
            return "Les cartes n'ont pas encore l'aspect « carte » attendu (coins / ombre).";
        }
        if (check.type === "min_padding") {
            return "Il manque encore de l'espace intérieur sur certaines sections.";
        }
        if (check.type === "css_source" && check.pattern === ":hover") {
            return "Aucune réaction au survol (:hover) n'a été détectée.";
        }
        if (check.type === "css_source" && check.pattern === "transition") {
            return "Ajoute une transition pour rendre l'interaction plus fluide.";
        }
        if (check.type === "css_source" && check.pattern === "@media") {
            return "Aucune media query n'a encore été trouvée pour le mobile.";
        }
        if (check.type === "img_contained") {
            return "Les images ne sont pas encore contraintes à leur conteneur.";
        }
        if (check.type === "mobile_stack") {
            return "Sur mobile, Hero/cartes ne passent pas encore en disposition verticale.";
        }
        if (check.type === "computed" && check.selector === ".btn-primary") {
            return "Le bouton principal n'utilise pas encore la couleur de marque.";
        }
        if (check.type === "computed" && (check.selector === ".site-header" || check.selector === ".site-footer")) {
            return "Header ou footer n'ont pas encore le fond sombre de la marque.";
        }
        return "Un critère de la mission n'est pas encore rempli.";
    }

    function updateStability() {
        var state = progressManager.getState();
        var completed = (state.completedLevels || []).length;
        var percent = Math.round((completed / Math.max(levels.length, 1)) * 100);
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
        hintLevel = 0;
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

    function getHints(level) {
        var fromTarget = level.target && level.target.hints;
        if (fromTarget && fromTarget.length) {
            return fromTarget;
        }
        if (level.hints && level.hints.length) {
            return level.hints;
        }
        if (level.hint) {
            return [level.hint];
        }
        return ["Observe la prévisualisation et affine ton CSS."];
    }

    function revealHint(auto) {
        var level = levels[currentLevel];
        var hints = getHints(level);
        if (!hintText || !hintBtn) {
            return;
        }
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
        hintBtn.textContent =
            hintLevel >= hints.length - 1
                ? auto
                    ? "Indice débloqué"
                    : "Indice révélé"
                : "Indice suivant";
        hintLevel += 1;
    }

    function loadLevel(index) {
        var level = levels[index];
        currentLevel = index;
        resetHintState();

        document.querySelector(".level-title").textContent = level.title;
        document.querySelector(".level-difficulty").textContent = level.difficulty;
        document.querySelector(".level-progress").textContent =
            index + 1 + " / " + levels.length;
        if (sceneTag) {
            sceneTag.textContent = level.scene || "Mission";
        }
        if (enigmaText) {
            enigmaText.textContent = level.objective || "";
        }
        if (feedbackEl) {
            feedbackEl.textContent = "";
            feedbackEl.classList.remove("error", "success");
        }
        if (validateBtn) {
            validateBtn.textContent = hasFinishedGame ? "VOIR LA FIN" : "VALIDER LA MISSION";
        }

        // CSS cumulatif : on ne réinitialise pas l'éditeur entre missions.
        if (!editor.getValue().trim()) {
            var savedCss = readSavedCss();
            if (savedCss) {
                editor.setValue(savedCss);
            } else if (level.starterCode) {
                editor.setValue(level.starterCode);
            } else if (levels[0] && levels[0].starterCode) {
                editor.setValue(levels[0].starterCode);
            }
        }

        writeSavedCss(editor.getValue());
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
        var level = levels[currentLevel];
        var checks = ((level.target || {}).validation) || [];
        var result;

        renderPreview(function () {
            window.setTimeout(function () {
                result = validateLevelChecks(checks);
                if (!result.ok) {
                    failedAttempts += 1;
                    if (feedbackEl) {
                        feedbackEl.classList.add("error");
                        feedbackEl.classList.remove("success");
                        feedbackEl.textContent = result.failed[0] || "Ce n'est pas encore bon.";
                    }
                    if (failedAttempts >= 2 && !hintRevealed) {
                        revealHint(true);
                    }
                    return;
                }

                if (feedbackEl) {
                    feedbackEl.classList.remove("error");
                    feedbackEl.classList.add("success");
                }
                markLevelCompleted(currentLevel);
                writeSavedCss(editor.getValue());

                if (currentLevel < levels.length - 1) {
                    if (feedbackEl) {
                        feedbackEl.textContent = "Mission validée. Le site s'améliore…";
                    }
                    currentLevel += 1;
                    progressManager.save({ currentLevel: currentLevel });
                    window.setTimeout(function () {
                        loadLevel(currentLevel);
                    }, 700);
                } else {
                    hasFinishedGame = true;
                    if (feedbackEl) {
                        feedbackEl.textContent = "Site TechNova restauré. Présentation prête !";
                    }
                    if (validateBtn) {
                        validateBtn.textContent = "VOIR LA FIN";
                    }
                    progressManager.save({
                        currentLevel: currentLevel,
                        isFinished: true
                    });
                    updateStability();
                    progressManager.syncNow && progressManager.syncNow();
                    window.setTimeout(showVictoryModal, 400);
                }
            }, 40);
        });
    }

    function restartGame() {
        hideVictoryModal();
        clearSavedCss();
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
        editor.setValue((levels[0] && levels[0].starterCode) || "/* TechNova */\n\n");
        if (progressManager.syncNow) {
            progressManager.syncNow({ reset: true }, function () {
                window.location.reload();
            });
        } else {
            window.location.reload();
        }
    }

    function handleCheck() {
        if (hasFinishedGame) {
            showVictoryModal();
            return;
        }
        validateLevel();
    }

    function setPreviewWidth(width) {
        if (!previewFrame) {
            return;
        }
        if (width === "100%" || width === "desktop") {
            previewFrame.style.width = "100%";
        } else {
            previewFrame.style.width = width + "px";
        }
        viewportBtns.forEach(function (btn) {
            btn.classList.toggle(
                "is-active",
                btn.getAttribute("data-preview-width") === String(width)
            );
        });
    }

    editor.on("change", function () {
        writeSavedCss(editor.getValue());
    });

    if (hintBtn) {
        hintBtn.addEventListener("click", function () {
            revealHint(false);
        });
    }
    if (runPreviewBtn) {
        runPreviewBtn.addEventListener("click", function () {
            openPreviewModal("student");
        });
    }
    if (validateBtn) {
        validateBtn.addEventListener("click", handleCheck);
    }
    var victoryRestart = document.getElementById("victory-restart");
    if (victoryRestart) {
        victoryRestart.addEventListener("click", restartGame);
    }
    document.querySelectorAll("[data-victory-close]").forEach(function (el) {
        el.addEventListener("click", hideVictoryModal);
    });
    document.querySelectorAll("[data-preview-close]").forEach(function (el) {
        el.addEventListener("click", hidePreviewModal);
    });
    document.querySelectorAll("[data-html-close]").forEach(function (el) {
        el.addEventListener("click", hideHtmlModal);
    });
    viewportBtns.forEach(function (btn) {
        btn.addEventListener("click", function () {
            setPreviewWidth(btn.getAttribute("data-preview-width"));
        });
    });

    var mockupBtn = document.getElementById("mockup-btn");
    if (mockupBtn) {
        mockupBtn.addEventListener("click", function () {
            openPreviewModal("mockup");
        });
    }

    var htmlStructureBtn = document.getElementById("html-structure-btn");
    if (htmlStructureBtn) {
        htmlStructureBtn.addEventListener("click", openHtmlModal);
    }

    document.addEventListener("keydown", function (event) {
        if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
            event.preventDefault();
            openPreviewModal("student");
            return;
        }
        if (event.key === "Escape") {
            if (previewModal && !previewModal.hidden) {
                hidePreviewModal();
            } else if (htmlModal && !htmlModal.hidden) {
                hideHtmlModal();
            }
        }
    });

    // Bootstrap CSS cumulatif
    (function initEditor() {
        var savedCss = readSavedCss();
        if (savedCss) {
            editor.setValue(savedCss);
        } else if (levels[0] && levels[0].starterCode) {
            editor.setValue(levels[0].starterCode);
        }
    })();

    setPreviewWidth("100%");
    loadLevel(currentLevel);
    if (hasFinishedGame) {
        window.setTimeout(showVictoryModal, 300);
    }
})();
