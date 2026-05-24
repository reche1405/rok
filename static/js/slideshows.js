import Slideshow from "./slideshow.js";


document.addEventListener('DOMContentLoaded', () => {
    const slideshows = document.querySelectorAll('.slideshow');
    const slideshowObjs = [];
    const options = {
        threshold: [0,0.25,0.5,0.75,1]
    }

    const getSlideShowObject = elementNode => {

        for(let obj of slideshowObjs) {
            if(obj.wrapperElement.isSameNode(elementNode)) {
                return obj;
            }
        }
        console.log("We were unable to find the corresponding object")
    }

    const observerCallback = entries => {
        entries.forEach(entry => {
            let object = getSlideShowObject(entry.target);
            if (object) {
                
                if(entry.intersectionRatio > 0.5) {   
                    
                    object.startSlideshow();
                    return;
                } else {
                    object.stopSlideshow();
                }
            } else {
                console.log('There was no object here!')
            }
        })
    }





    const slideshowObserver = new IntersectionObserver(observerCallback, options);
    slideshows.forEach(slideshow => {
        if(!slideshow.classList.contains('permanent')) {

            slideshowObserver.observe(slideshow);
        }

    })
    slideshows.forEach(slideshowElement => {
        const slideshowObj = new Slideshow(slideshowElement);
        slideshowObjs.push(slideshowObj);
        if(slideshowElement.classList.contains('permanent')) {
            slideshowObj.startSlideshow();
        }
    })
});
