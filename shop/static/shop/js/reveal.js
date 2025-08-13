// This event listener ensures that the code inside it only runs after the entire HTML document has been loaded and parsed
document.addEventListener("DOMContentLoaded", () => {
  // Select all the full-screen banner sections on the page
  const sections = document.querySelectorAll(".about-banner");
  // A variable to keep track of which section the user is currently viewing
  let currentIndex = 0;
  // A "flag" variable to prevent the user from scrolling again while a scroll animation is already in progress
  let isAnimating = false;

  /**
   * A helper function to smoothly scroll to a specific section by its index number
   * @param {number} index - The index of the section to scroll to (e.g., 0 for the first section)
   */
  function scrollToSection(index) {
    // Prevent scrolling beyond the first or last section
    if (index < 0 || index >= sections.length) return;

    // Set the animation flag to true to block other scroll events
    isAnimating = true;

    // This is the core command that tells the browser to smoothly scroll the target section into view
    sections[index].scrollIntoView({ behavior: "smooth" });

    // After a delay (800ms, matching a typical animation duration), set the flag back to false
    setTimeout(() => { isAnimating = false; }, 800); 
    
    // Update the current index to the new section
    currentIndex = index;
  }

  // --- Mouse wheel / trackpad scrolling ---
  // Attaches an event listener to the window to detect mouse wheel/trackpad scrolling
  window.addEventListener("wheel", (e) => {
    // If an animation is already happening, do nothing
    if (isAnimating) return;

    // If the user scrolls down (positive deltaY), go to the next section
    if (e.deltaY > 0) {
      scrollToSection(currentIndex + 1);
    }
    // If the user scrolls up (negative deltaY), go to the previous section
    else if (e.deltaY < 0) {
      scrollToSection(currentIndex - 1);
    }
  });

  // --- Click to scroll ---
  // Attaches an event listener to the window to detect a click anywhere on the page
  window.addEventListener("click", () => {
    if (!isAnimating) scrollToSection(currentIndex + 1);
  });
});
