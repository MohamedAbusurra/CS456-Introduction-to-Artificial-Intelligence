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



}