// Author: Aaron Antal-Bento ID: 23013693
function ConfirmDelete(){
    const displayElement = document.querySelector('#accountPage2');
    const deleteButton = displayElement.querySelector('.confirmDelete');
    displayElement.style.display = 'flex';
    deleteButton.style.display = 'flex';
}

function ChangeEmail(){
    const displayElement = document.querySelector('#accountPage2');
    const emailForm = displayElement.querySelector('#emailChangeForm');
    displayElement.style.display = 'flex';
    emailForm.style.display = 'flex';
}

function ChangePassword(){
    const displayElement = document.querySelector('#accountPage2');
    const passForm = displayElement.querySelector('#passwordChangeForm');
    displayElement.style.display = 'flex';
    passForm.style.display = 'flex';
}

function HidePage2() {
    const displayElement = document.querySelector('#accountPage2');
    const deleteButton = displayElement.querySelector('.confirmDelete');
    const emailForm = displayElement.querySelector('#emailChangeForm');
    const passForm = displayElement.querySelector('#passwordChangeForm');

    if (displayElement) {
        // Hide the parent element
        displayElement.style.display = 'none';
        deleteButton.style.display = 'none';
        emailForm.style.display = 'none';
        passForm.style.display = 'none';
    }
}