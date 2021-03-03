// ---------------------------------------------------------------
// Helper functions for altering algebraic square notation
// ---------------------------------------------------------------
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

const mirrorSquare = (square) => {
  if (!['d1', 'f1', 'd3', 'f3', 'd8', 'f8', 'd10', 'f10'].includes(square)) {
    return false
  }
  const letter = square.slice(0,1)
  const num = parseInt(square.slice(1))
  let mirror = ''
  mirror += letter === 'f' ? 'd' : 'f'
  mirror += [1, 8].includes(num) ? (num + 2) : (num - 2)
  return mirror
}

// ---------------------------------------------------------------
// Helper functions for getting certain palaces squares
// ---------------------------------------------------------------
const getPalace = (color=null) => {
  if (color === 'red') {
    return ['d1', 'e1', 'f1', 'd2', 'e2', 'f2', 'd3', 'e3', 'f3']
  } else if (color === 'blue') {
    return ['d8', 'e8', 'f8', 'd9', 'e9', 'f9', 'd10', 'e10', 'f10']
  } else {
    return ['d1', 'e1', 'f1', 'd2', 'e2', 'f2', 'd3', 'e3', 'f3',
    'd8', 'e8', 'f8', 'd9', 'e9', 'f9', 'd10', 'e10', 'f10']
  }
}

const getPalaceCorners = (color=null) => {
  if (color === 'red') {
    return ['d1', 'f1', 'd3', 'f3']
  } else if (color === 'blue') {
    return ['d8', 'f8', 'd10', 'f10']
  } else {
    return ['d1', 'f1', 'd3', 'f3', 'd8', 'f8', 'd10', 'f10']
  }
}

const getPalaceCenters = (color=null) => {
  if (color === 'red') {
    return 'e2'
  } else if (color === 'blue') {
    return 'e9'
  } else {
    return ['e2', 'e9']
  }
}

// ---------------------------------------------------------------
// Helper functions for initializing the game
// ---------------------------------------------------------------
const getStartGameProps = () => {
  const startPieces = [
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
  return {
    pieces: startPieces,
    nextColor: 'blue',
    gameOver: false,
    winner: null
  }
}

const getSavedGameProps = () => {
  const gamePropsJSON = localStorage.getItem('gameProps');
  try {
    return gamePropsJSON ? JSON.parse(gamePropsJSON) : null;
  } catch(e) {
    console.log(e.message);
    return null
  }
}

const getGameProps = () => {
  const savedGameProps = getSavedGameProps()
  if (savedGameProps) {
    // if gameProps were loaded from browser storage, clean the Pieces objects
    let cleanedPieces = []
    savedGameProps.pieces.forEach(piece => {
      cleanedPieces.push(new Piece(piece.color, piece.type, piece.square, piece.isCaptured))
    })
    savedGameProps.pieces = cleanedPieces
    return savedGameProps
  } else {
    // otherwise build an empty game
    return getStartGameProps()
  }
}
