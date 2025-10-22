import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        TilePuzzle tilePuzzle = new TilePuzzle();
        Scanner scanner = new Scanner(System.in);

        int[][] start = {
                {1, 4, 3},
                {2, 5, 6},
                {7, 8, 0}
        };


        while (true) {
            System.out.println("1.solve with greedy first search method");
            System.out.println("2.solve with A* Search method");
            System.out.println("3.exit");
            int searchMethodChosen = scanner.nextInt();

            if (searchMethodChosen == 3)
                break;

            if(searchMethodChosen != 1 && searchMethodChosen != 2){
                System.out.println("invalid number for search method choice entered");
                continue;
            }


            System.out.println("1. Solve with heuristic one");
            System.out.println("2. Solve with heuristic two");
            int heuristicChosen = scanner.nextInt();

            if(heuristicChosen != 1 && heuristicChosen != 2){
                System.out.println("invalid number for heuristic choice entered");
                continue;
            }


            if (searchMethodChosen == 1){
                System.out.println("Greedy first search method with h" + heuristicChosen + ":");
                long startTime = System.currentTimeMillis();
                tilePuzzle.greedyFirstSearch(start, heuristicChosen);
                long endTime = System.currentTimeMillis();
                double totalSearchTime = endTime - startTime / 1000.0;
                System.out.println("Greedy first search total search time: " + (endTime - startTime) + " seconds");
            }

            if (searchMethodChosen == 2){
                long startTime = System.currentTimeMillis();
                System.out.println("A* search method with h" + heuristicChosen + ":");
                tilePuzzle.aStarSearch(start, heuristicChosen);
                long endTime = System.currentTimeMillis();
                double totalSearchTime = endTime - startTime / 1000.0;
                System.out.println("A* search total search time: " + (endTime - startTime) + " seconds");
            }

        }

    }
}