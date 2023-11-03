    //delete function getting the modal and button
    var modal = document.getElementById("modaldemo5");
    var yesButton = modal.querySelector("[data-action='delete-teacher']");

    modal.addEventListener("show.bs.modal", function(event) {
        var triggerButton = event.relatedTarget;
        var teacherPk = triggerButton.getAttribute("data-teacher-pk");
        yesButton.setAttribute("data-teacher-pk", teacherPk); 
    });

    yesButton.addEventListener("click", function() {
        var teacherPk = yesButton.getAttribute("data-teacher-pk");
        if (teacherPk) {
            // Construct the GET URL with the teacher pk and redirect the user
            var getUrl = `/teachers/${teacherPk}/delete/`;
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


