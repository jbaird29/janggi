const moveEl = document.querySelector('#current-move')
moveEl.textContent = 'Select start square'

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
          game.renderGame()
        } 
      }
    }
  })
})


const makeMove = (start, end) => {
  const startPiece = document.getElementById(start).childNodes[1]
  const endPiece = document.getElementById(end).childNodes[1]
  if (!startPiece) {
    return false
  }
  document.getElementById(start).removeChild(startPiece);
  if (endPiece) {
    document.getElementById(end).removeChild(endPiece);
  }
  document.getElementById(end).appendChild(startPiece)
  return true
}

const game = new JanggiGame()
game.renderGame()
