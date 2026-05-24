export default class Slideshow {
    constructor(wrapperElement, showIndicators = true) {
        this.wrapperElement = wrapperElement;
        this.slides = this.wrapperElement.querySelectorAll('.slide');
        if(this.slides.length < 1) {
            return;
        }
        this.slides[0].classList.add('next');
        this.slideDuration = this.wrapperElement.dataset.slideDuration;
        this.slideType = this.wrapperElement.dataset.slideType;
        this.transitionDuration = this.wrapperElement.dataset.transitionDuration;
        this.options = {slideDuration: this.slideDuration, transitionDuration: this.transitionDuration};
        this.interval = null;
        this.isPlaying = false;
        this.showIndicators = this.slides.length > 1 ? showIndicators : false;

        this.indicators = this.setIndicators();
        this.initPlayPuaseButton();
        this.fadeOut = null;
         if (this.slides.length < 2) {

            this.slides[0].classList.remove("next");
            this.slides[0].classList.add("current");
        } 
       



    }

    startSlideshow = () => {

        /* console.log("The current slideshow is playing:", this.isPlaying, this.wrapperElement) */
        if(!this.isPlaying) {

            this.isPlaying = true;

            /* console.log("This is confirmation that the slideshow has been started."); */
            this.nextSlide = this.getNextSlide();
            if(this.nextSlide === null) {
                this.nextSlide = this.slides[0];
            }
            this.setCurrentSlide(this.nextSlide);
            this.interval = this.slides.length > 1 && setInterval(() => {
                /* console.log("This is an interval iteration for the slideshow.") */
                this.setCurrentSlide(this.nextSlide);
            }, this.options.slideDuration)
        }    
    }

    stopSlideshow = () => {
        if(this.slides.length < 2 || this.wrapperElement.classList.contains('permanent')) {
            return;
        }
        if(this.isPlaying) {

            this.isPlaying = false;

            clearInterval(this.interval);
            this.interval = null;
            clearTimeout(this.fadeOut);
            this.fadeOut = null;
            this.nextSlide.classList.remove('next');
            this.nextSlide.classList.remove('current');
            this.nextSlide = null;
            const currentSlide = this.wrapperElement.querySelector('.current');
            currentSlide.classList.remove('fading-out');
        }
    }

    setCurrentSlide = (slide) => {
        if(!this.isPlaying) return;
        if(this.slides.length < 2) {
                return;   

        }
        slide.classList.add('current');
        slide.classList.remove('next');
        this.setNextSlide(slide);

        this.setNextIndicator(parseInt(slide.dataset.slideNumber));
        this.fadeOut = setTimeout(() => {
            this.setFadeOutClass(slide);
        }, this.options.slideDuration - this.options.transitionDuration);
    }
    
    setFadeOutClass = (slide) => {
        slide.style = `animation-duration: ${this.options.transitionDuration / 1000}s;`;
        slide.classList.add('fading-out');
        slide.classList.remove('current');
        setTimeout(() => {
            this.removeFadeOutClass(slide);
        }, this.options.transitionDuration)
    }
    
    removeFadeOutClass = slide => {
        slide.classList.remove('fading-out');
    }
    
    getNextSlide = () => {
        const nextSlide = this.wrapperElement.querySelector('.next');
        return nextSlide;
    }
    
    setNextSlide = currentSlide => {
        const nextElem = currentSlide.nextElementSibling;

        if(nextElem) {
            if(nextElem.classList.contains('slide')) {
                currentSlide.nextElementSibling.classList.add('next');
                this.nextSlide = nextElem;

                return;
            }
        }  
        const firstElem = this.wrapperElement.querySelector('.slide');
        firstElem.classList.add('next');
        this.nextSlide = firstElem;
    }

    setIndicators = () => {
        if(!this.showIndicators) return;
        if(this.slides.length < 2) return;
        const progressContainer = this.wrapperElement.querySelector('.slide-progress__container'); 
        const indicators = [];
        for(let i = 0; i < this.slides.length; i++) {
            const progressBar = document.createElement('div');
            progressBar.setAttribute('data-slide-number', i)
            progressBar.classList.add('slide-progress__bar');
            const currentProgress = document.createElement('div');
            currentProgress.classList.add('slide-progress__current');
            currentProgress.style = `animation-duration: ${(this.slideDuration - (this.transitionDuration / 5)) / 1000}s; `;
            progressBar.appendChild(currentProgress);
            progressContainer.appendChild(progressBar);
            indicators.push(progressBar);

        }
        return indicators;
    }


    setNextIndicator = (slideNumber) => {
        if(!this.showIndicators) return;
        if(slideNumber === 0) {
            this.indicators.forEach(indicator => {
                if(parseInt(indicator.dataset.slideNumber) === this.slides.length - 1) {
                    indicator.classList.remove('current');
                    indicator.classList.add('played');
                    setTimeout(() => {
                        indicator.classList.remove('played');
                    }, this.slideDuration)

                } else {
                    indicator.classList.remove('played');
                }
            })

        }
        this.indicators.forEach(indicator => {
            if(parseInt(indicator.dataset.slideNumber) < slideNumber) {
                indicator.classList.remove('current');
                indicator.classList.add('played');
            }
            if(parseInt(indicator.dataset.slideNumber) === slideNumber) {
                indicator.classList.add('current')
            }
        })
    }  

    
    initPlayPuaseButton = () => {
        if(!this.showIndicators) return;
        const svgns = "http://www.w3.org/2000/svg";

        const overlay = this.wrapperElement.querySelector('.slideshow__overlay');

        const playPauseButton = document.createElement('button');
        playPauseButton.classList.add('slider-play-pause__button');
        const playSVG = document.createElementNS(svgns,"svg");
        
        playSVG.setAttribute('xmlns', svgns)
        playSVG.classList.add('play-icon');
        playSVG.setAttribute("width", 20);
        playSVG.setAttribute("height", 20);
        playSVG.setAttribute("viewBox", "0 0 20 20")
        const path = document.createElementNS(svgns, 'polygon');
        path.setAttribute('points', "4,2 16,10 4,18 ");
        path.setAttribute("fill", "#ffffff");
        playSVG.appendChild(path);
        playPauseButton.appendChild(playSVG);
        overlay.appendChild(playPauseButton);

        const pauseSVG = document.createElementNS(svgns, "svg");
        pauseSVG.classList.add('pause-icon'); 
        pauseSVG.setAttribute("width", 20);
        pauseSVG.setAttribute("height", 20);
        pauseSVG.setAttribute("viewBox", "0 0 20 20")
        const pauseRect = document.createElementNS(svgns, "rect");
        const secondRect = document.createElementNS(svgns, "rect");
        pauseRect.setAttribute("x", "4.5");
        pauseRect.setAttribute("y", "3.5");
        pauseRect.setAttribute("height", "15");
        pauseRect.setAttribute("width", "3");
        pauseRect.setAttribute("fill", "#ffffff");

        secondRect.setAttribute("x", "10.5");
        secondRect.setAttribute("y", "3.5");
        secondRect.setAttribute("height", "15");
        secondRect.setAttribute("width", "3");
        secondRect.setAttribute("fill", "#ffffff");
        pauseSVG.appendChild(pauseRect);
        pauseSVG.appendChild(secondRect);
        pauseSVG.classList.add('current');

        playPauseButton.appendChild(pauseSVG);
        playPauseButton.addEventListener('click', this.togglePlayPuaseButton);

    }
    
    togglePlayPuaseButton = event => {
        if(this.isPlaying) {
            if (this.wrapperElement.querySelector(".play-icon")) {

                this.wrapperElement.querySelector(".play-icon").classList.add('current');
                this.wrapperElement.querySelector(".pause-icon").classList.remove('current');
            }
            this.stopSlideshow();
            
        } else {
            if(this.wrapperElement.querySelector(".play-icon")) {

                this.wrapperElement.querySelector(".play-icon").classList.remove('current');
                this.wrapperElement.querySelector(".pause-icon").classList.add('current');
            }
            this.startSlideshow();
           
        }
    }
}
