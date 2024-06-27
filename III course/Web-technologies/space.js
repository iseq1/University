//board
let tileSize = 32;
let rows = 16;
let columns = 16;

let board;
let boardWidth = tileSize * columns; // 32 * 16
let boardHeight = tileSize * rows; // 32 * 16
let context;

// корабль
let shipWidth = tileSize * 2;
let shipHeight = tileSize;
let shipX = tileSize * columns / 2 - tileSize;
let shipY = tileSize * rows - tileSize * 2;

let ship = {
    x: shipX,
    y: shipY,
    width: shipWidth,
    height: shipHeight
}

let shipImg;
let shipVelocityX = tileSize; // скорость кораблика

// пришельцы
let alienArray = [];
let alienWidth = tileSize * 2;
let alienHeight = tileSize;
let alienX = tileSize;
let alienY = tileSize;
let alienImg;

let alienRows = 2;
let alienColumns = 3;
let alienCount = 0; // количество пришельцев, которых нужно победить
let alienVelocityX = 1; // скорость пришельцев

// пули
let bulletArray = [];
let bulletVelocityY = -10; // скорость пули
let score = 0;
let gameOver = false;
let gameWon = false;

window.onload = function () {
    board = document.getElementById("board");
    board.width = boardWidth;
    board.height = boardHeight;
    context = board.getContext("2d"); // используется для рисования на canvas

    // подгружаем изображение корабля
    shipImg = new Image();
    shipImg.src = "./images/ship.png";
    shipImg.onload = function () {
        context.drawImage(shipImg, ship.x, ship.y, ship.width, ship.height);
    }

    alienImg = new Image();
    alienImg.src = "./images/alien.png";
    createAliens();

    requestAnimationFrame(update);
    document.addEventListener("keydown", moveShip);
    document.addEventListener("keyup", shoot);

    let nextLevelButton = document.getElementById("nextLevelButton");
    nextLevelButton.addEventListener("click", nextLevel);

    let restartButton = document.getElementById("restartButton");
    restartButton.addEventListener("click", restartGame);
}

function update() {
    if (gameOver || gameWon) {
        // Показать сообщение "Ты выиграл!" или "Ты проиграл!"
        context.font = "52px courier";
        if (gameOver) {
            context.fillStyle = "red";
            context.fillText("Ты проиграл!", boardWidth / 2 - 150, boardHeight / 2);
            document.getElementById("restartButton").style.display = "block";
        } else if (gameWon) {
            context.fillStyle = "white";
            context.fillText("Ты выиграл!", boardWidth / 2 - 150, boardHeight / 2);
            document.getElementById("nextLevelButton").style.display = "block";
        }
        return;
    }

    requestAnimationFrame(update);

    context.clearRect(0, 0, board.width, board.height);

    // кораблик
    context.drawImage(shipImg, ship.x, ship.y, ship.width, ship.height);

    // пришельцы
    for (let i = 0; i < alienArray.length; i++) {
        let alien = alienArray[i];
        if (alien.alive) {
            alien.x += alienVelocityX;

            // если пришельцы дошли до края
            if (alien.x + alien.width >= board.width || alien.x <= 0) {
                alienVelocityX *= -1;
                alien.x += alienVelocityX * 2;

                // сместить пришельцев на один ряд вниз
                for (let j = 0; j < alienArray.length; j++) {
                    alienArray[j].y += alienHeight;
                }
            }
            context.drawImage(alienImg, alien.x, alien.y, alien.width, alien.height);

            if (alien.y >= ship.y) {
                gameOver = true;
            }
        }
    }

    // пули
    for (let i = 0; i < bulletArray.length; i++) {
        let bullet = bulletArray[i];
        bullet.y += bulletVelocityY;
        context.fillStyle = "white";
        context.fillRect(bullet.x, bullet.y, bullet.width, bullet.height);

        // столкновение пули и пришельца
        for (let j = 0; j < alienArray.length; j++) {
            let alien = alienArray[j];
            if (!bullet.used && alien.alive && detectCollision(bullet, alien)) {
                bullet.used = true;
                alien.alive = false;
                alienCount--;
                score += 100;
            }
        }
    }

    // чистка пуль
    while (bulletArray.length > 0 && (bulletArray[0].used || bulletArray[0].y < 0)) {
        bulletArray.shift(); // удаляет первый элемент массива
    }

    // переход на новый уровень
    if (alienCount == 0) {
        score += alienColumns * alienRows * 100; // бонусные очки
        alienColumns = Math.min(alienColumns + 1, columns / 2 - 2); // ограничение количества
        alienRows = Math.min(alienRows + 1, rows - 4);  // ограничение количества
        if (alienVelocityX > 0) {
            alienVelocityX += 0.2; // увеличиваем скорость пришельцев вправо
        } else {
            alienVelocityX -= 0.2; // увеличиваем скорость пришельцев влево
        }
        alienArray = [];
        bulletArray = [];
        createAliens();

        // Отображение сообщения о победе
        gameWon = true;
        document.getElementById("nextLevelButton").style.display = "block";
        return;
    }

    // очки
    context.fillStyle = "white";
    context.font = "24px courier";
    context.fillText(score, 5, 20);
}

function moveShip(e) {
    if (gameOver || gameWon) {
        return;
    }

    if (e.code == "ArrowLeft" && ship.x - shipVelocityX >= 0) {
        ship.x -= shipVelocityX; // шаг влево на 1 
    } else if (e.code == "ArrowRight" && ship.x + shipVelocityX + ship.width <= board.width) {
        ship.x += shipVelocityX; // шаг вправо на 1
    }
}

function createAliens() {
    for (let c = 0; c < alienColumns; c++) {
        for (let r = 0; r < alienRows; r++) {
            let alien = {
                img: alienImg,
                x: alienX + c * alienWidth,
                y: alienY + r * alienHeight,
                width: alienWidth,
                height: alienHeight,
                alive: true
            }
            alienArray.push(alien);
        }
    }
    alienCount = alienArray.length;
}

function shoot(e) {
    if (gameOver || gameWon) {
        return;
    }

    if (e.code == "Space") {
        // shoot
        let bullet = {
            x: ship.x + shipWidth * 15 / 32,
            y: ship.y,
            width: tileSize / 8,
            height: tileSize / 2,
            used: false
        }
        bulletArray.push(bullet);
    }
}

function detectCollision(a, b) {
    return a.x < b.x + b.width &&   // верхний левый угол a не достигает верхнего правого угла b
        a.x + a.width > b.x &&   // верхний правый угол игрока a проходит через верхний левый угол игрока b
        a.y < b.y + b.height &&  // левый верхний угол a не достигает левого нижнего угла b
        a.y + a.height > b.y;    // левый нижний угол a проходит левый верхний угол b
}

function nextLevel() {
    gameWon = false;
    document.getElementById("nextLevelButton").style.display = "none";
    requestAnimationFrame(update);
}

function restartGame() {
    gameOver = false;
    document.getElementById("restartButton").style.display = "none";
    score = 0;
    alienRows = 2;
    alienColumns = 3;
    alienVelocityX = 1;
    ship.x = shipX;
    ship.y = shipY;
    alienArray = [];
    bulletArray = [];
    createAliens();
    requestAnimationFrame(update);
}
 