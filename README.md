# CheckersAI
This is a checkers game with AI built off of a tutorial by 'Tech With Tim' out of my personal interest, and I encourage people to check out his channel: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg

## The Game
It's just a normal checkers game.

## Bugs
In the original tutorial/code, I found a couple of bugs, namely:
- you could not multi-jump into a king piece with the red pieces
- the king could not capture pieces both foward and back in the same turn
- king counter everytime a piece reaches the edge, even if the piece is already a king

I have fixed the bugs mentioned by re-writing the algorithms and code related to the issues. If you find more bugs, please let me know. 

## AI
The original project implements the minimax algorithm to support AI decisions, and I have added on to it by optimizing the AI using alpha beta pruning.
