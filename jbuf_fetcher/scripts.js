function toggleDetails(project_name) {
    var detailsContainer = document.getElementById(project_name);
    detailsContainer.classList.toggle('open');
}

document.addEventListener("DOMContentLoaded", function() {
    const allMainDetails = document.querySelectorAll("details:not(details details)");  // selection des details principaux
    const allNestedDetails = document.querySelectorAll("details details");  // selection des details imbriqués

    
    // Gestion des details principaux : fermer les autres et les imbriqués quand un principal est ouvert
    allMainDetails.forEach((targetDetail) => {
        targetDetail.addEventListener("toggle", () => {
            if (targetDetail.open) {
                // Fermer les autres détails principaux
                allMainDetails.forEach((detail) => {
                    if (detail !== targetDetail && detail.open) {
                        detail.removeAttribute("open");
                    }
                });

                // Ne pas fermer les détails imbriqués dans le même groupe
                const nestedInThisDetail = targetDetail.querySelectorAll("details");
                nestedInThisDetail.forEach((nestedDetail) => {
                    nestedDetail.setAttribute("open", "true");  // Laisser ouverts les imbriqués du même groupe
                });
            }
        });
    });

    // Étape 1 : Fermer tous les <details> imbriqués au démarrage
    allNestedDetails.forEach((detail) => {
        detail.removeAttribute("open");
        detail.open = false; // <-- Forcer fermeture
    });

    // Étape 2 : Ajouter l'écouteur pour gérer le comportement d'ouverture unique
    allNestedDetails.forEach((targetDetail) => {
        targetDetail.addEventListener("toggle", (e) => {
            if (!targetDetail.open) {
                // Trouver le parent contenant ce détail
                const parentDetail = targetDetail.closest("details")?.parentElement || document;

                // Trouver les autres <details> ouverts au même niveau
                const siblingDetails = parentDetail.querySelectorAll("details");

                siblingDetails.forEach((sibling) => {
                    if (sibling !== targetDetail && sibling.open) {
                        sibling.removeAttribute("open");
                    }
                });
            }
        });
    });
});