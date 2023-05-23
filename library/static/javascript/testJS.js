function testJS() {
    var confirmation = confirm('Ar tikrai norite ištrinti šią knygą?');
    if (confirmation) {
        return true;
    } else {
        return false;
    }
}