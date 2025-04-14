function toggleDetails(project_name) {
  var detailsContainer = document.getElementById(project_name);
  detailsContainer.classList.toggle("open");
}

document.addEventListener("DOMContentLoaded", function () {
  const allMainDetails = document.querySelectorAll(
    "details:not(details details)",
  ); // selection of main details
  const allNestedDetails = document.querySelectorAll("details details"); // selection of nested details

  // Managing main details: close others and nested details when a main detail is open
  allMainDetails.forEach((targetDetail) => {
    targetDetail.addEventListener("toggle", () => {
      if (targetDetail.open) {
        // Close other main details
        allMainDetails.forEach((detail) => {
          if (detail !== targetDetail && detail.open) {
            detail.removeAttribute("open");
          }
        });

        // Do not close nested details in the same group
        const nestedInThisDetail = targetDetail.querySelectorAll("details");
        nestedInThisDetail.forEach((nestedDetail) => {
          nestedDetail.setAttribute("open", "true"); // Leave nested groups open
        });
      }
    });
  });

  // Close all nested <details> on startup
  allNestedDetails.forEach((detail) => {
    detail.removeAttribute("open");
    detail.open = false; // <-- Forcer fermeture
  });

  // Add a listener to manage single opening behavior
  allNestedDetails.forEach((targetDetail) => {
    targetDetail.addEventListener("toggle", (e) => {
      if (!targetDetail.open) {
        // Find the parent containing this detail
        const parentDetail =
          targetDetail.closest("details")?.parentElement || document;

        // Find other <details> open at the same level
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
