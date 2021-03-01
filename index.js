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

const setUpBoard = () => {
  
  const pieces = {
    'blue-chariot': ['a10', 'i10'],
    'blue-elephant': ['b10', 'g10'],
    'blue-horse': ['c10', 'h10'],
    'blue-guard': ['d10', 'f10'],
    'blue-cannon': ['b8', 'h8'],
    'blue-soldier': ['a7', 'c7', 'e7', 'g7', 'i7'],
    'blue-general': ['e9'],
    'red-chariot': ['a1', 'i1'],
    'red-elephant': ['b1', 'g1'],
    'red-horse': ['c1', 'h1'],
    'red-guard': ['d1', 'f1'],
    'red-cannon': ['b3', 'h3'],
    'red-soldier': ['a4', 'c4', 'e4', 'g4', 'i4'],
    'red-general': ['e2'],
  }

  for (piece in pieces) {
    pieces[piece].forEach((square) => {
      const element = document.createElement('IMG');
      element.setAttribute('src', `images/pieces/${piece}.png`)
      element.classList.add('piece')
      document.querySelector(`#${square}`).appendChild(element)
    })
  }

}

setUpBoard()

class Piece {
  constructor(color, type) {
    this.color = color
    this.type = type
  }
  
}

const savedBoard = {
  'a1': {color: 'red', type: 'chariot'},
  'b1': {color: 'red', type: 'guard'},
  'c1': {color: 'blue', type: 'chariot'},
  'e1': null,
}

const defaultBoard = {
  'a1': new Piece('red', 'chariot'),
  'b1': new Piece('red', 'guard'),
  'c1': new Piece('blue', 'chariot'),
  'e1': null,
  'f1': null,
}


const getSavedBoard = () => {
  // const boardJSON = localStorage.getItem('board');
  const boardJSON = null
  try {
    return boardJSON ? JSON.parse(boardJSON) : null;
  } catch(e) {
    console.log(e.message);
    return null
  }
}

const createBoard = () => {
  let board = getSavedBoard()
  if (board) {
    for (square in board) {
      if (board[square]) {
        board[square] = new Piece(board[square].color, board[square].type)
      }
    }
  } else {
    board = defaultBoard
  }
  return board
}

const board = createBoard()


console.log(createBoard())
