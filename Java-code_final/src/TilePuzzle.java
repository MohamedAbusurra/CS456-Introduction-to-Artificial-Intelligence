import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;

public class TilePuzzle {

    private int n = 3;

    private final int[][] goal = {
            {0, 1, 2},
            {3, 4, 5},
            {6, 7, 8}
    };

    //Store key information required in the search in a node class that will be initalized
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

        /*Overrided equals and hashcode so when two nodes are compared or node is checked to
        see if contained by its configuration (arraylist,hashmap) in a data structure in GFS and A* does not compare
         objects but 2d array of board configuration */
        @Override
        public boolean equals(Object obj) {
            Node node = (Node) obj;
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    if (state[i][j] != node.state[i][j])
                        return false;
                }
            }
            return true;
        }

        @Override
        public int hashCode(){
            int hash = 7; // start from a nonzero constant
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    hash = 31 * hash + state[i][j];
                }
            }
            return hash;
        }


    }
    //loops around entire board state configuration with a counter adding how many misplaced
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

    // loops to see number of tiles not in correct row plus number of tiles not in correct column and returns sum
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

    /* Used as a cleaner implementation of which heuristic was chosen for the search with the heuristic being returned of given
    state and */
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

    /*copies 2d board tile configuration because 2d arrays are sent as by reference
     automatically and for altering tile configuration for creating successor states
     it does not want to alter the original
     */
    private int[][] copyBoard(int[][] state) {
        int[][] copy = new int[n][n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                copy[i][j] = state[i][j];
        return copy;
    }


    //checks if current board configuration state is the goal state
    private boolean isGoal(int[][] state) {
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                if (state[i][j] != goal[i][j])
                    return false;
        return true;
    }

    private int[][] moveUp(int[][] state) {
        /* gets blank tile i and j position and alters it in a copy board and returns
        new board configuration with blank tile moved up if possible
         */
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
        /*if null is returned, move up is not possible and condition operators use null comparison to ensure frontier
        is appended incorrectly
         */
        return null;
    }

    private int[][] moveDown(int[][] state) {
        /* gets blank tile i and j position and alters it in a copy board and returns
        new board configuration with blank tile moved down if possible
         */
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
        /* gets blank tile i and j position and alters it in a copy board and returns
        new board configuration with blank tile moved left if possible
         */
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
        /* gets blank tile i and j position and alters it in a copy board and returns
        new board configuration with blank tile moved right if possible
         */
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
        //traverses frontier arrayList and returns index of board in frontier with the lowest heuristic function (h(n))
        int lowestHeuristicIndex = 0;
        for (int i = 1; i < frontier.size(); i++) {
            if (frontier.get(i).h_n < frontier.get(lowestHeuristicIndex).h_n)
                lowestHeuristicIndex = i;
        }
        return lowestHeuristicIndex;
    }

    private int lowestAStarIndex(ArrayList<Node> frontier) {
        //traverses frontier arrayList and returns index of board in frontier with the lowest function of n (f(n))
        int lowestFunctionIndex = 0;
        for (int i = 1; i < frontier.size(); i++) {
            if (frontier.get(i).f_n < frontier.get(lowestFunctionIndex).f_n)
                lowestFunctionIndex = i;
        }
        return lowestFunctionIndex;
    }


    private ArrayList<Node> successors(Node node, int heuristicChoice) {
        /* takes board configuration (from node taken by parameter) and heuristic choose
         and performs all possible successor actions calculating their h(n) (for heuristic chosen), g(n),
          and f(n) and returning arraylist of nodes that are possible successor actions for node sent in
          parameter
         */
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

    private void printSolution(Node goalNode, int enteredNodesCounter, int expandedNodesCounter) {
        /* prints solution of goal Node with number of nodes which entered the frontier and
        number of nodes which expanded from the frontier during the search and with manual changing
        of boolean values printSteps and printPath, the path and/or the steps for the search will also be displayed
         */
        ArrayList<Node> path = new ArrayList<Node>();

        for (Node node = goalNode; node != null; node = node.parent)
            path.add(node);
        Collections.reverse(path);


        boolean printSteps = false;
        boolean printPath = false;
        System.out.println("Solution");
        if(printSteps){
            for (int i = 1; i < path.size(); i++) {
                System.out.println("Step " + i + ": ");
                printBoard(path.get(i).state);
                System.out.println(("\n"));
            }
        }
        if(printPath){
            System.out.print("actions: [");
            for (int i = 1; i < path.size(); i++) {
                System.out.print(path.get(i).move + ", ");
            }
            System.out.print("]");
            System.out.println();
        }
        System.out.println("number of actions:" + (path.size() - 1));
        System.out.println("number of nodes entered frontier: " + enteredNodesCounter);
        System.out.println("number of expanded frontier: " + expandedNodesCounter);

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
        HashSet<Node> expanded = new HashSet<>();
        //counter for nodes entered and expanded initialized
        int enteredNodesCounter = 0;
        int expandedNodesCounter = 0;

        //Initializes frontier with start state node
        int h_n = heuristic(start, heuristicChoice);
        frontier.add(new Node(copyBoard(start), null, null, 0, h_n, h_n));
        enteredNodesCounter++;

        while (!frontier.isEmpty()) {
            int index = lowestFrontierGreedyIndex(frontier);
            Node node = frontier.remove(index);
            expandedNodesCounter++;

            if (isGoal(node.state)) {
                printSolution(node, enteredNodesCounter, expandedNodesCounter);
                return;
            }

            if (expanded.contains(node))
                continue;
            expanded.add(node);

            ArrayList<Node> successorNodes = successors(node, heuristicChoice);
            for (int i = 0; i < successorNodes.size(); i++) {
                Node successorNode = successorNodes.get(i);
                if (!expanded.contains(successorNode)){
                    frontier.add(successorNode);
                    enteredNodesCounter++;
                }

            }
        }
    }

    public void aStarSearch(int[][] start, int heuristicChoice) {
        ArrayList<Node> frontier = new ArrayList<>();
        HashMap<Node, Integer> lowestSeenF_n = new HashMap<>();
        //counter for nodes entered and expanded initialized
        int enteredNodesCounter = 0;
        int expandedNodesCounter = 0;

        /*Initializes frontier with start state node and adds the node to a hashmap
        with the function of n (f(n)) to be used when searching as a way to only append
        input board configurations already in the frontier that have a lower f(n) than the one
        currently in the frontier
         */
        int h_n = heuristic(start, heuristicChoice);
        Node startNode = new Node(copyBoard(start), null, null, 0, h_n, h_n);
        frontier.add(startNode);
        lowestSeenF_n.put(startNode, startNode.f_n);
        enteredNodesCounter++;

        while (!frontier.isEmpty()) {
            // lowest f(n) board configuration is expanded and checked to see if goal state
            int index = lowestAStarIndex(frontier);
            Node node = frontier.remove(index);
            expandedNodesCounter++;

            if (isGoal(node.state)) {
                printSolution(node,enteredNodesCounter, expandedNodesCounter);
                return;
            }

            /*finds all possible successor action nodes which are stored in an
            array list and the array list is traversed seeing if current board
            configuration exists (if not node configuration is added to frontier) and
            if it exists checks to see which one of the two node board configurations
            has a lower f(n). keeps the lower f(n) and discards the other
             */
            ArrayList<Node> successorNodes = successors(node, heuristicChoice);
            for (int i = 0; i < successorNodes.size(); i++) {
                Node successorNode = successorNodes.get(i);

                Integer lowestF_n = lowestSeenF_n.get(successorNode);

                if (lowestF_n == null) {
                    lowestSeenF_n.put(successorNode, successorNode.f_n);
                    frontier.add(successorNode);
                    enteredNodesCounter++;
                    continue;
                }

                if (successorNode.f_n < lowestF_n) {
                    lowestSeenF_n.remove(successorNode);
                    lowestSeenF_n.put(successorNode, successorNode.f_n);
                    enteredNodesCounter++;
                }

                }
            }
        }



    }

