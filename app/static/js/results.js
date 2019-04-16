var activeRow = "";

function toggle(element) {
    $(activeRow).removeClass("active");
    if (activeRow != element) {
        activeRow = element;
        $(activeRow).addClass("active");
    } else {
        activeRow = "";
    }
}