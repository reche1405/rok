class InfiniteCarousel {
    constructor(options = {}) {
        // Configuration
        this.items = options.items || this.getDefaultItems();
        this.autoPlayInterval = options.autoPlayInterval || 3000;
        this.currentIndex = 0;
        this.isAutoPlaying = true;
        this.animationDuration = 500;
        this.isAnimating = false;
        this.orientation = options.orientation || 'portrait';
        // DOM Elements
        this.wrapper = document.querySelector('.carousel');
        this.wrapper.classList.add(this.orientation);
        this.track = document.getElementById('carouselTrack');
        this.thumbnailContainer = document.getElementById('thumbnailContainer');
        this.playPauseBtn = document.getElementById('playPauseBtn');
        this.prevBtn = document.getElementById('prevBtn');
        this.nextBtn = document.getElementById('nextBtn');
        
    // Bind methods
        this.next = this.next.bind(this);
        this.prev = this.prev.bind(this);
        this.selectSlide = this.selectSlide.bind(this);
        this.toggleAutoPlay = this.toggleAutoPlay.bind(this);
        
        // Initialize
        this.init();
    }
    
    getDefaultItems() {
        return [
            { url: 'https://picsum.photos/id/1015/800/450', title: 'Mountain Landscape' },
            { url: 'https://picsum.photos/id/104/800/450', title: 'Waterfall' },
            { url: 'https://picsum.photos/id/107/800/450', title: 'Grass Field' },
            { url: 'https://picsum.photos/id/116/800/450', title: 'Mountain Lake' },
            { url: 'https://picsum.photos/id/15/800/450', title: 'Forest Path' },
            { url: 'https://picsum.photos/id/169/800/450', title: 'Sunset Beach' },
            { url: 'https://picsum.photos/id/20/800/450', title: 'Coffee Desk' },
            { url: 'https://picsum.photos/id/26/800/450', title: 'Venice Canal' }
        ];
    }
    
    // Create carousel array with duplicate first slide at the end
    getCarouselItems() {
        const carouselItems = [...this.items];
        if (this.items.length > 0) {
            // Duplicate the first slide and add it to the end
            carouselItems.push({ ...this.items[0], isDuplicate: true });
        }
        return carouselItems;
    }
    
    init() {
        this.renderSlides();
        this.renderThumbnails();
        this.attachEventListeners();
        this.showSlide(this.currentIndex, true); // Skip animation for initial render
        this.startAutoPlay();
    }
    
    renderSlides() {
        this.track.innerHTML = '';
        const carouselItems = this.getCarouselItems();
        
        carouselItems.forEach((item, index) => {
            const slide = document.createElement('div');
            slide.className = 'slide';
            slide.style.backgroundImage = `url(${item.url})`;
            slide.setAttribute('data-index', index);
            if (item.isDuplicate) {
                slide.setAttribute('data-duplicate', 'true');
            }
            this.track.appendChild(slide);
        });
    }
    
    renderThumbnails() {
        this.thumbnailContainer.innerHTML = '';
        // Only render thumbnails for original items, not the duplicate
        this.items.forEach((item, index) => {
            const thumbnail = document.createElement('button');
            thumbnail.className = 'gallery-selector';
            thumbnail.setAttribute('data-index', index);
            
            const img = document.createElement('img');
            img.src = item.url;
            img.alt = item.title;
            
            thumbnail.appendChild(img);
            thumbnail.addEventListener('click', () => this.selectSlide(index));
            this.thumbnailContainer.appendChild(thumbnail);
        });
    }
    
    showSlide(index, skipAnimation = false) {
        // Prevent animation conflicts
        if (this.isAnimating && !skipAnimation) return;
        
        const carouselItems = this.getCarouselItems();
        const totalSlides = carouselItems.length;
        
        // Ensure index is within bounds
        let normalizedIndex = Math.min(index, totalSlides - 1);
        
        if (skipAnimation) {
            // Remove transition temporarily
            this.track.classList.add('no-transition');
            this.track.style.transform = `translateX(-${normalizedIndex * 100}%)`;
            
            // Force reflow
            this.track.offsetHeight;
            
            // Restore transition
            this.track.classList.remove('no-transition');
        } else {
            // Normal animated slide
            this.isAnimating = true;
            this.track.style.transform = `translateX(-${normalizedIndex * 100}%)`;
            
            // Handle duplicate slide reset after animation
            const currentSlide = carouselItems[normalizedIndex];
            if (currentSlide && currentSlide.isDuplicate) {
                // This is the duplicate first slide - after animation, reset to real first slide
                setTimeout(() => {
                    // Temporarily disable transitions
                    this.track.classList.add('no-transition');
                    
                    // Jump back to the real first slide (index 0)
                    this.track.style.transform = 'translateX(0%)';
                    this.currentIndex = 0;
                    
                    // Force reflow
                    this.track.offsetHeight;
                    
                    // Re-enable transitions
                    this.track.classList.remove('no-transition');
                    
                    // Update active thumbnail to first slide
                    const thumbnails = document.querySelectorAll('.gallery-selector');
                    thumbnails.forEach(thumb => thumb.classList.remove('active'));
                    if (thumbnails[0]) {
                        thumbnails[0].classList.add('active');
                    }
                    
                    this.isAnimating = false;
                }, this.animationDuration);
            } else {
                // Normal slide - just reset animation flag after transition
                setTimeout(() => {
                    this.isAnimating = false;
                }, this.animationDuration);
            }
        }
        
        // Update current index (but don't update if we just showed duplicate and will reset)
        const currentSlide = carouselItems[normalizedIndex];
        if (!currentSlide || !currentSlide.isDuplicate) {
            this.currentIndex = normalizedIndex;
            
            // Update active thumbnail (only for original slides)
            if (normalizedIndex < this.items.length) {
                const thumbnails = document.querySelectorAll('.gallery-selector');
                thumbnails.forEach(thumb => thumb.classList.remove('active'));
                if (thumbnails[normalizedIndex]) {
                    thumbnails[normalizedIndex].classList.add('active');
                }
            }
        }
    }
    
    next() {
        if (this.isAnimating) return;
        
        const carouselItems = this.getCarouselItems();
        const totalSlides = carouselItems.length;
        const nextIndex = this.currentIndex + 1;
        
        if (nextIndex >= totalSlides) {
            // This shouldn't happen with our duplicate approach, but as a fallback
            this.showSlide(0, false);
        } else {
            this.showSlide(nextIndex, false);
        }
    }
    
    prev() {
        if (this.isAnimating) return;
        
        let prevIndex = this.currentIndex - 1;
        
        if (prevIndex < 0) {
            // Going backwards from first slide - go to last real slide
            const carouselItems = this.getCarouselItems();
            prevIndex = carouselItems.length - 2; // Skip the duplicate
            
            // Jump instantly to last real slide (no animation for wrap-around)
            this.showSlide(prevIndex, true);
        } else {
            this.showSlide(prevIndex, false);
        }
    }
    
    selectSlide(index) {
        if (this.currentIndex === index || this.isAnimating) return;
        
        // Add visual feedback
        const thumbnail = document.querySelector(`.gallery-selector[data-index="${index}"]`);
        if (thumbnail) {
            thumbnail.style.transform = 'scale(0.95)';
            setTimeout(() => {
                thumbnail.style.transform = '';
            }, 200);
        }
        
        // Direct navigation to the selected slide (always use animation unless it's a wrap)
        // If going from near end to beginning, we might need special handling
        const isWrapForward = (index === 0 && this.currentIndex > this.currentIndex);
        
        if (isWrapForward) {
            // Jump instantly for wrap-around via thumbnail click
            this.showSlide(index, true);
        } else {
            this.showSlide(index, false);
        }
        
        // Reset auto-play timer if playing
        if (this.isAutoPlaying) {
            this.resetAutoPlay();
        }
    }
    
    startAutoPlay() {
        if (this.autoPlayTimer) {
            clearInterval(this.autoPlayTimer);
        }
        
        this.autoPlayTimer = setInterval(() => {
            this.next();
        }, this.autoPlayInterval);
        
        this.isAutoPlaying = true;
        this.updatePlayPauseButton();
    }
    
    stopAutoPlay() {
        if (this.autoPlayTimer) {
            clearInterval(this.autoPlayTimer);
            this.autoPlayTimer = null;
        }
        
        this.isAutoPlaying = false;
        this.updatePlayPauseButton();
    }
    
    toggleAutoPlay() {
        if (this.isAutoPlaying) {
            this.stopAutoPlay();
        } else {
            this.startAutoPlay();
        }
    }
    
    resetAutoPlay() {
        if (this.isAutoPlaying) {
            this.stopAutoPlay();
            this.startAutoPlay();
        }
    }
    
    updatePlayPauseButton() {
        if (this.isAutoPlaying) {
            this.playPauseBtn.classList.remove('paused');
        } else {
            this.playPauseBtn.classList.add('paused');
        }
    }
    
    attachEventListeners() {
        this.prevBtn.addEventListener('click', () => {
            this.prev();
            if (this.isAutoPlaying) this.resetAutoPlay();
        });
        
        this.nextBtn.addEventListener('click', () => {
            this.next();
            if (this.isAutoPlaying) this.resetAutoPlay();
        });
        
        this.playPauseBtn.addEventListener('click', this.toggleAutoPlay);
        
        // Pause on hover
        const carousel = document.querySelector('.carousel');
        if (carousel) {
            carousel.addEventListener('mouseenter', () => {
                if (this.isAutoPlaying) this.stopAutoPlay();
            });
            
            carousel.addEventListener('mouseleave', () => {
                if (!this.isAutoPlaying) this.startAutoPlay();
            });
        }
        
        // Add touch swipe support
        this.attachSwipeEvents();
    }
    
    attachSwipeEvents() {
        let touchStartX = 0;
        let touchEndX = 0;
        const carousel = document.querySelector('.carousel');
        
        if (!carousel) return;
        
        carousel.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
        });
        
        carousel.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            this.handleSwipe(touchStartX, touchEndX);
        });
    }
    
    handleSwipe(startX, endX) {
        const swipeThreshold = 50;
        const diff = endX - startX;
        
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                this.prev();
            } else {
                this.next();
            }
            
            if (this.isAutoPlaying) this.resetAutoPlay();
        }
    }
    
    // Public method to add new slides dynamically
    addSlide(item) {
        this.items.push(item);
        this.renderSlides();
        this.renderThumbnails();
        
        // Reset to first slide without animation
        this.currentIndex = 0;
        this.showSlide(0, true);
    }
    
    // Public method to remove slide
    removeSlide(index) {
        if (index >= 0 && index < this.items.length) {
            this.items.splice(index, 1);
            this.renderSlides();
            this.renderThumbnails();
            
            // Adjust current index if necessary
            if (this.currentIndex >= this.items.length) {
                this.currentIndex = this.items.length - 1;
            }
            this.showSlide(this.currentIndex, true);
        }
    }
    
    // Clean up method
    destroy() {
        if (this.autoPlayTimer) {
            clearInterval(this.autoPlayTimer);
        }
        
        this.prevBtn.removeEventListener('click', this.prev);
        this.nextBtn.removeEventListener('click', this.next);
        this.playPauseBtn.removeEventListener('click', this.toggleAutoPlay);
    }
}