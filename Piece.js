class Piece {
  constructor(color, type, square, isCaptured=false) {
    this.color = color
    this.type = type
    this.square = square
    this.isCaptured = isCaptured
  }

  isEmptyOrEnemy(potentialPiece) {
    return (potentialPiece === null || potentialPiece.color !== this.color)
  }

  getValidMoves(board) {
    switch (this.type) {
      case 'soldier':
        return this.soldierMoves(board);
      case 'cannon':
        return this.cannonMoves(board)
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
    const moves = []
    // add left, right, and up/down (depending on color)
    const directions = ['right', 'left']
    this.color === 'blue' ? directions.push('up') : directions.push('down')
    for (const direction of directions) {
      const square = shiftDir(start, direction);
      (square && this.isEmptyOrEnemy(board[square])) ? moves.push(square) : null
    }
    // add palace-specific moves
    if (['d3', 'f3'].includes(start) && this.isEmptyOrEnemy(board['e2'])) {
      moves.push('e2')
    }
    if (['d8', 'f8'].includes(start) && this.isEmptyOrEnemy(board['e9'])) {
      moves.push('e9')
    }
    if (start === 'e2') {
      this.isEmptyOrEnemy(board['d1']) ? moves.push('d1') : null
      this.isEmptyOrEnemy(board['f1']) ? moves.push('f1') : null
    }
    if (start === 'e9') {
      this.isEmptyOrEnemy(board['d10']) ? moves.push('d10') : null
      this.isEmptyOrEnemy(board['f10']) ? moves.push('f10') : null
    }
    return moves
  }

  cannonMoves(board) {
    const start = this.square
    const moves = []
    // add the right, left, up, down axes
    for (const direction of ['up', 'right', 'down', 'left']) {
      let pieceCount = 0
      let containsCannon = false
      let square = shiftDir(start, direction)  // shift the square by 1 in the given direction
      while (square && pieceCount < 2 && !containsCannon) {
        const piece = board[square]
        if (pieceCount === 1 && piece === null) {
          moves.push(square)  // append if empty
        } else if (pieceCount === 1 && piece.color !== this.color && piece.type !== 'cannon') {
          moves.push(square)  // append if it contains opposing piece that is not a cannon
        }
        if (piece !== null) {
          pieceCount += 1
          containsCannon = piece.type === 'cannon'
        }
        square = shiftDir(square, direction)  // do another shift
      }
    }
    // if in the palace corners, check on adding the 'mirror' across diagonal
    if (getPalaceCorners().includes(start)) {
      const squareColor = getPalaceCorners('red').includes(start) ? 'red' : 'blue'
      const center = getPalaceCenters(squareColor)
      const mirror = mirror(start)
      const centerIsCannon = board[center] !== null && board[center].type === 'cannon'
      const mirrorIsCannon = board[mirror] !== null && board[mirror].type === 'cannon'
      if (!centerIsCannon && !mirrorIsCannon) {
        if (board[center] !== null && self.isEmptyOrEnemy(board[mirror])) {
          moves.push(mirror)
        }
      }
    }
    return moves
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
