(function () {
    "use strict";

    var header = document.querySelector(".main-site-header");
    var toggle = document.querySelector(".nav-toggle");
    var nav = document.getElementById("site-nav");

    if (!header || !toggle || !nav) {
        return;
    }

    function setOpen(isOpen) {
        header.classList.toggle("is-nav-open", isOpen);
        toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
        toggle.setAttribute("aria-label", isOpen ? "Fermer le menu" : "Ouvrir le menu");
    }

    toggle.addEventListener("click", function () {
        setOpen(!header.classList.contains("is-nav-open"));
    });

    nav.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
            setOpen(false);
        });
    });

    window.addEventListener("resize", function () {
        if (window.innerWidth > 800) {
            setOpen(false);
        }
    });
})();
