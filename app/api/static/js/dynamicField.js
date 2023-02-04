$(document).ready(function () {
    var counter = 1;
    $("#addNewProduct").click(function () {
        $("#products").append('<li><label>codigo</label><input type="text" name="codes" required value />' + '<label>valor</label><input type="text" name="values" required value />' + "<input type='button' value='Remove' class='remove'></input></li>");
        counter += 1;
    });

    $("body").on("click", ".remove", function () {
        $(this).closest("li").remove();
        counter -= 1;
    });
});