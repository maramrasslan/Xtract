// authMiddleware.js
const jwt = require('jsonwebtoken');
const JWT_SECRET = 'your_jwt_secret';

const authMiddleware = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  if (!authHeader) {
    console.error('Authorization header missing');
    return res.status(401).json({ message: 'Unauthorized' });
  }

  const token = authHeader.split(' ')[1];
  if (!token) {
    console.error('Token missing in Authorization header');
    return res.status(401).json({ message: 'Unauthorized' });
  }

  jwt.verify(token, JWT_SECRET, (err, decoded) => {
    if (err) {
      console.error('Token verification failed', err);
      return res.status(401).json({ message: 'Unauthorized' });
    }
    
    req.userId = decoded.userId; // Assuming your JWT payload has userId
    next();
  });
};

module.exports = authMiddleware;
