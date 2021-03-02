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
  
    /**
     * Renders all the pieces based on the board state
     */
    clearPieces() {
      for (const square in this.board) {
        const squareEl = document.getElementById(square)
        const pieceEl = squareEl.childNodes[1]
        pieceEl && squareEl.removeChild(pieceEl)  // if there is a piece img, remove it
      }
    }

    clearCapturedPieces() {
      const redCapturedEl = document.getElementById('captured-pieces-red');
      const blueCapturedEl = document.getElementById('captured-pieces-blue');
      // must loop backward through nodeList; it live-updates
      for (let i = redCapturedEl.childNodes.length - 1; i >= 0; i--) {
        const childEl = redCapturedEl.childNodes[i]
        if (childEl.classList.contains('piece')) {
          redCapturedEl.removeChild(childEl)
        }
      }
      for (let i = blueCapturedEl.childNodes.length - 1; i >= 0; i--) {
        const childEl = blueCapturedEl.childNodes[i]
        if (childEl.classList.contains('piece')) {
          blueCapturedEl.removeChild(childEl)
        }
      }
    }

    renderPieces() {
      const pieces = this.pieces.filter(piece => !piece.isCaptured)
      pieces.forEach(piece => {
        const img = document.createElement('IMG');
        img.setAttribute('src', `images/pieces/${piece.color}-${piece.type}.png`)
        img.classList.add('piece')
        document.getElementById(`${piece.square}`).appendChild(img)  
      })
    }

    renderCapturedPieces() {
      const capturedPieces = this.pieces.filter(piece => piece.isCaptured)
      capturedPieces.forEach(piece => {
        const img = document.createElement('IMG');
        img.setAttribute('src', `images/pieces/${piece.color}-${piece.type}.png`)
        img.classList.add('piece', 'piece-captured')
        document.getElementById(`captured-pieces-${piece.color}`).appendChild(img)  
      })
    }

    renderGame() {
      this.clearPieces();
      this.clearCapturedPieces();
      this.renderPieces();
      this.renderCapturedPieces();
    }

    /**
     * Given a piece, highlights 'valid move' squares with a shading
     * @param {Piece} piece 
     */
    renderSquareShading(piece) {
      const validMoves = this.getValidMoves(piece)
      validMoves.forEach(square => {
        const squareEl = document.getElementById(square)
        const imageEl = squareEl.childNodes[0]
        imageEl.classList.add('square-img-highlight')
      })
      const squareEl = document.getElementById(piece.square)
      const pieceImageEl = squareEl.childNodes[1]
      pieceImageEl.classList.add('piece-highlight')
    }

    /**
     * Clears the shading of 'valid move' sauares
     */
    clearSquareShading(piece) {
      for (const square in this.board) { 
        const squareEl = document.getElementById(square)
        const imgageEl = squareEl.childNodes[0]
        imgageEl.classList.remove('square-img-highlight')
      }
      const squareEl = document.getElementById(piece.square)
      const pieceImageEl = squareEl.childNodes[1]
      pieceImageEl.classList.remove('piece-highlight')
    }
    
    /**
     * Given a color, returns the square of that color's general
     * @param {string} color 
     */
    getGeneralSquare(color) {
      return this.pieces.find(piece => piece.type === 'general' && piece.color === color).square
    }

    /**
     * Given a square, returns the piece at that square or null if empty
     * @param {string} square 
     */
    getPiece(square) {
      return this.board[square]
    }

    /**
     * Given a start and end square, returns true if the two squares contain pieces of the same color; otherwise false
     * @param {string} start 
     * @param {string} end 
     */
    areSameColor(start, end) {
      const startPiece = this.getPiece(start)
      const endPiece = this.getPiece(end)
      if (startPiece && endPiece && startPiece.color === endPiece.color) {
        return true
      } else {
        return false
      }
    }

    /**
     * Given a color, determines if that color is in check; returns true or false
     * @param {string} color 
     */
    isInCheck(color) {
      const generalSquare = this.getGeneralSquare(color)
      const opposingColor = color === 'blue' ? 'red' : 'blue'
      const pieces = this.pieces.filter(piece => piece.color === opposingColor && !piece.isCaptured)
      // # iterate through the board; see if any opposing color’s pieces could validly capture the given color's general
      for (const piece of pieces) {
        const canCaptureGeneral = piece.getValidMovements(this.board).includes(generalSquare)
        if (canCaptureGeneral) {
          return true
        }
      }
      // # if loop had ended with no True condition, return False
      return false
    }

    /**
     * Given a color, determines if that color is in checkmate; returns true or false
     * @param {string} color 
     */
    isInCheckmate(color) {
      // get array of pieces which are of the same color and not captured
      const pieces = this.pieces.filter(piece => piece.color === color && !piece.isCaptured)
      // iterate through each of this color's pieces and see if there is a validMove
      for (const piece of pieces) {
        if (this.getValidMoves(piece).length > 0) {
          return false  // if a valid move was found, it is not checkmate
        }
      }
      return true  // if no valid move was found, it is checkmate
    }

    /**
     * Moves the startPiece (located at start) to end (which may or may not contain endPiece); updates board & state
     * @param {string} start 
     * @param {string} end 
     * @param {Piece} startPiece 
     * @param {Piece || null} endPiece 
     */
    performMove(start, end, startPiece, endPiece) {
      if (endPiece && endPiece !== startPiece) {
        endPiece.isCaptured = true
        endPiece.square = null
      }
      startPiece.square = end
      this.board[start] = null
      this.board[end] = startPiece
    }

    /**
     * REVERSES move of startPiece (located at start) to end (which may or may not contain endPiece); updates board & state
     * @param {string} start 
     * @param {string} end 
     * @param {Piece} startPiece 
     * @param {Piece || null} endPiece 
     */
    reverseMove(start, end, startPiece, endPiece) {
      this.board[end] = endPiece
      this.board[start] = startPiece
      startPiece.square = start
      if (endPiece && endPiece !== startPiece) {
        endPiece.isCaptured = false
        endPiece.square = end
      }
    }
  
    /**
     * Given a piece, returns an array of all valid end positions for that piece
     * @param {Piece} piece 
     */
    getValidMoves(piece) {
      const validMovements = piece.getValidMovements(this.board)
      const validMoves = []
      for (const end of validMovements) {
        const start = piece.square
        const endPiece = this.board[end]
        this.performMove(start, end, piece, endPiece)  // attempt the move
        if (!this.isInCheck(piece.color)) {
          validMoves.push(end)  // valid if player is not left in check
        }
        this.reverseMove(start, end, piece, endPiece)  // revere the move
      }
      return validMoves
    }

    /**
     * Given a start sqaure, determines if that is a valid start square based on board / game state
     * @param {string} start 
     */
    isValidStart(start) {
      const startPiece = this.board[start]
      if (this.gameOver) {
        return {valid: false, response: `Game is already over.`}
      } else if (!startPiece) {
        return {valid: false, response: `Invalid: There is no piece there.`}
      } else if (startPiece.color !== this.nextColor) {
        return {valid: false, response: `Invalid: That piece does not belong to you.`}
      } else {
        return {valid: true, response: `Start square is ${start}. Select end square.`}
      }
    }
    /**
     * Given a start and end square, determines if that move is valid and updates board / game state if so
     * returns an object of {valid: true || false, response: 'response text message'}
     * @param {string} start 
     * @param {string} end 
     */
    makeMove(start, end) {
      try {
        const startPiece = this.board[start]
        const endPiece = this.board[end]
        // determine if the move is falid
        if (this.gameOver) {
          return {valid: false, response: `Game is already over.`}
        } else if (!startPiece) {
          return {valid: false, response: `Invalid: There is no piece there.`}
        } else if (startPiece.color !== this.nextColor) {
          return {valid: false, response: `Invalid: That piece does not belong to you.`}
        } else if (!this.getValidMoves(startPiece).includes(end)) {
          return {valid: false, response: `Invalid: not a valid end position for that piece.`}
        }
        // if valid, update the board and game state
        this.performMove(start, end, startPiece, endPiece)
        this.nextColor = this.nextColor === 'red' ? 'blue' : 'red'
        // if current player is in check, determine if checkmate occurred, update game state if so
        if (this.isInCheck(this.nextColor)) {
          if (this.isInCheckmate(this.nextColor)) {
            this.gameOver = true
            this.winner = this.nextColor === 'red' ? 'blue' : 'red'
            return {valid: true, response: `Game over: ${this.winner} wins.`}
          }
        }
        // otherwise return valid response
        return {valid: true, response: `Next turn: ${this.nextColor}`}
      } catch(e) {
        console.log(e)
        return {valid: false, response: `There was an error.`}
      }
    }
  }
  