 class InfiniteCarousel {
            constructor(options = {}) {
                // Configuration
                this.items = options.items || this.getDefaultItems();
                this.autoPlayInterval = options.autoPlayInterval || 3000;
                this.currentIndex = 0;
                this.isAutoPlaying = true;
                this.animationDuration = 500;
                
                // DOM Elements
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
                    { 
                        url: 'https://picsum.photos/id/1015/800/450', 
                        title: 'Mountain Landscape',
                        description: 'Beautiful mountain scenery'
                    },
                    { 
                        url: 'https://picsum.photos/id/104/800/450', 
                        title: 'Waterfall',
                        description: 'Serene waterfall in nature'
                    },
                    { 
                        url: 'https://picsum.photos/id/107/800/450', 
                        title: 'Grass Field',
                        description: 'Golden hour grass field'
                    },
                    { 
                        url: 'https://picsum.photos/id/116/800/450', 
                        title: 'Mountain Lake',
                        description: 'Crystal clear mountain lake'
                    },
                    { 
                        url: 'https://picsum.photos/id/15/800/450', 
                        title: 'Forest Path',
                        description: 'Mysterious forest pathway'
                    },
                    { 
                        url: 'https://picsum.photos/id/169/800/450', 
                        title: 'Sunset Beach',
                        description: 'Beautiful sunset over the ocean'
                    },
                    { 
                        url: 'https://picsum.photos/id/20/800/450', 
                        title: 'Coffee Desk',
                        description: 'Cozy workspace'
                    },
                    { 
                        url: 'https://picsum.photos/id/26/800/450', 
                        title: 'Venice Canal',
                        description: 'Romantic venice scenery'
                    }
                ];
            }
            
            init() {
                this.renderSlides();
                this.renderThumbnails();
                this.attachEventListeners();
                this.showSlide(this.currentIndex);
                this.startAutoPlay();
            }
            
            renderSlides() {
                this.track.innerHTML = '';
                this.items.forEach((item, index) => {
                    const slide = document.createElement('div');
                    slide.className = 'slide';
                    slide.style.backgroundImage = `url(${item.url})`;
                    slide.setAttribute('data-index', index);
                    this.track.appendChild(slide);
                });
            }
            
            renderThumbnails() {
                this.thumbnailContainer.innerHTML = '';
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
            
            showSlide(index) {
                // Remove active class from all slides
                const slides = document.querySelectorAll('.slide');
                slides.forEach(slide => slide.classList.remove('active'));
                
                // Add active class to current slide
                if (slides[index]) {
                    slides[index].classList.add('active');
                }
                
                // Update active thumbnail
                const thumbnails = document.querySelectorAll('.gallery-selector');
                thumbnails.forEach(thumb => thumb.classList.remove('active'));
                if (thumbnails[index]) {
                    thumbnails[index].classList.add('active');
                }
                
                // Update current index
                this.currentIndex = index;
            }
            
            next() {
                const nextIndex = (this.currentIndex + 1) % this.items.length;
                this.showSlide(nextIndex);
            }
            
            prev() {
                const prevIndex = (this.currentIndex - 1 + this.items.length) % this.items.length;
                this.showSlide(prevIndex);
            }
            
            selectSlide(index) {
                if (this.currentIndex === index) return;
                
                // Add a small visual feedback
                const thumbnail = document.querySelector(`.gallery-selector[data-index="${index}"]`);
                if (thumbnail) {
                    thumbnail.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        thumbnail.style.transform = '';
                    }, 200);
                }
                
                this.showSlide(index);
                
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
                
                // Pause on hover (optional)
                const carousel = document.querySelector('.carousel');
                carousel.addEventListener('mouseenter', () => {
                    if (this.isAutoPlaying) this.stopAutoPlay();
                });
                
                carousel.addEventListener('mouseleave', () => {
                    if (!this.isAutoPlaying) this.startAutoPlay();
                });
            }
            
            // Public method to add new slides dynamically
            addSlide(item) {
                this.items.push(item);
                this.renderSlides();
                this.renderThumbnails();
                this.attachEventListeners(); // Re-attach listeners for new thumbnails
            }
            
            // Public method to remove slide
            removeSlide(index) {
                if (index >= 0 && index < this.items.length) {
                    this.items.splice(index, 1);
                    this.renderSlides();
                    this.renderThumbnails();
                    this.attachEventListeners();
                    
                    // Adjust current index if necessary
                    if (this.currentIndex >= this.items.length) {
                        this.currentIndex = this.items.length - 1;
                    }
                    this.showSlide(this.currentIndex);
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
        
        
