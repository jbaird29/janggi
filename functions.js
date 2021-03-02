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

const mirror = (square) => {
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
