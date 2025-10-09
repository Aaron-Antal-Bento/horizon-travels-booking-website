// Author: Aaron Antal-Bento ID: 23013693
function updateButtonText(holder) {
    const economyRadio = holder.querySelector('#economyseats');
    const businessRadio = holder.querySelector('#businessseats');
    const bookButton = holder.querySelector('#bookticket');
    const seats = holder.querySelector('#numseats').value;
    const ticketText = seats === '1' ? 'ticket' : 'tickets';

    //total price display
    let price = 0;
    if (economyRadio.checked) {
        price = parseFloat(economyRadio.getAttribute('data-price'));
        if (bookButton != null)
            bookButton.value = `Book ${seats} Standard ${ticketText}`;
    } else {
        price = parseFloat(businessRadio.getAttribute('data-price'));
        if (bookButton != null)
            bookButton.value = `Book ${seats} First-class ${ticketText}`;
    }

    const totalPrice = price * seats;
    holder.querySelector('h1').innerText = '£' + totalPrice.toFixed(2);

    let seatsleft = 0;
    if (economyRadio.checked) {
        seatsleft = economyRadio.getAttribute('data-seatsleft');
    } else {
        seatsleft = businessRadio.getAttribute('data-seatsleft');
    }

    if (bookButton != null) {
        if (parseInt(seatsleft) < parseInt(seats)) {
            bookButton.disabled = true;
            bookButton.value = "No seats available";
        }
        else {
            bookButton.disabled = false;
        }
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.journeyholder').forEach(f => {
        updateButtonText(f);

        var departed = f.querySelector('#departed');
        if (departed !== null) {
            const bookButton = f.querySelector('#bookticket');
            bookButton.id = "hasdeparted";
            bookButton.disabled = true;
            bookButton.value = "Departed";
        }
    });
});

function goBack() {
    window.history.back();
}

function toggleDepartedJourneys() {
    // Select all elements to toggle
    const elements = document.querySelectorAll('#journeyHasDeparted');

    // Find the button
    const icon = document.getElementById('showDepartedCheveron');

    // Check if the elements are currently visible
    let areElementsVisible = Array.from(elements).some(el => !el.classList.contains('hideDeparted'));

    // Toggle the display property and change the button text
    if (areElementsVisible) {
        elements.forEach(el => el.classList.add('hideDeparted'));
        icon.classList = 'fa-solid fa-chevron-right';
    } else {
        elements.forEach(el => el.classList.remove('hideDeparted'));
        icon.classList = 'fa-solid fa-chevron-down';
    }
}

function showAllJourneys() {
    const journeyHolders = document.querySelectorAll('.journeyholder');

    // Remove the 'hide' class from all journey holders
    journeyHolders.forEach(journeyHolder => {
        journeyHolder.classList.remove('hide');
    });
}

function showPlaneJourneys() {
    const journeyHolders = document.querySelectorAll('.journeyholder');

    // Loop through each journey holder
    journeyHolders.forEach(journeyHolder => {
        if (journeyHolder.dataset.type === '1') {
            // Remove 'hide' class for plane journeys
            journeyHolder.classList.remove('hide');
        } else {
            // Add 'hide' class to non-plane journeys
            journeyHolder.classList.add('hide');
        }
    });
}

function showTrainJourneys() {
    const journeyHolders = document.querySelectorAll('.journeyholder');

    // Loop through each journey holder
    journeyHolders.forEach(journeyHolder => {
        if (journeyHolder.dataset.type === '2') {
            // Remove 'hide' class for rail journeys
            journeyHolder.classList.remove('hide');
        } else {
            // Add 'hide' class to non-rail journeys
            journeyHolder.classList.add('hide');
        }
    });
}

function showExpiredTickets() {
    const journeyHolders = document.querySelectorAll('.journeyholder');

    // Loop through each journey holder
    journeyHolders.forEach(journeyHolder => {
        if (journeyHolder.id === 'journeyHasDeparted') {
            // Remove 'hide' class for rail journeys
            journeyHolder.classList.remove('hideDeparted');
        } else {
            // Add 'hide' class to non-rail journeys
            journeyHolder.classList.add('hideDeparted');
        }
    });
}

function showUpcomingTickets() {
    const journeyHolders = document.querySelectorAll('.journeyholder');

    // Loop through each journey holder
    journeyHolders.forEach(journeyHolder => {
        if (journeyHolder.id != 'journeyHasDeparted') {
            // Remove 'hide' class for rail journeys
            journeyHolder.classList.remove('hideDeparted');
        } else {
            // Add 'hide' class to non-rail journeys
            journeyHolder.classList.add('hideDeparted');
        }
    });
}

// Add event listener to all buttons in the group
const buttons = document.querySelectorAll('.journeyType');

buttons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove the 'active' class from all buttons
        buttons.forEach(btn => btn.classList.remove('activeJourneyType'));

        // Add the 'active' class to the clicked button
        button.classList.add('activeJourneyType');
    });
});