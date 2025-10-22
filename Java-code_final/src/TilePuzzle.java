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
            for(int j = 0; j < n; j++) {
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



}