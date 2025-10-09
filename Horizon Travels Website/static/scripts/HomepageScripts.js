// Author: Aaron Antal-Bento ID: 23013693
function updateDropbtn(dropbtn, selectedText) {
    // Trim whitespace
    selectedText = selectedText.trim();

    // Check which dropdown this is (by id).
    switch (dropbtn.id) {
        case 'origins':
            dropbtn.style.padding =
                selectedText === 'Southampton' || selectedText === 'Birmingham'
                    ? '16px 10px'
                    : '16px';
            dropbtn.textContent = 'From: ' + selectedText;
            break;

        case 'destinations':
            dropbtn.style.padding =
                selectedText.includes('Destination') ? '16px 10px' : '16px';
            dropbtn.textContent = 'To: ' + selectedText;
            break;

        case 'passengers':
            // For passengers, add "Passenger(s)" based on the numeric value.
            dropbtn.textContent =
                selectedText + ' Passenger' + (parseInt(selectedText, 10) > 1 ? 's' : '');
            dropbtn.style.padding =
                dropbtn.textContent.includes('Passengers') ? '16px 10px' : '16px';
            break;

        default:
            dropbtn.textContent = selectedText;
    }
}

function resetBtnBackgrounds(container) {
    container.querySelectorAll('button').forEach(btn => {
        btn.style.backgroundColor = 'white';
    });
}

// ---------- Event Handler Functions ----------
function handleDropdownClick(e) {
    const button = e.target;
    const dropdownContent = button.parentElement;
    // Get the associated dropbutton
    const dropbtn = dropdownContent.previousElementSibling;
    const selectedText = button.textContent;

    // Update the dropbutton text and style accordingly.
    updateDropbtn(dropbtn, selectedText);
    getValidCities(button);

    // Reset the background colors of all sibling buttons and highlight the clicked one.
    resetBtnBackgrounds(dropdownContent);
    button.style.backgroundColor = '#f5f5f5';

    // Hide the dropdown content.
    dropdownContent.style.display = 'none';

    const dropdownWrapper = button.closest('.dropdown');
    const inputField = dropdownWrapper.querySelector('input[type="text"], input[type="number"]');
    if (inputField) {
        inputField.value = selectedText;
        inputField.style.display = 'none';
        dropbtn.style.display = 'block';
    }
}

function handleDropdownMouseOver(e) {
    e.target.style.backgroundColor = '#eaeaea';
}

function handleDropdownMouseOut(e) {
    const button = e.target;
    const dropdownContent = button.parentElement;
    const dropbtn = dropdownContent.previousElementSibling;
    const text = button.textContent;

    const anyDestination = dropbtn.textContent.trim() === 'To:' && text.includes('Destination');
    const anyOrigin = dropbtn.textContent.trim() === 'From:' && text.includes('Origin');

    if (dropbtn.textContent.includes(text) || anyDestination || anyOrigin) {
        button.style.backgroundColor = '#f5f5f5';
    } else {
        button.style.backgroundColor = 'white';
    }
}

function setupDropdownContainer(dropdown) {
    // When clicking within the dropdown, open its content.
    dropdown.addEventListener('click', function (e) {
        // Open the dropdown content if the target isn't a dropdown option.
        if (!e.target.matches('.dropdown-content button')) {
            this.querySelector('.dropdown-content').style.display = 'block';
        }
    });
}

function closeDropdown(dropdown) {
    const content = dropdown.querySelector('.dropdown-content');
    content.scrollTop = 0; // Reset scroll position.
    content.style.display = 'none';

    const inputField = dropdown.querySelector('input[type="text"], input[type="number"]');
    const dropbtn = dropdown.querySelector('.dropbtn');
    if (inputField) {
        inputField.style.display = 'none';
    }
    if (dropbtn) {
        dropbtn.style.display = 'block';
    }

    const displayedOptions = Array.from(content.children)
        .filter(option => window.getComputedStyle(option).display !== 'none' && option.id !== 'all');

    if (inputField.type === 'text') {
        if (
            inputField &&
            displayedOptions
                .map(option => option.textContent.trim().toLowerCase())
                .includes(inputField.value.toLowerCase()) &&
            displayedOptions.length === 1
        ) {
            const selectedText = displayedOptions[0].textContent.trim();
            updateDropbtn(dropbtn, selectedText);
            getValidCities(displayedOptions[0]);
            inputField.value = selectedText;
        }
    }
    else if (inputField.type === 'number') {
        if (
            inputField &&
            displayedOptions
                .map(option => option.textContent.trim().toLowerCase())
                .includes(inputField.value.toLowerCase())
        ) {
            const selectedText = inputField.value.trim();
            updateDropbtn(dropbtn, selectedText);
            inputField.value = selectedText;
        }
    }
}

// Global click listener: when clicking anywhere check each dropdown.
document.addEventListener('click', function (e) {
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        // If the click target is not inside this dropdown, close it.
        if (!dropdown.contains(e.target)) {
            closeDropdown(dropdown);
        }
    });
});

// Initialize all dropdowns.
document.querySelectorAll('.dropdown').forEach(dropdown => {
    setupDropdownContainer(dropdown);
});

function handleDropbtnToggle(e) {
    const dropbtn = e.currentTarget;
    const dropdown = dropbtn.closest('.dropdown');
    const inputField = dropdown.querySelector('input[type="text"], input[type="number"]');
    if (!inputField) return;

    // Hide the dropbutton and show the input field.
    dropbtn.style.display = 'none';
    inputField.style.display = 'block';
    inputField.focus();

    if (inputField.value.startsWith('Any')) inputField.value = '';
    inputField.select()

    // Also display the dropdown content.
    dropdown.querySelector('.dropdown-content').style.display = 'block';
}

function filterDropdownOptions(e) {
    const inputField = e.target;
    const searchTerm = inputField.value.toLowerCase();
    const dropdown = inputField.closest('.dropdown');
    const options = dropdown.querySelectorAll('.dropdown-content button');

    const optionsArray = Array.from(options).filter(option =>
        option.dataset.validcity === "true" || !option.dataset.validcity
    );
    const matchingOptions = optionsArray.filter(option =>
        option.textContent.toLowerCase().startsWith(searchTerm)
    );

    if (matchingOptions.length === 0 && searchTerm !== "") {
        // If none match and the search term isn't empty, display all options
        optionsArray.forEach(option => option.style.display = 'block');
    } else {
        // Otherwise, display only those starting with the search term
        optionsArray.forEach(option => {
            if (option.textContent.toLowerCase().startsWith(searchTerm) || option.id === 'all') {
                option.style.display = 'block';
            } else {
                option.style.display = 'none';
            }
        });
    }
}
// ---------- Attach Event Listeners ----------

// Attach event listeners for all dropdown option buttons.
document.querySelectorAll('.dropdown-content button').forEach(button => {
    button.addEventListener('click', handleDropdownClick);
    button.addEventListener('mouseover', handleDropdownMouseOver);
    button.addEventListener('mouseout', handleDropdownMouseOut);
});

document.querySelectorAll('.dropinput').forEach(input => {
    input.addEventListener('keydown', function (event) {    // Check if the Enter key was pressed.
        if (event.key === 'Enter') {
            event.preventDefault();
            const content = input.parentElement.querySelector('.dropdown-content');
            const dropbtn = input.parentElement.querySelector('.dropbtn');

            content.scrollTop = 0;  // Reset scroll position.
            content.style.display = 'none';
            input.style.display = 'none';
            dropbtn.style.display = 'block';

            let displayedOptions = Array.from(content.children)
                .filter(option => window.getComputedStyle(option).display !== 'none' && option.id !== 'all')
                .map(option => option);

            if (displayedOptions.length == 0 || input.value.trim() == '') displayedOptions = Array.from(content.children)
                .filter(option => window.getComputedStyle(option).display !== 'none')
                .map(option => option);

            let selectedText = displayedOptions[0].textContent.trim();
            if (input.type === 'number') selectedText = input.value.trim();
            updateDropbtn(dropbtn, selectedText);
            getValidCities(displayedOptions[0]);
            input.value = selectedText;
        }
    });
    if (input.type === 'text')
        input.addEventListener('input', filterDropdownOptions);
    else if (input.type === 'number')
        input.addEventListener('input', (event) => {
            if (event.inputType) {
                closeDropdown(input.parentElement);
            }
        });
});

// Set up the container behavior for all dropdown elements.
document.querySelectorAll('.dropdown').forEach(dropdown => {
    setupDropdownContainer(dropdown);
});

// Attach toggle behavior for dropbuttons.
document.querySelectorAll('.dropbtn').forEach(btn => {
    btn.addEventListener('click', handleDropbtnToggle);
});

// Initialize date selector with current date
function start() {
    const date = new Date();
    document.getElementById("dateselector").childNodes[0].nodeValue = formatDate(date.getDay(), date.getDate(), date.getMonth(), date.getFullYear());

    // Format dates to "YYYY-MM-DD"
    var today = new Date();
    var threeMonthsFromToday = new Date();
    threeMonthsFromToday.setMonth(today.getMonth() + 3);

    var formattedToday = today.toISOString().split('T')[0];
    var formattedThreeMonths = threeMonthsFromToday.toISOString().split('T')[0];

    document.getElementById("dateselectorinput").setAttribute('min', formattedToday);
    document.getElementById("dateselectorinput").setAttribute('max', formattedThreeMonths);
    document.getElementById("dateselectorinput").value = formattedToday;

}

// Get selected date and format it
function getDate() {
    let selectedDate = document.getElementById("dateselectorinput").value;
    const date = new Date(selectedDate);
    document.getElementById("dateselector").childNodes[0].nodeValue = formatDate(date.getDay(), date.getDate(), date.getMonth(), date.getFullYear());
}

// Format the date in a readable format
function formatDate(dayofweek, day, month, year) {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

    return `${days[dayofweek]} ${day} of ${months[month]} ${year}`;
}

function getValidCities(button) {
    const dropdown = button.closest('.dropdown'); // Closest dropdown container
    const dropbtn = dropdown.querySelector('.dropbtn'); // Find the .dropbtn within the dropdown

    if (button.id === 'all') {
        dropbtn.dataset.value = 'all'; // Update the button's data attribute
    }
    else {
        dropbtn.dataset.value = button.innerText; // Update the button's data attribute
    }

    if (dropbtn.id == 'origins' || dropbtn.id == 'destinations') {
        // Create a FormData object from the form
        const getCitiesForm = new FormData();
        getCitiesForm.append("constriantOriginDest", dropbtn.id == "origins" ? "origin" : "destination");
        getCitiesForm.append('availableOriginDest', dropbtn.id == "origins" ? "destination" : "origin");
        getCitiesForm.append('city', dropbtn.dataset.value);

        // Send the form data to the server using the POST method
        fetch('/getcities', {
            method: 'POST',
            body: getCitiesForm
        })
            .then(response => response.json())
            .then(responseData => {
                // Handle the server response
                console.log(dropbtn.dataset.value, ' has: ', responseData, ' valid cities.');

                var dropbtnSearch = document.querySelector(dropbtn.id == "origins" ? "#destinationscontent" : "#originscontent");
                Array.from(dropbtnSearch.children).forEach(cityToMod => {
                    if (responseData.includes(cityToMod.innerText) || cityToMod.id === 'all') {
                        cityToMod.style.display = 'block';
                        cityToMod.dataset.validcity = true;
                    }
                    else {
                        cityToMod.style.display = 'none';
                        cityToMod.dataset.validcity = false;
                    }
                });
            })
            .catch(error => {
                // Handle any errors
                console.error('Error:', error);
            });
    }
}

document.getElementById('search').addEventListener('click', function () {
    const switchloadingicon = document.getElementById('switchtoloading');
    switchloadingicon.className = 'fa-solid fa-spinner fa-spin';
    setTimeout(() => {
        switchloadingicon.className = 'fa fa-magnifying-glass';
    }, 1000); // 1000 milliseconds = 1 second

    const origin = document.getElementById('origins').dataset.value || 'all';
    const destination = document.getElementById('destinations').dataset.value || 'all';
    const passengers = document.getElementById('passengers').dataset.value || '1';
    const date = document.getElementById('dateselectorinput').value || '';

    const searchParams = new URLSearchParams({
        origin,
        destination,
        passengers,
        date
    }).toString();

    const searchURL = `/HorizonTravels/journeys?${searchParams}`;
    window.location.href = searchURL;
});