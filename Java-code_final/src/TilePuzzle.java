import java.util.ArrayList;
import java.util.Collections;

public class TilePuzzle {

    private int n = 3;

    private final int[][] goal = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 0}
    };

    private class Node {
        int[][] state;
        Node parent;
        String move;
        int g_n;
        int h_n;
        int f_n;

        Node(int[][] state, Node parent, String move, int g_n, int h_n, int f_n) {
            this.state = state;
            this.parent = parent;
            this.move = move;
            this.g_n = g_n;
            this.h_n = h_n;
            this.f_n = f_n;
        }
    }

    private int h1(int[][] state) {
        int heuristic = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (state[i][j] != 0 && state[i][j] != goal[i][j])
                    heuristic++;
            }
        }
        return heuristic;
    }

    private int h2(int[][] state) {
        int heuristic = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {

                if (state[i][j] == 0) continue;

                boolean isInRow = false;
                boolean isInCol = false;
                for (int k = 0; k < n; k++) {
                    if (goal[i][k] == state[i][j])
                        isInRow = true;
                    if (goal[k][j] == state[i][j])
                        isInCol = true;
                }
                if (!isInRow)
                    heuristic++;
                if (!isInCol)
                    heuristic++;
            }
        }
        return heuristic;
    }

    private int heuristic(int[][] state, int heuristicChoice) {
        if (heuristicChoice == 1)
            return h1(state);

        return h2(state);
    }

    private int[] findBlank(int[][] state) {
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (state[i][j] == 0)
                    return new int[]{i, j};

        return new int[]{-1, -1};
    }

    private int[][] copyBoard(int[][] state) {
        int[][] copy = new int[n][n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                copy[i][j] = state[i][j];
        return copy;
    }

    private boolean isGoal(int[][] state) {
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (state[i][j] != goal[i][j])
                    return false;
        return true;
    }

    private int[][] moveUp(int[][] state) {
        int[][] copy = copyBoard(state);
        int[] blank = findBlank(copy);
        int positionI = blank[0];
        int positionJ = blank[1];
        if (positionI > 0) {
            int temp = copy[positionI][positionJ];
            copy[positionI][positionJ] = copy[positionI - 1][positionJ];
            copy[positionI - 1][positionJ] = temp;
            return copy;
        }

        return null;
    }

    private int[][] moveDown(int[][] state) {
        int[][] copy = copyBoard(state);
        int[] blank = findBlank(copy);
        int positionI = blank[0];
        int positionJ = blank[1];
        if (positionI < n - 1) {
            int temp = copy[positionI][positionJ];
            copy[positionI][positionJ] = copy[positionI + 1][positionJ];
            copy[positionI + 1][positionJ] = temp;
            return copy;
        }

        return null;
    }

    private int[][] moveLeft(int[][] state) {
        int[][] copy = copyBoard(state);
        int[] blank = findBlank(copy);
        int positionI = blank[0];
        int positionJ = blank[1];
        if (positionJ > 0) {
            int temp = copy[positionI][positionJ];
            copy[positionI][positionJ] = copy[positionI][positionJ - 1];
            copy[positionI][positionJ - 1] = temp;
            return copy;
        }

        return null;
    }

    private int[][] moveRight(int[][] state) {
        int[][] copy = copyBoard(state);
        int[] blank = findBlank(copy);
        int positionI = blank[0];
        int positionJ = blank[1];
        if (positionJ < n - 1) {
            int temp = copy[positionI][positionJ];
            copy[positionI][positionJ] = copy[positionI][positionJ + 1];
            copy[positionI][positionJ + 1] = temp;
            return copy;
        }

        return null;
    }

    private int lowestFrontierGreedyIndex(ArrayList<Node> frontier) {
        int lowestHeuristicIndex = 0;
        for (int i = 1; i < frontier.size(); i++) {
            if (frontier.get(i).h_n < frontier.get(lowestHeuristicIndex).h_n)
                lowestHeuristicIndex = i;
        }
        return lowestHeuristicIndex;
    }

    private int lowestAStarIndex(ArrayList<Node> frontier) {
        int lowestFunctionIndex = 0;
        for (int i = 1; i < frontier.size(); i++) {
            if (frontier.get(i).f_n < frontier.get(lowestFunctionIndex).f_n)
                lowestFunctionIndex = i;
        }
        return lowestFunctionIndex;
    }


    private ArrayList<Node> successors(Node node, int heuristicChoice) {
        ArrayList<Node> successorNodes = new ArrayList<Node>();
        int h_nNext;
        int g_nNext = node.g_n + 1;


        int[][] movedUpBoard = moveUp(node.state);
        if (movedUpBoard != null) {
            h_nNext = heuristic(movedUpBoard, heuristicChoice);
            successorNodes.add(new Node(movedUpBoard, node, "Up", g_nNext, h_nNext, h_nNext + g_nNext));
        }

        int[][] movedDownBoard = moveDown(node.state);
        if (movedDownBoard != null) {
            h_nNext = heuristic(movedDownBoard, heuristicChoice);
            successorNodes.add(new Node(movedDownBoard, node, "down", g_nNext, h_nNext, h_nNext + g_nNext));
        }

        int[][] movedLeftBoard = moveLeft(node.state);
        if (movedLeftBoard != null) {
            h_nNext = heuristic(movedLeftBoard, heuristicChoice);
            successorNodes.add(new Node(movedLeftBoard, node, "left", g_nNext, h_nNext, h_nNext + g_nNext));
        }

        int[][] movedRightBoard = moveRight(node.state);
        if (movedRightBoard != null) {
            h_nNext = heuristic(movedRightBoard, heuristicChoice);
            successorNodes.add(new Node(movedRightBoard, node, "right", g_nNext, h_nNext, h_nNext + g_nNext));
        }

        return successorNodes;

    }

    private void printSolution(Node goalNode) {
        ArrayList<Node> path = new ArrayList<Node>();

        for (Node node = goalNode; node != null; node = node.parent)
            path.add(node);
        Collections.reverse(path);

        System.out.println("Solution");
        System.out.println("number of actions:" + (path.size() - 1));

        for (int i = 1; i < path.size(); i++) {
            System.out.println("Step " + i + ": ");
            printBoard(path.get(i).state);
            System.out.println();
        }

    }

    private void printBoard(int[][] state) {
        for (int i = 0; i < n; i++) {
            System.out.println("\n");
            for (int j = 0; j < n; j++) {
                System.out.print(state[i][j] + " ");
            }
        }
    }


    public void greedyFirstSearch(int[][] start, int heuristicChoice) {
        ArrayList<Node> frontier = new ArrayList<>();
        ArrayList<Node> expanded = new ArrayList<>();

        int h_n = heuristic(start, heuristicChoice);
        frontier.add(new Node(copyBoard(start), null, null, 0, h_n, h_n));

        while (!frontier.isEmpty()) {
            int index = lowestFrontierGreedyIndex(frontier);
            Node node = frontier.remove(index);

            if (isGoal(node.state)) {
                printSolution(node);
                return;
            }

            if (expanded.contains(node))
                continue;

            expanded.add(node);

            ArrayList<Node> successorNodes = successors(node, heuristicChoice);
            for (int i = 0; i < successorNodes.size(); i++) {
                Node successorNode = successorNodes.get(i);
                if (!expanded.contains(successorNode))
                    frontier.add(successorNode);
            }
        }
    }

    public void aStarSearch(int[][] start, int heuristicChoice) {
        ArrayList<Node> frontier = new ArrayList<>();

        int h_n = heuristic(start, heuristicChoice);
        frontier.add(new Node(copyBoard(start), null, null, 0, h_n, h_n));

        while (!frontier.isEmpty()) {
            int index = lowestAStarIndex(frontier);
            Node node = frontier.remove(index);

            if (isGoal(node.state)) {
                printSolution(node);
                return;
            }
            ArrayList<Node> successorNodes = successors(node, heuristicChoice);
            for (int i = 0; i < successorNodes.size(); i++) {
                continue;
                }
            }
        }



    }

