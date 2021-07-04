# CheckersAI
This is a checkers game with AI built off of a tutorial by 'Tech With Tim' out of my personal interest, and I encourage people to check out his channel: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg

## The Game

In this checkers game, there were a couple of bugs in the algorithm, namely:
- you could not multi jump into a king piece with the red pieces
- the king could not capture pieces both foward and back in the same turn
- king counter everytime a piece reaches the edge, even if the piece is already a king

Bugs have been fixed

# AI
The AI uses a minimax algorithm and is optimized using alpha beta pruning
