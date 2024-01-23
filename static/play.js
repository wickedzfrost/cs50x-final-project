document.addEventListener("DOMContentLoaded", function func() {
    wanakana.bind(document.querySelector("#wanakana-input"));
    let input = document.querySelector("#wanakana-input");
    $('#showscore').modal({ show: false})
    // Logs the value of the input field

    // input.addEventListener("keyup", function log() {
    //     console.log(input.value);
    // });

    var new_score = 0;

    function submit_score(score) {
        var jqXHR = $.ajax({
            type: "POST",
            url: "/submit_score",
            async: false,
            data: {score}
        });
    }

    function submit(input) {
        var jqXHR = $.ajax({
            type: "POST",
            url: "/submit",
            async: false,
            data: {input}
        });
        return jqXHR.responseText;
    }

    function check(n, bool, user_score) {
        if (bool == true) {
            n.style.backgroundColor = "#90EE90";
            n.style.opacity = 0.65;
        }
        else {
            n.style.backgroundColor = "#DC143C";
            n.style.opacity = 0.65;
            setTimeout(() => { $('#showscore').modal('show'); }, 300);
            let score = document.querySelector("#score-final");
            score.innerHTML = user_score;
            submit_score(user_score);
            $('#showscore').on('hidden.bs.modal', function redirect() {
                window.location.replace("/history");
            })
        }
    }

    function runScript(text, type){
        if (type == "script") {
            var jqXHR = $.ajax({
                type: "POST",
                url: "/script",
                async: false,
                data: {text}
            });
            return jqXHR.responseText;
        }
        else if (type == "genword") {
            var jqXHR = $.ajax({
                type: "POST",
                url: "/genword",
                async: false,
                data: {text}
            });
            return jqXHR.responseText;
        }
        else if (type == "genword_s") {
            var jqXHR = $.ajax({
                type: "POST",
                url: "/genword_special",
                async: false,
                data: {text}
            });
            return jqXHR.responseText;
        }
        else {
            return "Error type"
        }
    }

    function nextword(curr) {
        let last_mora = curr[curr.length - 1];
        var new_word = runScript(last_mora, "genword");
        var KEY, VALUE;
        let jsonObject = JSON.parse(new_word);
        for (let key in jsonObject) {
            KEY = key;
            VALUE = jsonObject[key];
        }
        return [KEY, VALUE];
    }

    function nextword_s(curr) {
        let last_mora = curr;
        last_mora = last_mora.slice(curr.length - 2, curr.length);
        var new_word = runScript(last_mora, "genword_s");
        var KEY, VALUE;
        let jsonObject = JSON.parse(new_word);
        for (let key in jsonObject) {
            KEY = key;
            VALUE = jsonObject[key];
        }
        return [KEY, VALUE];
    }

    input.addEventListener("keypress", function(key) {
        if (key.key == "Enter") {
            let text = input.value;
            let question = document.querySelector("#word").innerHTML;
            let bool = false;

            // Remove last letter if it's not a mora
            if (text[text.length - 1] == "ー") {
                text = text.slice(0, -1);
            }

            if (question[question.length - 1] == "ー") {
                question = question.slice(0, -1);
            }

            let condition = false;
            if ((text[0]) == question[(question.length) - 1]) {
                condition = true;
            }
            else if (question[(question.length - 1)] == "ゃ" || question[(question.length) - 1] == "ゅ" || question[(question.length) - 1] == "ょ") {
                if ((text[0] == question[(question.length - 2)]) && (text[1] == question[(question.length - 1)])) {
                    condition = true;
                }
            }

            if ((condition == true && text.length > 1) && (text[text.length - 1] != "ん" && text[text.length - 1] != "ン")) {
                var temp = submit(text);
                if (temp == "false") {
                    bool = false;
                    check(input, bool, new_score);
                    return;
                }

                let encoded = runScript(text, "script");
                if (encoded == "FALSE") {
                    bool = false;
                    check(input, bool, new_score);
                    return;
                }
                else {
                    let decode = new URLSearchParams(encoded);
                    let value = decode.get("text");
                    // check for yoon kanas
                    if (value[value.length - 1] == "ゃ" || value[value.length - 1] == "ゅ" || value[value.length - 1] == "ょ") {
                        bool = true;
                        check(input, bool, new_score);

                        let new_word = nextword_s(value);
                        question = document.querySelector("#word");
                        question.innerHTML = new_word[0];
                        let def = document.querySelector("#definition");
                        def.innerHTML = new_word[1];

                        input.value = "";

                        let score = document.querySelector("#score").innerHTML;
                        new_score = parseInt(score);
                        new_score++;
                        document.querySelector("#score").innerHTML = new_score;
                    }
                    // for normal kanas
                    else {
                        bool = true;
                        check(input, bool, new_score);

                        let new_word = nextword(value);
                        question = document.querySelector("#word");
                        question.innerHTML = new_word[0];
                        let def = document.querySelector("#definition");
                        def.innerHTML = new_word[1];

                        input.value = "";

                        let score = document.querySelector("#score").innerHTML;
                        new_score = parseInt(score);
                        new_score++;
                        document.querySelector("#score").innerHTML = new_score;
                    }
                }
            }
            else {
                bool = false;
                check(input, bool, new_score);
                return;
            }
        }
    });
});
