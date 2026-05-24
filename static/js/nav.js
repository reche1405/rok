const menuToggle = document.getElementById('mobile-nav-toggle');
const mobileNav = document.getElementById('mobile-nav')
const SHOWN_STATE_CLASS = 'show';

const toggleState = (event) => {
   const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
  console.log("Test hello!!!!")
  menuToggle.setAttribute('aria-expanded', !isExpanded);
  mobileNav.hidden = isExpanded;
  console.log(isExpanded);
  if (!isExpanded) {
    mobileNav.querySelector('a').focus();
  } else {
    menuToggle.focus();
  }
}

const menuEscape = (event) => {
    if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
    menuToggle.setAttribute('aria-expanded', 'false');
    mobileNav.hidden = true;
    menuToggle.focus();
  }
}

menuToggle.addEventListener('click',  toggleState)
document.addEventListener('keydown',  menuEscape)


