function deleteNote(noteId){ //fetch is the method for requesting in javascript
    fetch('/delete-note', {
        method:'POST', 
        body: JSON.stringify({noteId:noteId}), 
    }).then((_res) => {
        windows.location.href = '/';  //this refreshes the page after deleting note when requesting
    });
}

//This sends a request to the backend in javascript