// Author: Aaron Antal-Bento ID: 23013693
let currentwindowsize = -1;

// Call the function once to set the initial state
checkUpdateCards();
window.addEventListener('resize', checkUpdateCards);

function checkUpdateCards() {
    var windowWidth = window.innerWidth;

    if (windowWidth <= 830 && currentwindowsize != 1) {
        currentwindowsize = 1;
        console.log('window size: ', currentwindowsize);
        updateCards();
    }
    else if (windowWidth > 830 && windowWidth <= 1230 && currentwindowsize != 2) {
        currentwindowsize = 2;
        console.log('window size: ', currentwindowsize);
        updateCards();
    }
    else if (windowWidth > 1230 && currentwindowsize != 3) {
        currentwindowsize = 3;
        console.log('window size: ', currentwindowsize);
        updateCards();
    }
}

function updateCards() {
    // go though each carousel that need to be resized
    updateCarousel(document.querySelector('#myCarousel3'));
    updateCarousel(document.querySelector('#myCarousel2'));
}

function updateCarousel(carousel) {
    $(carousel).carousel(0); // Set to first slide of the carousel

    let carouselindicators = carousel.querySelector('.carousel-indicators');
    let carouselinner = carousel.querySelector('.carousel-inner');

    carouselinner.querySelectorAll('.displaycard').forEach(card => {
        // Calculate new parent ID based on current window size category
        let newparentid = Math.floor(card.id / currentwindowsize);
        let newParent = null;

        // Find the correct carouselslideholder
        carouselinner.querySelectorAll('.carouselslideholder').forEach(holder => {
            if (holder.id == newparentid) {
                newParent = holder;
            }
        });

        if (newParent) {
            newParent.appendChild(card);
        } else {
            // Create a new parent element if not found
            var itemdiv = document.createElement('div');
            itemdiv.classList.add('item');
            carouselinner.appendChild(itemdiv);

            var cslideholderdiv = document.createElement('div');
            cslideholderdiv.classList.add('carouselslideholder');
            cslideholderdiv.id = carouselinner.children.length - 1;
            cslideholderdiv.style.cssText = 'width: 80%; display: flex; justify-content: space-evenly; margin: auto;';
            itemdiv.appendChild(cslideholderdiv);

            // Append the card to the newly created parent
            cslideholderdiv.appendChild(card);
        }
    });

    // Remove empty children of the carousel-inner element
    var slideholders = carousel.querySelectorAll('.carouselslideholder');
    slideholders.forEach(slholder => {
        if (slholder.children.length === 0) {
            carouselinner.removeChild(slholder.parentNode); //remove .item and its child from .carousel-inner
        }
    });

    // Display the correct number of indicators based on the number of childeren in carousel-inner
    let i = carouselinner.children.length;
    if (i == 1)
        i = 0;

    Array.from(carouselindicators.children).forEach(indicator => {
        if (i <= 0) {
            indicator.style.cssText = "display: none;";
        }
        else {
            indicator.style.cssText = "display: inline-block;";
        }
        i--;
    });
}