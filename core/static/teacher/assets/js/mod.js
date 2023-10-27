    //delete function getting the modal and button
    var modal = document.getElementById("modaldemo5");
    var yesButton = modal.querySelector("[data-action='delete-course']");

    modal.addEventListener("show.bs.modal", function(event) {
        var triggerButton = event.relatedTarget;
        var coursePk = triggerButton.getAttribute("data-course-pk");
        yesButton.setAttribute("data-course-pk", coursePk); 
    });

    yesButton.addEventListener("click", function() {
        var coursePk = yesButton.getAttribute("data-course-pk");
        if (coursePk) {
            // Construct the GET URL with the course pk and redirect the user
            var getUrl = `/shorterm-course/${coursePk}/delete/`;
            window.location.href = getUrl;
        }
        
        // Close the modal
        modal.modal("hide");
    });


    //description showing function
    var modal = document.getElementById("description");
    var descriptionContent = document.getElementById("description-content");

    modal.addEventListener("show.bs.modal", function(event) {
        var triggerButton = event.relatedTarget;
        var courseDescription = triggerButton.getAttribute("data-course-description");
        // Set the course description in the modal
        descriptionContent.innerHTML = courseDescription;
    });


