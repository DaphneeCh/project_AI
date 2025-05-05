"""
moves.py - Implements movement rules for Vietnamese Chess (Cờ Tướng)
This module contains functions to calculate valid moves for each piece type
according to the traditional rules of Vietnamese Chess.
"""
import copy

def get_valid_moves(piece, board):
    """
    Determines all valid moves for a given piece on the current board.
    
    Implements the specific movement rules for each piece type:
    - General: Moves one space in any direction, restricted to the palace. Two Generals cannot face each other directly on the same line. If they do, there must be a piece from either side blocking their view.
    - Advisor: Moves one space diagonally, restricted to the palace.
    - Elephant: Moves diagonally two spaces, cannot cross the river. If there is another piece standing in the middle of that diagonal line, the Elephant is blocked and cannot move.
    - Horse: Move in an 'L' shape, two squares in one direction and one square perpendicular. If there is another piece standing at the intersection adjacent to the vertical or horizontal step, the Horse is blocked and cannot move.
    - Chariot: Moves horizontally or vertically any number of spaces
    - Cannon: Moves like a Chariot but captures by jumping over one piece
    - Soldier: Moves one space forward, can move sideways after crossing the river.
    
    Args:
        piece (Piece): The piece to find moves for
        board (Board): The current game board
        
    Returns:
        list: A list of tuples (x, y) representing valid destination coordinates
    """
    moves = []
    x, y = piece.x, piece.y
    
    if piece.type == 'General':
        # General moves one step horizontally or vertically within the palace
        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 3 <= nx <= 5 and ((0 <= ny <= 2 and piece.color == 'Black') or (7 <= ny <= 9 and piece.color == 'White')):
                target = board.grid[ny][nx] if board.is_in_bounds(nx, ny) else None
                if not target or target.color != piece.color:
                    # Create a temporary board to check if this move would result in facing generals
                    temp_board = copy.deepcopy(board)
                    temp_piece = temp_board.grid[y][x]
                    temp_board.move_piece(temp_piece, nx, ny)
                    if not temp_board.is_general_facing_general():
                        moves.append((nx, ny))
    
    elif piece.type == 'Advisor':
        # Advisor moves diagonally within the palace
        directions = [(1,1), (1,-1), (-1,1), (-1,-1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 3 <= nx <= 5 and ((0 <= ny <= 2 and piece.color == 'Black') or (7 <= ny <= 9 and piece.color == 'White')):
                target = board.grid[ny][nx] if board.is_in_bounds(nx, ny) else None
                if not target or target.color != piece.color:
                    moves.append((nx, ny))
    
    elif piece.type == 'Elephant':
        # Elephant moves exactly two points diagonally and cannot cross the river
        directions = [(2,2), (2,-2), (-2,2), (-2,-2)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Check if the move is within bounds and doesn't cross the river
            if board.is_in_bounds(nx, ny) and ((ny <= 4 and piece.color == 'Black') or (ny >= 5 and piece.color == 'White')):
                # Check if the diagonal path is blocked
                block_x, block_y = x + dx//2, y + dy//2
                if not board.grid[block_y][block_x]:  # Path is clear
                    target = board.grid[ny][nx]
                    if not target or target.color != piece.color:
                        moves.append((nx, ny))
    
    elif piece.type == 'Horse':
        # Horse moves in an L shape: one point horizontally/vertically then one point diagonally
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for dx, dy in directions:
            # First step
            step_x, step_y = x + dx, y + dy
            if board.is_in_bounds(step_x, step_y) and not board.grid[step_y][step_x]:  # No blocking
                # Second step (diagonal)
                diagonals = []
                if dx == 0:  # Vertical first step
                    diagonals = [(1, dy*2), (-1, dy*2)]
                else:  # Horizontal first step
                    diagonals = [(dx*2, 1), (dx*2, -1)]
                
                for nx, ny in diagonals:
                    nx, ny = x + nx, y + ny
                    if board.is_in_bounds(nx, ny):
                        target = board.grid[ny][nx]
                        if not target or target.color != piece.color:
                            moves.append((nx, ny))
    
    elif piece.type == 'Chariot':
        # Chariot moves any distance horizontally or vertically
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while board.is_in_bounds(nx, ny):
                target = board.grid[ny][nx]
                if not target:
                    moves.append((nx, ny))
                else:
                    if target.color != piece.color:
                        moves.append((nx, ny))
                    break
                nx, ny = nx + dx, ny + dy
    
    elif piece.type == 'Cannon':
        # Cannon moves like chariot but needs exactly one piece to jump over for capture
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Moving without capturing
            while board.is_in_bounds(nx, ny) and not board.grid[ny][nx]:
                moves.append((nx, ny))
                nx, ny = nx + dx, ny + dy
            
            # Found a potential platform to jump over
            if board.is_in_bounds(nx, ny):
                platform_x, platform_y = nx, ny
                nx, ny = nx + dx, ny + dy
                # Look for a piece to capture after the platform
                while board.is_in_bounds(nx, ny):
                    target = board.grid[ny][nx]
                    if target:
                        if target.color != piece.color:
                            moves.append((nx, ny))
                        break
                    nx, ny = nx + dx, ny + dy
    
    elif piece.type == 'Soldier':
        # Soldier moves differently based on which side of the river they're on
        directions = []
        
        # Forward direction depends on color
        if piece.color == 'Black':
            directions.append((0, 1))  # Move down
            if y > 4:  # Crossed the river
                directions.extend([(1, 0), (-1, 0)])  # Can move horizontally
        else:  # White
            directions.append((0, -1))  # Move up
            if y < 5:  # Crossed the river
                directions.extend([(1, 0), (-1, 0)])  # Can move horizontally
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if board.is_in_bounds(nx, ny):
                target = board.grid[ny][nx]
                if not target or target.color != piece.color:
                    moves.append((nx, ny))
    
    return moves