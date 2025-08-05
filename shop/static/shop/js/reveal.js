document.addEventListener("DOMContentLoaded", () => {
  const sections = document.querySelectorAll(".about-banner");
  let currentIndex = 0;
  let isAnimating = false;

  function scrollToSection(index) {
    if (index < 0 || index >= sections.length) return;
    isAnimating = true;
    sections[index].scrollIntoView({ behavior: "smooth" });
    setTimeout(() => { isAnimating = false; }, 800); // animation duration
    currentIndex = index;
  }

  // Mouse wheel / trackpad
  window.addEventListener("wheel", (e) => {
    if (isAnimating) return;
    if (e.deltaY > 0) {
      scrollToSection(currentIndex + 1);
    } else if (e.deltaY < 0) {
      scrollToSection(currentIndex - 1);
    }
  });

  // Click anywhere to go next
  window.addEventListener("click", () => {
    if (!isAnimating) scrollToSection(currentIndex + 1);
  });
});
