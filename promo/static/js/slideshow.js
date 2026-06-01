export default class Slideshow {
    constructor(wrapperElement, showIndicators = true) {
        this.wrapperElement = wrapperElement;
        this.slides = this.wrapperElement.querySelectorAll('.slide');
        
        if (this.slides.length < 1) return;

        // Parse dataset values properly
        this.slideDuration = parseInt(this.wrapperElement.dataset.slideDuration) || 5000;
        this.transitionDuration = parseInt(this.wrapperElement.dataset.transitionDuration) || 1000;
        this.slideType = this.wrapperElement.dataset.slideType || 'fade'; // Defaulting to 'fade' matching your logic
        this.options = { 
            slideDuration: this.slideDuration, 
            transitionDuration: this.transitionDuration,
            slideType: this.slideType
        };

        // Assign slide numbers
        this.slides.forEach((slide, index) => {
            if (!slide.dataset.slideNumber) {
                slide.setAttribute('data-slide-number', index);
            }
        });

        // Initial state
        this.currentSlideIndex = 0;
        this.timeoutId = null;
        this.fadeOutTimeoutId = null;
        this.isPlaying = false;
        this.showIndicators = this.slides.length > 1 ? showIndicators : false;

        // Initialize based on slide type
        if (this.slideType === 'scroll') {
            this.setupScrollMode();
        } else {
            this.setupFadeMode();
        }

        this.indicators = this.setIndicators();
        this.initPlayPauseButton();
        this.initFullscreenButton();
    
        // Listen for fullscreen changes
        document.addEventListener('fullscreenchange', this.handleFullscreenChange);
            
        if (this.slides.length > 1) {
            this.startSlideshow();
        }
    }

    setupFadeMode() {
        if (this.slides.length === 1) {
            this.slides[0].classList.add("current");
        } else {
            this.slides[0].classList.add("current");
            this.slides[1].classList.add("next");
        }
    }

    setupScrollMode() {
        this.updateSlidePositions(0);
    }

    startSlideshow = () => {
        if (this.slides.length < 2 || this.isPlaying) return;
        this.isPlaying = true;
        this.runSlideshowCycle();
    }

    runSlideshowCycle = () => {
        if (!this.isPlaying) return;

        // Calculate exactly when the transition needs to start triggering
        const msBeforeFadeStarts = this.options.slideDuration - this.options.transitionDuration;

        this.fadeOutTimeoutId = setTimeout(() => {
            const currentSlide = this.slides[this.currentSlideIndex];
            const nextSlideIndex = (this.currentSlideIndex + 1) % this.slides.length;
            const nextSlide = this.slides[nextSlideIndex];
            
            if (this.options.slideType === 'scroll') {
                this.updateSlidePositions(nextSlideIndex);
            } else {
                // --- THE FADE FIX ---
                // 1. Explicitly inject the transition speed directly into the style layer
                currentSlide.style.animationDuration = `${this.options.transitionDuration / 1000}s`;
                nextSlide.style.animationDuration = `${this.options.transitionDuration / 1000}s`;

                // 2. Start fading out the old slide, but do NOT strip its layer priority yet
                currentSlide.classList.add('fading-out');
                
                // 3. Keep the next slide ready in the background stack layer
                nextSlide.classList.add('next');
            }

            // Prepare the future upcoming element class hook safely
            const futureSlideIndex = (nextSlideIndex + 1) % this.slides.length;
            this.slides.forEach((s, idx) => {
                if (idx !== this.currentSlideIndex && idx !== nextSlideIndex && idx !== futureSlideIndex) {
                    s.classList.remove('next', 'current', 'fading-out');
                }
            });

            this.setNextIndicator(nextSlideIndex);

            // 4. Wait for the transition duration animation to fully finish executing
            this.timeoutId = setTimeout(() => {
                if (this.options.slideType === 'fade') {
                    // Clean up classes strictly *after* the opacity animation finishes
                    currentSlide.classList.remove('current', 'fading-out');
                    currentSlide.style.animationDuration = '';

                    // Promote the new slide to the active front-row slot
                    nextSlide.classList.remove('next');
                    nextSlide.classList.add('current');
                }
                
                this.currentSlideIndex = nextSlideIndex;
                this.runSlideshowCycle();
            }, this.options.transitionDuration);

        }, msBeforeFadeStarts > 0 ? msBeforeFadeStarts : 200);
    }

    stopSlideshow = () => {
        if (this.slides.length < 2 || this.wrapperElement.classList.contains('permanent')) return;
        
        this.isPlaying = false;
        clearTimeout(this.timeoutId);
        clearTimeout(this.fadeOutTimeoutId);
        
        this.slides.forEach(slide => {
            slide.classList.remove('fading-out');
            slide.style.animationDuration = '';
        });
    }

    updateSlidePositions(index) {
        const container = this.wrapperElement.querySelector('.slides-container');
        if (container) {
            const translatePercent = -index * 100;
            container.style.transform = `translateX(${translatePercent}%)`;
        }
    }

    initFullscreenButton = () => {
        const overlay = this.wrapperElement.querySelector('.slideshow__overlay');
        if (!overlay) return;

        const svgns = "http://www.w3.org/2000/svg";
        const fullscreenButton = document.createElement('button');
        fullscreenButton.classList.add('slider-fullscreen__button');
        fullscreenButton.setAttribute('type', 'button');
        
        const fullscreenSVG = document.createElementNS(svgns, "svg");
        fullscreenSVG.classList.add('fullscreen-icon', 'current');
        fullscreenSVG.setAttribute("width", "20");
        fullscreenSVG.setAttribute("height", "20");
        fullscreenSVG.setAttribute("viewBox", "0 0 24 24");
        
        const path = document.createElementNS(svgns, "path");
        path.setAttribute("d", "M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z");
        path.setAttribute("fill", "#ffffff");
        fullscreenSVG.appendChild(path);
        
        const exitSVG = document.createElementNS(svgns, "svg");
        exitSVG.classList.add('exit-fullscreen-icon');
        exitSVG.setAttribute("width", "20");
        exitSVG.setAttribute("height", "20");
        exitSVG.setAttribute("viewBox", "0 0 24 24");
        
        const exitPath = document.createElementNS(svgns, "path");
        exitPath.setAttribute("d", "M5 16h3v3h2v-5H5v2zm3-8H5v2h5V5H8v3zm6 11h2v-3h3v-2h-5v5zm2-11V5h-2v5h5V8h-3z");
        exitPath.setAttribute("fill", "#ffffff");
        exitSVG.appendChild(exitPath);
        
        fullscreenButton.appendChild(fullscreenSVG);
        fullscreenButton.appendChild(exitSVG);
        overlay.appendChild(fullscreenButton);
        
        fullscreenButton.addEventListener('click', this.toggleFullscreen);
    }

    toggleFullscreen = async () => {
        const fullscreenIcon = this.wrapperElement.querySelector(".fullscreen-icon");
        const exitIcon = this.wrapperElement.querySelector(".exit-fullscreen-icon");
        
        try {
            if (!document.fullscreenElement) {
                await this.wrapperElement.requestFullscreen();
                if (fullscreenIcon) fullscreenIcon.classList.remove('current');
                if (exitIcon) exitIcon.classList.add('current');
            } else {
                await document.exitFullscreen();
                if (fullscreenIcon) fullscreenIcon.classList.add('current');
                if (exitIcon) exitIcon.classList.remove('current');
            }
        } catch (error) {
            console.error('Fullscreen error:', error);
        }
    }

    // FIX: Changed to an arrow function to lock down the lexical scope of `this`
    handleFullscreenChange = () => {
        if (!document.fullscreenElement) {
            this.wrapperElement.style.background = '';
            this.wrapperElement.style.padding = '';
        } else {
            this.wrapperElement.style.background = '#000';
            this.wrapperElement.style.padding = '0';
        }
    }

    setIndicators = () => {
        if(!this.showIndicators) return [];
        if(this.slides.length < 2) return [];
        const progressContainer = this.wrapperElement.querySelector('.slide-progress__container'); 
        if(!progressContainer) return [];

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
        if(!this.showIndicators || !this.indicators.length) return;
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

    initPlayPauseButton = () => {
        if(!this.showIndicators) return;
        const svgns = "http://www.w3.org/2000/svg";
        const overlay = this.wrapperElement.querySelector('.slideshow__overlay');
        if (!overlay) return;

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
        playPauseButton.addEventListener('click', this.togglePlayPauseButton);
    }
    
    togglePlayPauseButton = event => {
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