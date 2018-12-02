for (let i = 0; i < 10; i++) {

    var columns = ["time", "rain"];
    require("csv-to-array")({
        file: "./files/0" + i + "Historic.csv",
        columns: columns
    }, function (err, array) {
        var result = new Array();
        result = array;
        console.log("var 0" + i + "historic = " + result);

    });
}