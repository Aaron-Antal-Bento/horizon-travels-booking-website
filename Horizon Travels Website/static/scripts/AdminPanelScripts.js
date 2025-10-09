// Author: Aaron Antal-Bento ID: 23013693
function showHint(str) {
    if (str.length == 0) str = '*';

    fetch("/ajax_users/?q=" + str)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            // Target the "Suggestions" div
            const suggestionsDiv = document.getElementById("Suggestions");
            suggestionsDiv.style.display = 'block';
            // Clear previous suggestions
            suggestionsDiv.innerHTML = "";

            if (Array.isArray(data) && data.length > 0) {
                // Create a button for each suggestion
                data.forEach(item => {
                    const button = document.createElement("button");
                    button.className = "suggestionbutton";
                    button.textContent = item.userstr; // Display the userstr in the button

                    // Optionally: Add an event listener to handle button clicks
                    button.addEventListener("click", () => {
                        event.preventDefault();
                        document.querySelectorAll(".valuesaved").forEach((element) => {
                            element.classList.remove("valuesaved");
                        });
                        document.querySelectorAll(".valuefailed").forEach((element) => {
                            element.classList.remove("valuefailed");
                        });
                        document.querySelectorAll(".valueedited").forEach((element) => {
                            element.classList.remove("valueedited");
                        });
                        document.getElementById("Suggestions").style.display = "none";
                        fetchUser(item.userid); // Example action on click
                    });

                    // Append the button to the "Suggestions" div
                    suggestionsDiv.appendChild(button);
                });
            } else {
                // Handle no suggestions case
                const noSuggestionsMessage = document.createElement("p");
                noSuggestionsMessage.textContent = "No suggestions available";
                suggestionsDiv.appendChild(noSuggestionsMessage);
            }
        })
        .catch(error => console.error("Fetch error:", error));
}

function fetchUser(userid) {
    if (userid.length === 0) {
        return;
    } else {
        fetch("/getuserinfo/?id=" + userid)
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then(data => {
                // Populate form inputs with retrieved data
                document.getElementById("usersdetails").style.display = 'flex';
                document.getElementById("searchheader").classList.add('scrollHeader');
                document.getElementById("UserInfo").dataset.userid = userid;
                document.getElementById("fname").value = data.FirstName || "";
                document.getElementById("lname").value = data.LastName || "";
                document.getElementById("email").value = data.Email || "";
                document.getElementById("password").value = "";
                document.getElementById("rdate").value = data.RegDate || "";
                document.getElementById("rtime").value = data.RegTime || "";
                document.getElementById("usertype").value = data.UserType || "Standard";
                document.getElementById("deleteUserAccount").onclick = function () {
                    location.href = `/admindeleteaccount/${userid}`;
                };

                // Populate the cards table
                const cardsTableBody = document.querySelector("#cards tbody");
                cardsTableBody.innerHTML = ""; // Clear any existing rows

                if (data.Cards.length > 0) {
                    data.Cards.forEach(card => {
                        // Create a new row
                        const row = document.createElement("tr");

                        // Create cells for the row
                        const nameCell = document.createElement("td");
                        nameCell.textContent = card[1] || "N/A";

                        const cardNumberCell = document.createElement("td");
                        cardNumberCell.textContent = card[2] || "N/A";

                        const expiryDateCell = document.createElement("td");
                        if (card[5])
                            expiryDateCell.style.color = 'red';
                        expiryDateCell.textContent = card[3] || "N/A";

                        const cvvCell = document.createElement("td");
                        cvvCell.textContent = card[4] || "N/A";

                        const removeCell = document.createElement("td");
                        const removeButton = document.createElement("button");
                        removeButton.innerHTML = '<i class="fa-solid fa-trash"></i>';
                        removeButton.id = 'removebtnbtn';
                        removeButton.onclick = () => removeCard(row, card[0]);
                        removeCell.appendChild(removeButton);

                        // Append cells to the row
                        row.appendChild(nameCell);
                        row.appendChild(cardNumberCell);
                        row.appendChild(expiryDateCell);
                        row.appendChild(cvvCell);
                        row.appendChild(removeCell);

                        // Append the row to the table body
                        cardsTableBody.appendChild(row);
                    });
                }
                else {
                    const row = document.createElement("tr");
                    const nocardstext = document.createElement("td");
                    nocardstext.textContent = "No cards to display...";
                    nocardstext.setAttribute("colspan", "5");
                    nocardstext.style.textAlign = "center";
                    row.appendChild(nocardstext);
                    cardsTableBody.appendChild(row);
                }

                BookingsTable(data);
            })
            .catch(error => console.error("Fetch error:", error));
    }
}

function BookingsTable(data) {
    const cardsTableBody = document.querySelector("#bookings tbody");
    cardsTableBody.innerHTML = ""; // Clear any existing rows

    if (data.Bookings.length > 0) {
        data.Bookings.forEach(booking => {
            const row = document.createElement("tr");
            const bookingid = booking[0];
            booking.splice(0, 1);

            row.dataset.departed = booking[11];

            row.appendChild(createCell((booking[0] == 1) ? "Plane" : "Train"));
            row.appendChild(createCell(booking[1]));
            row.appendChild(createCell(booking[2]));
            row.appendChild(createInputCell("date", booking[3], "JourneyDate"));
            row.appendChild(createCell(booking[4]));
            row.appendChild(createInputCell("datetime-local", booking[5], "BookingDate"));
            row.appendChild(createCell(booking[6]));
            row.appendChild(createInputCell("number", booking[7], "Seats", '40px'));
            row.appendChild(createDropdownCell(["standard", "first class"], booking[8], "Seattype"));
            row.appendChild(createInputCell("number", booking[9], "PricePaidPerSeat", '40px'));
            row.appendChild(createDropdownCell(["true", "false"], (booking[10] == 1) ? "true" : "false", "Cancelled"));
            row.appendChild(createButtonCell('<i class="fa-solid fa-trash"></i>', "removebtnbtn", () => removeBooking(row, bookingid)));
            row.appendChild(createButtonCell("Submit", "submitbtn", () => submitBookingChanges(row, bookingid)));

            if (booking[10]) {
                row.style.backgroundColor = "rgb(255, 177, 177)";
            } else if (booking[11]) {
                row.style.backgroundColor = "rgb(255, 226, 177)";
            }

            cardsTableBody.appendChild(row);
        });
    }
    else {
        const row = document.createElement("tr");
        const nocardstext = document.createElement("td");
        nocardstext.textContent = "No bookings to display...";
        nocardstext.setAttribute("colspan", "11");
        nocardstext.style.textAlign = "center";
        row.appendChild(nocardstext);
        cardsTableBody.appendChild(row);
    }
}

function removeCard(row, cardID) {
    // Send DELETE request to Flask server
    fetch(`/admindeletecard/${cardID}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to delete card");
            }
            // Remove the row from the table
            row.remove();
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while deleting the card.");
        });
}

function removeBooking(row, bookingID) {
    // Send DELETE request to Flask server
    fetch(`/admindeletebooking/${bookingID}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to delete booking");
            }
            // Remove the row from the table
            row.remove();
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while deleting the booking.");
        });
}

function removeJourney(row, journeyID) {
    // Send DELETE request to Flask server
    fetch(`/admindeletejourney/${journeyID}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to delete journey");
            }
            // Remove the row from the table
            row.remove();
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while deleting the journey.");
        });
}

const form1 = document.getElementById("UserInfo");
// Handle form submission
form1.addEventListener("submit", (event) => {
    event.preventDefault(); // Prevent the default form submission

    // Collect form data
    const formData = new FormData(form1);
    const data = {};
    formData.forEach((value, key) => {
        // Get the form element associated with the key
        const element = form1.querySelector(`[name="${key}"]`);

        // Check if the element has the desired class
        if (element && element.classList.contains("valueedited") || element && element.classList.contains("valuefailed")) {
            data[key] = value; // Add to the data object only if the class exists
        }
    });

    userid = form1.dataset.userid;

    // Send the data to the server
    fetch("/updateuserinfo/?id=" + userid, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.text();
        })
        .then(() => {
            document.querySelectorAll(".valuesaved").forEach((element) => {
                element.classList.remove("valuesaved");
            });
            document.querySelectorAll(".valuefailed").forEach((element) => {
                element.classList.remove("valuefailed");
                element.classList.add("valuesaved");
            });
            document.querySelectorAll(".valueedited").forEach((element) => {
                element.classList.remove("valueedited");
                element.classList.add("valuesaved");
            });
        })
        .catch((error) => {
            document.querySelectorAll(".valuesaved").forEach((element) => {
                element.classList.remove("valuesaved");
            });
            document.querySelectorAll(".valueedited").forEach((element) => {
                element.classList.remove("valueedited");
                element.classList.add("valuefailed");
            });
            console.error("Error:", error);
            alert("An error occurred while updating user details.");
        });
});

const textInput = document.getElementById("txt1");
const elementToShow = document.getElementById("Suggestions");
document.addEventListener("click", (event) => {
    if (!textInput.contains(event.target) && !elementToShow.contains(event.target)) {
        elementToShow.style.display = "none";
    }
});

const form2 = document.getElementById("UserInfo");
// Listen for changes in all input fields
form2.addEventListener("input", (event) => {
    const target = event.target;

    // Only apply the highlight if the edited element is an input
    if (target.tagName === "INPUT" || target.tagName === "SELECT") {
        target.classList.remove("valuesaved");
        target.classList.remove("valuefailed");
        target.classList.add("valueedited");
    }

    if (target.id === "password" && target.value === "") {
        target.classList.remove("valueedited"); // Remove the edited class
    }
});

function submitBookingChanges(row, bookingid) {
    const data = {};
    const userBookingElements = row.querySelectorAll(".UserBooking");

    // Loop through each element to collect values
    userBookingElements.forEach((element) => {
        const name = element.name; // Ensure each input has a valid "name" attribute
        const value = element.value;

        // Check if the element has "valueedited" or "valuefailed" class
        if (element.classList.contains("valueedited") || element.classList.contains("valuefailed") || element.name == 'Seattype' || element.name == 'Seats') {
            if (name) {
                data[name] = value; // Add to data object
            }
        }
    });

    // Send the data to the server
    fetch("/updateuserbooking/?id=" + bookingid, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.text();
        })
        .then(() => {
            // Handle successful updates
            row.querySelectorAll(".valuesaved").forEach((element) => {
                element.classList.remove("valuesaved");
            });
            row.querySelectorAll(".valuefailed").forEach((element) => {
                element.classList.remove("valuefailed");
                element.classList.add("valuesaved");
            });
            row.querySelectorAll(".valueedited").forEach((element) => {
                element.classList.remove("valueedited");
                element.classList.add("valuesaved");
            });

            if (row.querySelector("[name='Cancelled']").value == 'true')
                row.style.backgroundColor = 'rgb(255, 177, 177)';
            else if (row.dataset.departed == 'true')
                row.style.backgroundColor = 'rgb(255, 226, 177)';
            else
                row.style.backgroundColor = 'white';
        })
        .catch((error) => {
            // Handle errors
            row.querySelectorAll(".valuesaved").forEach((element) => {
                element.classList.remove("valuesaved");
            });
            row.querySelectorAll(".valueedited").forEach((element) => {
                element.classList.remove("valueedited");
                element.classList.add("valuefailed");
            });
            console.error("Error:", error);
            alert("An error occurred while updating the user booking.");
        });
}

function submitJourneyChanges(row, journeyid) {
    const data = {};
    const userJourneyElements = row.querySelectorAll(".UserBooking");

    // Loop through each element to collect values
    userJourneyElements.forEach((element) => {
        const name = element.name; // Ensure each input has a valid "name" attribute
        const value = element.value;

        // Check if the element has "valueedited" or "valuefailed" class
        if (element.classList.contains("valueedited") || element.classList.contains("valuefailed")) {
            if (name) {
                data[name] = value; // Add to data object
            }
        }
    });

    // Send the data to the server
    fetch("/updatejourney/?id=" + journeyid, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.text();
        })
        .then(() => {
            // Handle successful updates
            row.querySelectorAll(".valuesaved").forEach((element) => {
                element.classList.remove("valuesaved");
            });
            row.querySelectorAll(".valuefailed").forEach((element) => {
                element.classList.remove("valuefailed");
                element.classList.add("valuesaved");
            });
            row.querySelectorAll(".valueedited").forEach((element) => {
                element.classList.remove("valueedited");
                element.classList.add("valuesaved");
            });
        })
        .catch((error) => {
            // Handle errors
            row.querySelectorAll(".valuesaved").forEach((element) => {
                element.classList.remove("valuesaved");
            });
            row.querySelectorAll(".valueedited").forEach((element) => {
                element.classList.remove("valueedited");
                element.classList.add("valuefailed");
            });
            console.error("Error:", error);
            alert("An error occurred while updating the journey.");
        });
}

function loadJourneys() {
    fetch("/getjourneys/")
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            // Populate form inputs with retrieved data
            document.getElementById("journeys").style.display = 'block';
            document.getElementById("showjourneysbtn").innerHTML = 'Reload <i class="fa-solid fa-rotate"></i>';

            // Populate the cards table
            const journeysTableBody = document.querySelector("#journeys tbody");
            journeysTableBody.innerHTML = ""; // Clear any existing rows

            if (data.length > 0) {
                data.forEach((journey, index) => {
                    // Create a new row
                    const row = document.createElement("tr");
                    row.style.backgroundColor = index % 2 === 0 ? "white" : "whitesmoke";
                    const journeyid = journey['journeyid'];

                    row.appendChild(createCell(journeyid));
                    row.appendChild(createDropdownCell(["UKAir", "BritishTrains"], journey['companyid'], "companyid"));
                    row.appendChild(createInputCell("text", journey['origin'], "origin", '80px'));
                    row.appendChild(createInputCell("time", journey['departuretime'], "departuretime"));
                    row.appendChild(createInputCell("text", journey['destination'], "destination", '80px'));
                    row.appendChild(createInputCell("time", journey['arrivaltime'], "arrivaltime"));
                    row.appendChild(createInputCell("number", journey['price'], "price", '40px'));

                    row.querySelectorAll("td").forEach((cell) => {
                        cell.style.textAlign = 'left';
                    });

                    row.appendChild(createButtonCell('<i class="fa-solid fa-trash"></i>', "removebtnbtn", () => removeJourney(row, journeyid)));
                    row.appendChild(createButtonCell("Submit", "submitbtn", () => submitJourneyChanges(row, journeyid)));

                    // Append the row to the table body
                    journeysTableBody.appendChild(row);
                });
            }
            else {
                const row = document.createElement("tr");
                const nocardstext = document.createElement("td");
                nocardstext.textContent = "No journeys to display...";
                nocardstext.setAttribute("colspan", "7");
                nocardstext.style.textAlign = "center";
                row.appendChild(nocardstext);
                journeysTableBody.appendChild(row);
            }
        })
        .catch(error => console.error("Fetch error:", error));
}

function createCell(content = "N/A") {
    const cell = document.createElement("td");
    cell.textContent = content;
    return cell;
}

function createInputCell(type, value, name, width = null) {
    const cell = document.createElement("td");
    const input = document.createElement("input");
    input.type = type;
    input.value = value || "";
    input.name = name;
    if (width)
        input.style.width = width;
    input.classList.add("UserBooking");
    input.addEventListener("input", (event) => {
        const target = event.target;
        target.classList.remove("valuesaved", "valuefailed");
        target.classList.add("valueedited");
    });
    cell.appendChild(input);
    return cell;
}

function createDropdownCell(options, selectedValue, name) {
    const cell = document.createElement("td");
    const dropdown = document.createElement("select");
    options.forEach(optionText => {
        const option = document.createElement("option");
        option.value = optionText;
        option.textContent = optionText;
        dropdown.appendChild(option);
    });
    dropdown.value = selectedValue;
    dropdown.name = name;
    dropdown.classList.add("UserBooking");
    dropdown.addEventListener("input", (event) => {
        const target = event.target;
        target.classList.remove("valuesaved", "valuefailed");
        target.classList.add("valueedited");
    });
    cell.appendChild(dropdown);
    return cell;
}

function createButtonCell(innerHTML, id, callback) {
    const cell = document.createElement("td");
    const button = document.createElement("button");
    button.innerHTML = innerHTML;
    button.id = id;
    button.onclick = callback;
    cell.appendChild(button);
    return cell;
}

document.getElementById("submitJourney").addEventListener("click", function () {
    const form = document.getElementById("addJourneyForm");
    const inputs = form.querySelectorAll(".UserBooking");

    // Check if all fields are filled
    let allFilled = true;
    inputs.forEach(input => {
        if (!input.value) {
            allFilled = false;
            input.style.border = "2px solid red"; // Highlight missing fields
        } else {
            input.style.border = ""; // Remove highlight if filled
        }
    });

    if (!allFilled) {
        return; // Stop submission if validation fails
    }

    // Gather form data
    const formData = {};
    inputs.forEach(input => {
        formData[input.name] = input.value;
    });

    // Send data to Flask endpoint
    fetch("/addnewjourney/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(formData)
    })
        .then(response => {
            if (response.ok) {
                alert("Journey added successfully!");
                form.reset(); // Clear the form
            } else {
                alert("Failed to add journey.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while submitting the journey.");
        });
});

document.querySelectorAll(".UserBooking").forEach(input => {
    input.addEventListener("input", (event) => {
        const target = event.target;

        // Remove the red border when the user enters a value
        if (target.value) {
            target.style.border = ""; // Clear border style
        }
    });
});

function getTopCustomers() {
    fetch("/gettopcustomers/")
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            // Populate form inputs with retrieved data
            document.getElementById("topcustomers").style.display = 'block';
            const topCTableBody = document.querySelector("#topcustomers tbody");
            topCTableBody.innerHTML = ""; // Clear any existing rows

            if (data.length > 0) {
                data.forEach((customer, index) => {
                    // Create a new row
                    const row = document.createElement("tr");

                    // Create cells for the row
                    const rankingCell = document.createElement("td");
                    rankingCell.textContent = index + ".";
                    rankingCell.style.backgroundColor = 'gainsboro'

                    const idCell = document.createElement("td");
                    idCell.textContent = customer[0] || "N/A";
                    const nameCell = document.createElement("td");
                    nameCell.textContent = customer[1] || "N/A";
                    const emailCell = document.createElement("td");
                    emailCell.textContent = customer[2] || "N/A";

                    const numBookCell = document.createElement("td");
                    numBookCell.textContent = customer[3] || "N/A";
                    const numSeatsCell = document.createElement("td");
                    numSeatsCell.textContent = customer[4] || "N/A";
                    const amountSpentCell = document.createElement("td");
                    amountSpentCell.textContent = customer[5]
                        ? Number(customer[5]).toLocaleString('en-GB', {
                            style: 'currency',
                            currency: 'GBP',
                            maximumFractionDigits: 0
                        })
                        : "N/A";

                    const topJourneyCell = document.createElement("td");
                    topJourneyCell.textContent = customer[6] || "N/A";

                    // Append cells to the row
                    row.append(rankingCell);
                    row.appendChild(idCell);
                    row.appendChild(nameCell);
                    row.appendChild(emailCell);
                    row.appendChild(numBookCell);
                    row.appendChild(numSeatsCell);
                    row.appendChild(amountSpentCell);
                    row.appendChild(topJourneyCell);

                    // Append the row to the table body
                    topCTableBody.appendChild(row);
                });
            }
            else {
                const row = document.createElement("tr");
                const nouserstext = document.createElement("td");
                nouserstext.textContent = "No customers...";
                nouserstext.setAttribute("colspan", "7");
                nouserstext.style.textAlign = "center";
                row.appendChild(nouserstext);
                topCTableBody.appendChild(row);
            }
            document.getElementById('topcustomers').scrollIntoView({ behavior: 'smooth', block: 'center' });
        })
        .catch(error => console.error("Fetch error:", error));
}

// This function calls the Flask endpoint to retrieve booking data
function fetchBookingData() {
    fetch('/booking-info')
        .then(response => response.json())
        .then(data => {
            // Get the container element and clear any existing content
            const container = document.getElementById("bookingsContainer");
            container.innerHTML = "";

            // Iterate over the fetched booking data array
            data.forEach(booking => {
                if (booking[0] == true) {
                    const totalCapacity = Number(booking[7]) + Number(booking[9]);
                    const bookedSeats = Number(booking[6]) + Number(booking[8]);
                    const greenPercentage = totalCapacity > 0 ? (booking[6] / totalCapacity * 100).toFixed(2) : 0;
                    const bluePercentage = totalCapacity > 0 ? (booking[8] / totalCapacity * 100).toFixed(2) : 0;
                    const greyPercentage = totalCapacity > 0 ? (100 - greenPercentage - bluePercentage).toFixed(2) : 0;

                    bookingHTML = `
                    <div class="bookingContainer">
                        <h2 style="margin-bottom: 5px; width: fit-content; display: inline;">${booking[1]}-${booking[2]}</h2>
                        <h3 style="display: inline; width: fit-content;">${booking[3]}</h3>
                        <h3>${booking[4]}</h3>
                        <p style="margin-bottom: 10px;">${booking[5]}</p>
                        <h3>Seat availability ${totalCapacity - bookedSeats}/${totalCapacity}</h3>
                        <div class="seat-bar">
                            <div class="seat-green" style="width: ${greenPercentage}%;"></div>
                            <div class="seat-blue" style="width: ${bluePercentage}%;"></div>
                            <div class="seat-grey" style="width: ${greyPercentage}%;"></div>
                        </div>
                        <p><span style="color: lightgreen;">Standard: ${booking[6]}/${booking[7]}</span>, <span style="color: blue;">First class: ${booking[8]}/${booking[9]}</span>, <span style="color: red;">Cancelled: ${booking[10]}</span></p>
                        <p style="margin-bottom: 10px;">Individual bookings: ${booking[11]}</p>
                        <h3>Journey income: £${booking[12]}</h3>
                    </div>
                    `;
                }
                else {
                    bookingHTML = `<div style="width: 100%; display: flex;">
                    <h3 style="display: inline; width: fit-content;">${booking[1]}</h3>
                    <div class="dateLine"></div>
                    </div>`
                }

                // Append the new booking item into the container
                container.insertAdjacentHTML('beforeend', bookingHTML);
            });
        })
        .catch(error => console.error("Error fetching booking data:", error));
}