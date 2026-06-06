// 1. Setup the configuration options
const observerOptions = {
  root: null,         // Use the browser viewport as the container
  rootMargin: '0px',  // No shrinking/growing of the viewport bounds
  threshold: 0.2      // Trigger when 10% of the card is visible
};

// 2. Define the callback function
const observerCallback = (entries, observer) => {
  entries.forEach(entry => {
    // Check if the element has entered the viewport
    if (entry.isIntersecting) {
      // Add the class that triggers the CSS transition
      entry.target.classList.add('in-frame');
      
      // Stop observing this element once it has animated in (optional)
      observer.unobserve(entry.target);
    }
  });
};

// 3. Initialize the observer
const observer = new IntersectionObserver(observerCallback, observerOptions);

// 4. Target all cards and track them
const hiddenElements = document.querySelectorAll('.animate-on-scroll');
hiddenElements.forEach(el => observer.observe(el));