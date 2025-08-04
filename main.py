# Tetris solver
import capture, os, cv2, solver, executeInput, clock, numpy as np
from PIL import Image

def is_cell_filled(imageFile, x1, y1, x2, y2, threshold=100, i=0, j=0):
    """
    Returns True if the cell is filled (not black), False if black.
    Threshold defines how close to black it must be to be considered empty.
    """
    image = cv2.imread(imageFile)
    x1, y1 = round(x1), round(y1)
    x2, y2 = round(x2), round(y2)
    cell = image[y1:y2, x1:x2] 
    avg_color = np.mean(cell, axis=(0, 1))  # average over all pixels 
    distance = np.linalg.norm(avg_color)
    return int(distance > threshold)
firstIter = True
def main():
    """
    Main function to capture the screen, analyze the Tetris grid, and execute the best move.
    """
    global firstIter
    imageFilename = capture.main(firstIter=firstIter)
    firstIter = False
    width, height = Image.open(imageFilename).size
    GridSize = (10, 20)
    CellSize = (width/GridSize[0], height/GridSize[1])
    marginpx = 5

    Grid = []
    ones=0
    for i in range(GridSize[1]):
        Grid.append([])
        for j in range(GridSize[0]):
            x1, y1 = marginpx + j * CellSize[0], marginpx + i * CellSize[1]
            x2, y2 = x1 + CellSize[0] - marginpx, y1 + CellSize[1] - marginpx
            Grid[i].append(is_cell_filled(imageFilename, x1, y1, x2, y2, i=i, j=j))
            if(Grid[i][j]):
                ones+=1
            print(Grid[i][j], end =' ')
        print()
    print(f"Total filled cells: {ones} out of {GridSize[0] * GridSize[1]} ({ones / (GridSize[0] * GridSize[1]) * 100:.2f}%)")

    output = solver.decide_best_move(Grid).split('\n')

    for move in output:
        print(move)
        executeInput.executeCmd(move)

if __name__ == "__main__":
    clk = clock.Clock(1/5)
    while True:
        main()
        clk.waitTillNextTick()
        clk.reset()