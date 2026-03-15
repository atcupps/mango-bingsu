#[derive(Debug, PartialEq, Clone, Copy)]
pub enum PieceType {
    Rook,
    Knight,
    Bishop,
    King,
    Queen,
    WhitePawn,
    BlackPawn
}

pub struct Piece {
    pub piece_type: PieceType,
    pub bits: u64,
}

impl Piece {
    pub fn new(piece_type: PieceType, rank: u8, file: u8) -> Piece {
        Piece {
            piece_type,
            bits: rf_to_bits(rank, file)
        }
    }
}

pub struct Board {
    pub white_pieces: [Piece; 16],
    pub black_pieces: [Piece; 16]
}

impl Board {
    pub fn new() -> Self {
        Board {
            white_pieces: [
                Piece::new(PieceType::Rook, 0, 0),
                Piece::new(PieceType::Knight, 0, 1),
                Piece::new(PieceType::Bishop, 0, 2),
                Piece::new(PieceType::King, 0, 3),
                Piece::new(PieceType::Queen, 0, 4),
                Piece::new(PieceType::Bishop, 0, 5),
                Piece::new(PieceType::Knight, 0, 6),
                Piece::new(PieceType::Rook, 0, 7),
                Piece::new(PieceType::WhitePawn, 1, 0),
                Piece::new(PieceType::WhitePawn, 1, 1),
                Piece::new(PieceType::WhitePawn, 1, 2),
                Piece::new(PieceType::WhitePawn, 1, 3),
                Piece::new(PieceType::WhitePawn, 1, 4),
                Piece::new(PieceType::WhitePawn, 1, 5),
                Piece::new(PieceType::WhitePawn, 1, 6),
                Piece::new(PieceType::WhitePawn, 1, 7),
            ],
            black_pieces: [
                Piece::new(PieceType::Rook, 7, 0),
                Piece::new(PieceType::Knight, 7, 1),
                Piece::new(PieceType::Bishop, 7, 2),
                Piece::new(PieceType::King, 7, 3),
                Piece::new(PieceType::Queen, 7, 4),
                Piece::new(PieceType::Bishop, 7, 5),
                Piece::new(PieceType::Knight, 7, 6),
                Piece::new(PieceType::Rook, 7, 7),
                Piece::new(PieceType::BlackPawn, 6, 0),
                Piece::new(PieceType::BlackPawn, 6, 1),
                Piece::new(PieceType::BlackPawn, 6, 2),
                Piece::new(PieceType::BlackPawn, 6, 3),
                Piece::new(PieceType::BlackPawn, 6, 4),
                Piece::new(PieceType::BlackPawn, 6, 5),
                Piece::new(PieceType::BlackPawn, 6, 6),
                Piece::new(PieceType::BlackPawn, 6, 7),
            ],
        }
    }
}

pub fn rf_to_bits(rank: u8, file: u8) -> u64 {
    1 << (rank * 8 + file)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rf_to_bits() {
        assert_eq!(rf_to_bits(0, 0), 1);
        assert_eq!(rf_to_bits(0, 7), 1 << 7);
        assert_eq!(rf_to_bits(1, 0), 1 << 8);
        assert_eq!(rf_to_bits(7, 7), 1 << 63);
    }

    #[test]
    fn test_board_initial_positions() {
        let board = Board::new();
        
        // Check white pieces (rank 0 and 1)
        for i in 0..8 {
            assert_eq!(board.white_pieces[i].bits, rf_to_bits(0, i as u8));
        }
        for i in 8..16 {
            assert_eq!(board.white_pieces[i].bits, rf_to_bits(1, (i - 8) as u8));
        }

        // Check black pieces (rank 6 and 7)
        for i in 0..8 {
            assert_eq!(board.black_pieces[i].bits, rf_to_bits(7, i as u8));
        }
        for i in 8..16 {
            assert_eq!(board.black_pieces[i].bits, rf_to_bits(6, (i - 8) as u8));
        }
    }
}
