class JanggiGame {
  constructor() {
    this.pieces = this.buildPieces()
    this.board = this.buildBoard()
    this.nextColor = 'blue'
    this.gameOver = false
    this.winner = null
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

  clearSquareShading() {
    for (const square in this.board) { 
      const squareEl = document.getElementById(square)
      const imgageEl = squareEl.childNodes[0]
      imgageEl.classList.remove('square-img-highlight')
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
    try {
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
    } catch(e) {
      console.log(e)
      return {valid: false, response: `There was an error.`}
    }
  }
}
