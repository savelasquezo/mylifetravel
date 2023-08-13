var slider = new Glider(document.querySelector('.glider-slide'), {
    slidesToScroll: 1,
    slidesToShow: 1,
    draggable: false,
    scrollLock: true,
});

slideAutoPlay(slider, '.glider-slide');

function slideAutoPlay(glider, selector, delay = 4500, repeat = true) {
    let autoplay = null;
    const slidesCount = glider.track.childElementCount;
    let nextIndex = 1;
    let pause = true;

    function slide() {
        autoplay = setInterval(() => {
            if (nextIndex >= slidesCount) {
                if (!repeat) {
                    clearInterval(autoplay);
                } else {
                    nextIndex = 0;
                }
            }
            glider.scrollItem(nextIndex++);
        }, delay);
    }

    slide();

    var element = document.querySelector(selector);
    element.addEventListener('mouseover', (event) => {
        if (pause) {
            clearInterval(autoplay);
            pause = false;
        }
    }, 300);

    element.addEventListener('mouseout', (event) => {
        if (!pause) {
            slide();
            pause = true;
        }
    }, 300);
}

const thumbnailsContainer = document.querySelector('.glider__miniaturas');
const slides = document.querySelectorAll('.glider-slide img');


slides.forEach((slide, index) => {
    const thumbnail = document.createElement('img');
    thumbnail.src = slide.src;
    thumbnail.classList.add('glider__miniatura');
    thumbnailsContainer.appendChild(thumbnail);

    thumbnail.addEventListener('click', () => {
        slider.scrollItem(index);
        thumbnail.classList.add('active');
        setTimeout(() => {
            thumbnail.classList.remove('active');
        }, 300);
    });
});