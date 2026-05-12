
var editor = CodeMirror.fromTextArea(document.getElementById("code"), {
    mode: "css",
    lineNumbers: true,
    theme: "default"
});

var currentLevel = 0;
var hasFinishedGame = false;

function loadLevel(index) {
    var level = levels[index];
    var gameArea = document.querySelector(".game-area");
    var targetContainer = document.querySelector(".target-container");
    var itemsContainer = document.querySelector(".items-container");
    var feedback = document.querySelector(".level-feedback");
    var itemCount = level.itemCount || 1;

    gameArea.classList.toggle("compact-squares", itemCount >= 4);
    renderSquares(itemCount);

    document.querySelector(".level-title").textContent = level.title;
    document.querySelector(".level-difficulty").textContent = level.difficulty;
    document.querySelector(".level-progress").textContent = (index + 1) + " / " + levels.length;
    document.querySelector(".level-explication p").innerHTML = "<strong>Objectif :</strong> " + level.objective;

    resetFlexStyles(targetContainer);
    resetFlexStyles(itemsContainer);
    applyFlexStyles(targetContainer, level.target);

    feedback.textContent = "";
    feedback.classList.remove("error");
    document.querySelector(".validate-btn").textContent = "VALIDATE";

    editor.setValue(level.starterCode);
    applyCSS();
}

function renderSquares(count) {
    var targetContainer = document.querySelector(".target-container");
    var itemsContainer = document.querySelector(".items-container");
    var targetHtml = "";
    var itemHtml = "";
    var i;

    for (i = 0; i < count; i++) {
        targetHtml += "<div class=\"target\"></div>";
        itemHtml += "<div class=\"item\"></div>";
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
    var css = editor.getValue();
    document.getElementById("dynamic-styles").innerHTML = css;

    setTimeout(checkWin, 50);
}

function checkWin() {
    var isCompleted = isLevelCompleted();
    var items = document.querySelectorAll(".item");
    var i;

    if (!items.length) return false;

    for (i = 0; i < items.length; i++) {
        if (isCompleted) {
            items[i].classList.add("success");
        } else {
            items[i].classList.remove("success");
        }
    }

    return isCompleted;
}

function isLevelCompleted() {
    var items = document.querySelectorAll(".item");
    var targets = document.querySelectorAll(".target");
    var i;

    if (!items.length || items.length !== targets.length) return false;

    for (i = 0; i < items.length; i++) {
        var itemRect = items[i].getBoundingClientRect();
        var targetRect = targets[i].getBoundingClientRect();

        if (Math.abs(itemRect.top - targetRect.top) >= 2 || Math.abs(itemRect.left - targetRect.left) >= 2) {
            return false;
        }
    }

    return true;
}

function validateLevel() {
    var feedback = document.querySelector(".level-feedback");
    var validateButton = document.querySelector(".validate-btn");

    applyCSS();

    setTimeout(function () {
        if (!isLevelCompleted()) {
            feedback.textContent = "Pas encore. Ajustez le code pour superposer chaque carre a sa cible.";
            feedback.classList.add("error");
            checkWin();
            return;
        }

        feedback.classList.remove("error");

        if (currentLevel < levels.length - 1) {
            feedback.textContent = "Reussi. Passage au niveau suivant...";
            currentLevel++;

            setTimeout(function () {
                loadLevel(currentLevel);
            }, 700);
        } else {
            hasFinishedGame = true;
            feedback.textContent = "Bravo, tous les niveaux sont termines.";
            validateButton.textContent = "RECOMMENCER";
        }
    }, 80);
}

function restartGame() {
    currentLevel = 0;
    hasFinishedGame = false;
    loadLevel(currentLevel);
}

function handleValidateClick() {
    if (hasFinishedGame) {
        restartGame();
        return;
    }

    validateLevel();
}

editor.on("change", applyCSS);
document.querySelector(".validate-btn").addEventListener("click", handleValidateClick);
loadLevel(currentLevel);
