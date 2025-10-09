// Author: Aaron Antal-Bento ID: 23013693
document.addEventListener("DOMContentLoaded", () => {
    // Make a GET request to the Flask server
    fetch('/getusersname')
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.text(); // Read the response as plain text
        })
        .then(data => {
            const signin = document.getElementById("signIn");
            const usersname = document.getElementById("usersname");
            const manageaccount = document.getElementById("manageaccount");
            
            if (data == '') {
                signin.style.display = 'inline';
                manageaccount.style.display = 'none';
            } else {
                signin.style.display = 'none';
                manageaccount.style.display = 'inline';
            
                // Update the button's text and icon
                usersname.textContent = data;
                manageaccount.innerHTML += ' <i class="fa-solid fa-user"></i>';
            }            
        })
        .catch(error => {
            console.error("There was a problem with the fetch operation:", error);
        });
});