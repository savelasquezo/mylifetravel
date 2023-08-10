var slider = new Glider(document.querySelector('.carousel__lista'), {
    slidesToScroll: 1,
    slidesToShow: 1,
    draggable: false,
    scrollLock: true,
});

slideAutoPlay(slider, '.carousel__lista');

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

const thumbnailsContainer = document.querySelector('.carousel__miniaturas');
const slides = document.querySelectorAll('.carousel__lista img');


slides.forEach((slide, index) => {
    const thumbnail = document.createElement('img');
    thumbnail.src = slide.src;
    thumbnail.classList.add('carousel__miniatura');
    thumbnailsContainer.appendChild(thumbnail);

    thumbnail.addEventListener('click', () => {
        slider.scrollItem(index);
        thumbnail.classList.add('active');
        setTimeout(() => {
            thumbnail.classList.remove('active');
        }, 300);
    });
});