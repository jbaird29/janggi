const moveEl = document.querySelector('#current-move')

let game = new JanggiGame(getGameProps())
game.renderGame()
moveEl.innerHTML = game.getHeaderText()

let start = null;
let end = null;

document.querySelectorAll('.square').forEach(square => {
  square.addEventListener('click', (e) => {
    const square = e.target.parentElement.id;
    if (!start && !end) {
      const {valid, response} = game.isValidStart(square)
      moveEl.innerHTML = `${response}`;
      if (valid) {
        start = square;
        game.renderSquareShading(game.getPiece(start))
      } else {
        start = null;  
      }
    } else if (start && !end) {
      game.clearSquareShading(game.getPiece(start))
      end = square;
      // short circuit - if the end contains a piece of the same color, change that to the new start
      if (game.areSameColor(start, end)) {
        start = end;
        end = null;
        game.renderSquareShading(game.getPiece(start))
      } else {
        const {valid, response} = game.makeMove(start, end)
        moveEl.innerHTML = `${response}`;
        start = null;
        end = null;  
        if (valid) {
          game.renderGame();
        } 
      }
    }
  })
})

document.getElementById('pass-btn').addEventListener('click', (e) => {
  if (start) {
    game.clearSquareShading(game.getPiece(start))
  }
  const {valid, response} = game.makeMove(start=null, end=null, pass=true);
  moveEl.innerHTML = `${response}`;
  start = null;
  end = null;
  game.renderGame();
})

document.getElementById('reset-btn').addEventListener('click', (e) => {
  if (start) {
    game.clearSquareShading(game.getPiece(start))
  }
  game = new JanggiGame(getStartGameProps())
  game.saveGave()
  game.renderGame()
  moveEl.innerHTML = game.getHeaderText()
})
