const moveEl = document.querySelector('#current-move')
moveEl.textContent = 'Select start square'

let start = null;
let end = null;

document.querySelectorAll('.square').forEach(square => {
  square.addEventListener('click', (e) => {
    const square = e.target.parentElement.id;
    if (!start && !end) {
      start = square;
      moveEl.textContent = `Start square is ${square}. Select end square.`;
    } else if (!end) {
      end = square;
      result = makeMove(start, end)
      if (result) {
        moveEl.textContent = `Move successful. Select start square.`;
      } else {
        moveEl.textContent = `Move invalid. Try again.`;
      }
      start = null;
      end = null;
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
game.renderPieces()
console.log(game.board)
console.log(game.board['a1'].getValidMoves())