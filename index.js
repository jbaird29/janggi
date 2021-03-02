const moveEl = document.querySelector('#current-move')

moveEl.textContent = 'Next turn: blue. Select start square'
let game = new JanggiGame()
game.renderGame()

let start = null;
let end = null;

document.querySelectorAll('.square').forEach(square => {
  square.addEventListener('click', (e) => {
    const square = e.target.parentElement.id;
    if (!start && !end) {
      const {valid, response} = game.isValidStart(square)
      moveEl.textContent = `${response}`;
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
        moveEl.textContent = `${response}`;
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
  moveEl.textContent = `${response}`;
  start = null;
  end = null;
  game.renderGame();
})

document.getElementById('reset-btn').addEventListener('click', (e) => {
  if (start) {
    game.clearSquareShading(game.getPiece(start))
  }
  moveEl.textContent = 'Next turn: blue. Select start square'
  game = new JanggiGame()
  game.renderGame()
})
