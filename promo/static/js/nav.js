const menuToggle = document.getElementById('mobile-nav-toggle');
const mobileNav = document.getElementById('mobile-nav')
const SHOWN_STATE_CLASS = 'show';

const toggleState = (event) => {
   const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
   menuToggle.setAttribute('aria-expanded', !isExpanded);

  if (!isExpanded) {
    mobileNav.classList.toggle('no-display');
      mobileNav.hidden = isExpanded;
    setTimeout(() => {

      mobileNav.classList.toggle('hide');
      mobileNav.querySelector('a').focus();
    }, 50);
  } else {
    mobileNav.classList.toggle('hide');
    menuToggle.focus();
    setTimeout(() => {
      
      mobileNav.hidden = isExpanded;
      mobileNav.classList.toggle('no-display');
    }, 500)
  }
}

const menuEscape = (event) => {
    if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
    menuToggle.setAttribute('aria-expanded', 'false');
    mobileNav.classList.toggle('hide');
    setTimeout(() => {
      mobileNav.classList.toggle('no-display');
      mobileNav.hidden = true;
      menuToggle.focus();
    }, 500)
  }
}

menuToggle.addEventListener('click',  toggleState)
document.addEventListener('keydown',  menuEscape)


