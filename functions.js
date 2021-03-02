class Piece {
  constructor(color, type, square, isCaptured=false) {
    this.color = color
    this.type = type
    this.square = square
    this.isCaptured = isCaptured
  }

  getValidMoves(start, board) {
    switch (this.type) {
      case 'soldier':
        return this.soldierMoves(start, board);
      case 'chariot':
        return this.chariotMoves();
      case 'elephant':
        return this.elephantMoves();
      case 'horse':
        return this.horseMoves();
    }
  }

  soldierMoves(board) {
    const start = this.square
    const squares = []
    // add left, right, and up/down (depending on color)
    const directions = ['right', 'left']
    this.color === 'blue' ? directions.push('up') : directions.push('down')
    for (const direction of directions) {
      const square = shiftDir(start, direction);
      (square && isEmptyOrEnemy(board[square])) ? squares.push(square) : null
    }
    // add palace-specific moves
    if (['d3', 'f3'].includes(start) && isEmptyOrEnemy(board['e2'])) {
      squares.push('e2')
    }
    if (['d8', 'f8'].includes(start) && isEmptyOrEnemy(board['e9'])) {
      squares.push('e9')
    }
    if (start === 'e2') {
      isEmptyOrEnemy(board['d1']) ? squares.push('d1') : null
      isEmptyOrEnemy(board['f1']) ? squares.push('f1') : null
    }
    if (start === 'e9') {
      isEmptyOrEnemy(board['d10']) ? squares.push('d10') : null
      isEmptyOrEnemy(board['f10']) ? squares.push('f10') : null
    }
    return squares
  }


  chariotMoves() {
    return 'chariot'
  }

  elephantMoves() {
    return 'elephant'
  }

  horseMoves() {
    return 'horse'
  }
}

class JanggiGame {
  constructor() {
    this.pieces = this.buildPieces()
    this.board = this.buildBoard()
    this.nextColor = 'blue'
    this.gameOver = false
    this.winner = null
  }

  getPalace(color=null) {
    if (color === 'red') {
      return ['d1', 'e1', 'f1', 'd2', 'e2', 'f2', 'd3', 'e3', 'f3']
    } else if (color === 'blue') {
      return ['d8', 'e8', 'f8', 'd9', 'e9', 'f9', 'd10', 'e10', 'f10']
    } else {
      return ['d1', 'e1', 'f1', 'd2', 'e2', 'f2', 'd3', 'e3', 'f3',
      'd8', 'e8', 'f8', 'd9', 'e9', 'f9', 'd10', 'e10', 'f10']
    }
  }
  
  getPalaceCorners(color=null) {
    if (color === 'red') {
      return ['d1', 'f1', 'd3', 'f3']
    } else if (color === 'blue') {
      return ['d8', 'f8', 'd10', 'f10']
    } else {
      return ['d1', 'f1', 'd3', 'f3', 'd8', 'f8', 'd10', 'f10']
    }
  }
  
  getPalaceCenters(color=null) {
    if (color === 'red') {
      return 'e2'
    } else if (color === 'blue') {
      return 'e9'
    } else {
      return ['e2', 'e9']
    }
  }

  getSavedPieces() {
    // const piecesJSON = localStorage.getItem('pieces');
    const piecesJSON = null
    try {
      return piecesJSON ? JSON.parse(piecesJSON) : null;
    } catch(e) {
      console.log(e.message);
      return null
    }
  }

  buildPieces() {
    let pieces = []
    const savedPieces = this.getSavedPieces()
    if (savedPieces) {
      savedPieces.forEach(piece => {
        pieces.push(new Piece(piece.color, piece.type, piece.square, piece.isCaptured))
      })
    } else {
      pieces = [
        new Piece('red', 'chariot', 'a1'),
        new Piece('red', 'chariot', 'i1'),
        new Piece('red', 'elephant', 'b1'),
        new Piece('red', 'elephant', 'g1'),
        new Piece('red', 'horse', 'c1'),
        new Piece('red', 'horse', 'h1'),
        new Piece('red', 'guard', 'd1'),
        new Piece('red', 'guard', 'f1'),
        new Piece('red', 'cannon', 'b3'),
        new Piece('red', 'cannon', 'h3'),
        new Piece('red', 'soldier', 'a4'),
        new Piece('red', 'soldier', 'c4'),
        new Piece('red', 'soldier', 'e4'),
        new Piece('red', 'soldier', 'g4'),
        new Piece('red', 'soldier', 'i4'),
        new Piece('red', 'general', 'e2'),
        new Piece('blue', 'chariot', 'a10'),
        new Piece('blue', 'chariot', 'i10'),
        new Piece('blue', 'elephant', 'b10'),
        new Piece('blue', 'elephant', 'g10'),
        new Piece('blue', 'horse', 'c10'),
        new Piece('blue', 'horse', 'h10'),
        new Piece('blue', 'guard', 'd10'),
        new Piece('blue', 'guard', 'f10'),
        new Piece('blue', 'cannon', 'b8'),
        new Piece('blue', 'cannon', 'h8'),
        new Piece('blue', 'soldier', 'a7'),
        new Piece('blue', 'soldier', 'c7'),
        new Piece('blue', 'soldier', 'e7'),
        new Piece('blue', 'soldier', 'g7'),
        new Piece('blue', 'soldier', 'i7'),
        new Piece('blue', 'general', 'e9'),
      ]
    }
    return pieces
  }

  buildEmpytyBoard() {
    let board = {}
    let letter = 'a'
    let num = 1
    while (letter <= 'i') {
      while (num <= 10) {
        board[letter+num] = null
        num += 1
      }
      num = 1
      letter = nextChar(letter)
    }
    return board
  }

  buildBoard() {
    let board = this.buildEmpytyBoard()
    this.pieces.forEach(piece => {
      board[piece.square] = piece
    })
    return board
  }

  renderPieces() {
    for (const square in this.board) {
      const piece = this.board[square]
      const squareEl = document.getElementById(square)
      const pieceEl = squareEl.childNodes[1]
      pieceEl && squareEl.removeChild(pieceEl)  // remove the prior element
      if (piece && !piece.isCaptured) {
        const img = document.createElement('IMG');
        img.setAttribute('src', `images/pieces/${piece.color}-${piece.type}.png`)
        img.classList.add('piece')
        document.querySelector(`#${square}`).appendChild(img)  
      }
    }
  }

  // renderPieces() {
  //   this.pieces.forEach(piece => {
  //     if (!piece.isCaptured) {
  //       const img = document.createElement('IMG');
  //       img.setAttribute('src', `images/pieces/${piece.color}-${piece.type}.png`)
  //       img.classList.add('piece')
  //       document.querySelector(`#${piece.square}`).appendChild(img)  
  //     }
  //   })
  // } 

  makeMove(start, end) {
    const startPiece = this.board[start]
    const endPiece = this.board[end]
    if (this.gameOver) {
      return {valid: false, response: `Game is already over.`}
    } else if (!startPiece) {
      return {valid: false, response: `There is no piece there.`}
    } else if (startPiece.color !== this.nextColor) {
      return {valid: false, response: `That piece does not belong to you.`}
    } else if (!startPiece.getValidMoves(this.board).includes(end)) {
      return {valid: false, response: `Not a valid end position for that piece.`}
    }
    if (endPiece && endPiece !== startPiece) {
      endPiece.isCaptured = true
      endPiece.square = null
    }
    startPiece.square = end
    this.board[start] = null
    this.board[end] = startPiece
    this.nextColor = this.nextColor === 'red' ? 'blue' : 'red'
    return {valid: true, response: `Next turn: ${this.nextColor}`}
  }

}

const nextChar = (c) => { 
  return String.fromCharCode(c.charCodeAt(0) + 1); 
}

const shift = (square, vertical, horizontal) => {
  const startLet = square.slice(0,1)
  const startNum = square.slice(1)
  const startOrd = startLet.charCodeAt(0)
  if (!(startLet >= 'a' && startLet <= 'i' && startNum >= 1 && startNum <= 10)) {
    return false
  }
  const endNum = startNum - vertical
  const endOrd = startOrd + horizontal
  const endLet = String.fromCharCode(endOrd)
  if (!(endLet >= 'a' && endLet <= 'i' && endNum >= 1 && endNum <= 10)) {
    return false
  }
  return endLet + endNum
}

const shiftDir = (square, direction) => {
  if (direction === 'right') return shift(square, 0, 1);
  if (direction === 'left') return shift(square, 0, -1);
  if (direction === 'up') return shift(square, 1, 0);
  if (direction === 'down') return shift(square, -1, 0);
}

const isEmptyOrEnemy = (potentialPiece) => {
  return (potentialPiece === null || potentialPiece.color !== this.color)
}