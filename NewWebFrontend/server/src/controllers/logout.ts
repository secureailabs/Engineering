import express from'express';

const router = express.Router();

// -- LogOut -- (destroy session)
router.delete(
    '/logout',
    (req, res) => {
      req.session.destroy(() => res.sendStatus(200));
    }
); export default router;