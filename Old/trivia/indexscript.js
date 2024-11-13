window.addEventListener("load", function () {

    //when correct answer is clicked change button colour to green
    let correct = document.querySelector('.correct');
    correct.addEventListener('click', function () {
        correct.style.backgroundColor = 'green';
        document.querySelector('#response1').innerHTML = 'Correct!';
    });

    //When any incorrect answer is clicked, change color to red.
    let incorrects = document.querySelectorAll('.incorrect');
    for (let i = 0; i < incorrects.length; i++) {
        incorrects[i].addEventListener('click', function () {
            incorrects[i].style.backgroundColor = 'red';
            document.querySelector('#response1').innerHTML = 'Incorrect';
        });
    }

    document.querySelector('#confirm').addEventListener('click', function() {
        let input = document.querySelector('input');
        if (input.value === 'Picard') {
            input.style.backgroundColor = 'green';
            document.querySelector('#response2').innerHTML = 'Correct!';
            } else {
                input.style.backgroundColor = 'red';
                document.querySelector('#response2').innerHTML = 'Incorrect!';
                    }
    });
});
