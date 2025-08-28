// <head>でスクリプトを読み込んでいた場合は、"DOM ~"の記述は必要になるが、<body>で読み込んでいた場合は不要。


document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.querySelector(".skill-search-form");
    const skillLabels = document.querySelectorAll(".skill-name-selection");

    // inputを使うことで、文字が入力されるたびにイベントが発火
    searchInput.addEventListener("input", function() {

        // 入力された文字を小文字に直してqueryに格納
        const query = searchInput.value.toLowerCase();

        skillLabels.forEach(label => {

            // SkillLabelsから一つずつ取り出したlabelを小文字に直して格納
            const text = label.textContent.toLowerCase();
            if (text.includes(query)) {
                label.style.display = "inline-block";
            } else {
                label.style.display = "none";
            }
        });
    });
});
