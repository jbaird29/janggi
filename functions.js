class Piece {
  constructor(color, type, square, isCaptured=false) {
    this.color = color
    this.type = type
    this.square = square
    this.isCaptured = isCaptured
  }

  getValidMoves() {
    switch (this.type) {
      case 'chariot':
        return this.chariotMoves();
      case 'elephant':
        return this.elephantMoves();
        case 'horse':
          return this.horseMoves();
    }
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
    this.pieces.forEach(piece => {
      const img = document.createElement('IMG');
      img.setAttribute('src', `images/pieces/${piece.color}-${piece.type}.png`)
      img.classList.add('piece')
      document.querySelector(`#${piece.square}`).appendChild(img)
    })
  } 

}

function nextChar(c) { 
  return String.fromCharCode(c.charCodeAt(0) + 1); 
}

