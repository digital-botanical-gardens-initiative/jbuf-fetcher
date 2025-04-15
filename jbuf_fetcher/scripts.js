function toggleDetails(project_name) {
  var detailsContainer = document.getElementById(project_name);

  // toggle visibility
  const isNowOpen = detailsContainer.classList.toggle("open");

  if (!isNowOpen) {
    // If we close the block, all <details> get closed
    const nestedDetails = detailsContainer.querySelectorAll("details");
    nestedDetails.forEach((d) => {
      d.removeAttribute("open");
    });
  }
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
      } else {
        // if MainDetail is closed, close all nested details
        const nestedDetails = targetDetail.querySelectorAll("details");
        nestedDetails.forEach((nestedDetail) => {
          nestedDetail.removeAttribute("open");
          nestedDetail.open = false;
        });
      }
    });
  });
  // Close all nested <details> on startup
  allNestedDetails.forEach((detail) => {
    detail.removeAttribute("open");
    detail.open = false;
  });

  // Add a listener to manage single opening behavior
  allNestedDetails.forEach((targetDetail) => {
    targetDetail.addEventListener("toggle", () => {
      if (targetDetail.open) {
        // find the common parent
        const parent = targetDetail.parentElement;

        if (!parent) return;

        // Close other nested details in the same parent
        const siblingDetails = parent.querySelectorAll("details");

        siblingDetails.forEach((sibling) => {
          if (sibling !== targetDetail && sibling.open) {
            sibling.removeAttribute("open");
          }
        });
      }
    });
  });
});
